import argparse
import json
import logging
import os
import re

import psycopg2
from psycopg2 import extras
from tqdm import tqdm


logger = logging.getLogger("DataImporter")

ADDRESS_LIMITS = {
    "logradouro": 50,
    "endereco": 150,
    "numero": 50,
    "complemento": 50,
    "bairro": 100,
    "municipio": 100,
    "municipio_ibge": 50,
    "estado": 2,
    "cep": 10,
}

REQUIRED_ADDRESS_FIELDS = (
    "logradouro",
    "endereco",
    "bairro",
    "municipio",
    "estado",
    "cep",
)


def setup_logging(log_file):
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def build_db_config(args):
    db_config = {
        "host": args.host or os.getenv("PGHOST"),
        "port": args.port or os.getenv("PGPORT", "5432"),
        "user": args.user or os.getenv("PGUSER"),
        "password": args.password or os.getenv("PGPASSWORD"),
        "dbname": args.dbname or os.getenv("PGDATABASE", "dados_dev"),
    }

    missing = [key for key, value in db_config.items() if not value]
    if missing:
        raise ValueError(
            "Missing database configuration for: "
            + ", ".join(missing)
            + ". Provide CLI args or PG* environment variables."
        )
    return db_config


def load_json_payload(file_path):
    with open(file_path, "r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("JSON payload must be an object or an array of objects.")


def ensure_single_row(rows, label, cns):
    if len(rows) > 1:
        raise ValueError(f"[{cns}] Multiple active rows found for {label}.")
    return rows[0] if rows else None


def clean_phone(phone):
    return re.sub(r"\D", "", phone or "")


def normalize_cns(raw_cns):
    digits_only = re.sub(r"\D", "", raw_cns or "")
    return digits_only[:6]


def validate_text(field_name, value, max_length, cns, required=False):
    if value is None:
        value = ""

    if not isinstance(value, str):
        value = str(value)

    value = value.strip()

    if required and not value:
        raise ValueError(f"[{cns}] Missing required field '{field_name}'.")

    if len(value) > max_length:
        raise ValueError(
            f"[{cns}] Field '{field_name}' exceeds max length {max_length}: {len(value)}."
        )

    return value


def normalize_address(address_data, cns):
    if not address_data:
        return None

    normalized = {}
    for field_name, max_length in ADDRESS_LIMITS.items():
        normalized[field_name] = validate_text(
            field_name=field_name,
            value=address_data.get(field_name, ""),
            max_length=max_length,
            cns=cns,
            required=field_name in REQUIRED_ADDRESS_FIELDS,
        )
    return normalized


def get_registry_context(cursor, cns):
    cursor.execute(
        """
        SELECT
            pda.id_pessoa,
            pda.descricao,
            pj.id_pessoa_juridica
        FROM global.pessoas_dados_adicionais pda
        INNER JOIN global.pessoas_juridicas pj
            ON pj.id_pessoa = pda.id_pessoa
           AND pj.situacao = pda.situacao
        WHERE pda.id_pessoa_dado_adicional_tipo = 2
          AND pda.descricao = %s
          AND pda.situacao = 1
        """,
        (cns,),
    )
    pessoa_row = ensure_single_row(cursor.fetchall(), "pessoa lookup", cns)

    cursor.execute(
        """
        SELECT
            s.id_serventia,
            s.codigo_tj
        FROM global.serventias s
        WHERE s.codigo_cns = %s
          AND s.situacao = 1
        """,
        (cns,),
    )
    serventia_row = ensure_single_row(cursor.fetchall(), "serventia lookup", cns)

    return {
        "cns": cns,
        "id_pessoa": pessoa_row["id_pessoa"] if pessoa_row else None,
        "id_pessoa_juridica": pessoa_row["id_pessoa_juridica"] if pessoa_row else None,
        "id_serventia": serventia_row["id_serventia"] if serventia_row else None,
        "codigo_tj": serventia_row["codigo_tj"] if serventia_row else None,
    }


def address_exists(cursor, id_pessoa, address_data):
    cursor.execute(
        """
        SELECT 1
        FROM global.pessoas_enderecos
        WHERE id_pessoa = %s
          AND id_pessoa_endereco_tipo = 3
          AND logradouro = %s
          AND endereco = %s
          AND COALESCE(numero, '') = %s
          AND COALESCE(complemento, '') = %s
          AND bairro = %s
          AND municipio = %s
          AND COALESCE(municipio_ibge, '') = %s
          AND estado = %s
          AND cep = %s
          AND situacao = 1
        LIMIT 1
        """,
        (
            id_pessoa,
            address_data["logradouro"],
            address_data["endereco"],
            address_data["numero"],
            address_data["complemento"],
            address_data["bairro"],
            address_data["municipio"],
            address_data["municipio_ibge"],
            address_data["estado"],
            address_data["cep"],
        ),
    )
    return cursor.fetchone() is not None


def insert_address(cursor, id_pessoa, address_data):
    cursor.execute(
        """
        INSERT INTO global.pessoas_enderecos (
            id_pessoa,
            id_pessoa_endereco_tipo,
            logradouro,
            endereco,
            numero,
            complemento,
            bairro,
            municipio,
            municipio_ibge,
            estado,
            cep,
            situacao
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            id_pessoa,
            3,
            address_data["logradouro"],
            address_data["endereco"],
            address_data["numero"] or None,
            address_data["complemento"] or None,
            address_data["bairro"],
            address_data["municipio"],
            address_data["municipio_ibge"] or None,
            address_data["estado"],
            address_data["cep"],
            1,
        ),
    )


def contact_exists(cursor, id_pessoa, contact_type, description):
    cursor.execute(
        """
        SELECT 1
        FROM global.pessoas_contatos
        WHERE id_pessoa = %s
          AND id_pessoa_contato_tipo = %s
          AND descricao = %s
          AND situacao = 1
        LIMIT 1
        """,
        (id_pessoa, contact_type, description),
    )
    return cursor.fetchone() is not None


def insert_contact(cursor, id_pessoa, contact_type, description):
    cursor.execute(
        """
        INSERT INTO global.pessoas_contatos (
            id_pessoa_contato_tipo,
            id_pessoa,
            descricao,
            situacao
        )
        VALUES (%s, %s, %s, %s)
        """,
        (contact_type, id_pessoa, description, 1),
    )


def assignment_exists(cursor, id_serventia, codigo):
    cursor.execute(
        """
        SELECT 1
        FROM global.serventias_atribuicoes
        WHERE id_serventia = %s
          AND id_atribuicao = %s
          AND situacao = 1
        LIMIT 1
        """,
        (id_serventia, codigo),
    )
    return cursor.fetchone() is not None


def insert_assignment(cursor, id_serventia, codigo):
    cursor.execute(
        """
        INSERT INTO global.serventias_atribuicoes (
            id_serventia,
            id_atribuicao,
            situacao
        )
        VALUES (%s, %s, %s)
        """,
        (id_serventia, codigo, 1),
    )


def employee_exists(cursor, id_pessoa_juridica, employee_name, qualification_id):
    cursor.execute(
        """
        SELECT 1
        FROM global.pessoas_fisicas pf
        INNER JOIN global.pessoas_juridicas_fisicas pjf
            ON pjf.id_pessoa_fisica = pf.id_pessoa_fisica
           AND pjf.situacao = 1
        INNER JOIN global.pessoas_fisicas_qualificacoes pfq
            ON pfq.id_pessoa_fisica_funcionario = pf.id_pessoa_fisica
           AND pfq.id_pessoa_juridica_cartorio = pjf.id_pessoa_juridica
           AND pfq.situacao = 1
        WHERE pjf.id_pessoa_juridica = %s
          AND pf.nome_registro = %s
          AND pf.situacao = 1
          AND pfq.id_pessoa_qualificacao = %s
        LIMIT 1
        """,
        (id_pessoa_juridica, employee_name, qualification_id),
    )
    return cursor.fetchone() is not None


def create_employee(cursor, id_pessoa_juridica, employee_name, qualification_id):
    cursor.execute(
        """
        INSERT INTO global.pessoas (
            id_pessoa_tipo,
            id_pessoa_origem,
            pessoa,
            situacao
        )
        VALUES (%s, %s, %s, %s)
        RETURNING id_pessoa
        """,
        (6, 2, 0, 1),
    )
    new_id_pessoa = cursor.fetchone()["id_pessoa"]

    cursor.execute(
        """
        INSERT INTO global.pessoas_fisicas (
            id_pessoa,
            id_pessoa_genero,
            id_pessoa_estado_civil,
            cpf_justificativa,
            nome_registro,
            situacao
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id_pessoa_fisica
        """,
        (new_id_pessoa, 1, 1, 1, employee_name, 1),
    )
    new_id_pessoa_fisica = cursor.fetchone()["id_pessoa_fisica"]

    cursor.execute(
        """
        INSERT INTO global.pessoas_juridicas_fisicas (
            id_pessoa_juridica,
            id_pessoa_fisica,
            id_pessoa_juridica_perfil,
            juridica_principal,
            situacao
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (id_pessoa_juridica, new_id_pessoa_fisica, 3, 0, 1),
    )

    cursor.execute(
        """
        INSERT INTO global.pessoas_fisicas_qualificacoes (
            id_pessoa_juridica_cartorio,
            id_pessoa_fisica_funcionario,
            id_pessoa_qualificacao,
            situacao
        )
        VALUES (%s, %s, %s, %s)
        """,
        (id_pessoa_juridica, new_id_pessoa_fisica, qualification_id, 1),
    )


def process_record(cursor, item):
    raw_cns = validate_text("cns", item.get("cns"), 50, "unknown", required=True)
    cns = normalize_cns(raw_cns)
    if len(cns) != 6:
        raise ValueError(f"[{raw_cns}] CNS must contain at least 6 digits after normalization.")
    context = get_registry_context(cursor, cns)
    logger.info("[%s -> %s] Lookup completed: %s", raw_cns, cns, context)

    id_pessoa = context["id_pessoa"]
    id_pessoa_juridica = context["id_pessoa_juridica"]
    id_serventia = context["id_serventia"]

    if id_pessoa and not id_pessoa_juridica:
        raise ValueError(f"[{raw_cns}] Found id_pessoa without id_pessoa_juridica.")

    if not id_serventia:
        raise ValueError(f"[{raw_cns}] Mandatory step failed: id_serventia not found.")

    if id_pessoa:
        address_data = normalize_address(item.get("endereco", {}), cns)
        if address_data and not address_exists(cursor, id_pessoa, address_data):
            insert_address(cursor, id_pessoa, address_data)
            logger.info("[%s] Address inserted.", raw_cns)
        elif address_data:
            logger.info("[%s] Address already exists. Skipping.", raw_cns)
    else:
        logger.info("[%s] Address step skipped: no id_pessoa.", raw_cns)

    if id_pessoa:
        contato = item.get("contato", {}) or {}

        phone = clean_phone(contato.get("telefonePrincipal"))
        if phone:
            phone = validate_text("telefonePrincipal", phone, 50, cns, required=True)
            if not contact_exists(cursor, id_pessoa, 4, phone):
                insert_contact(cursor, id_pessoa, 4, phone)
                logger.info("[%s] Phone contact inserted.", raw_cns)
            else:
                logger.info("[%s] Phone contact already exists. Skipping.", raw_cns)

        email = contato.get("eMail")
        if email:
            email = validate_text("eMail", email, 50, cns, required=True)
            if not contact_exists(cursor, id_pessoa, 1, email):
                insert_contact(cursor, id_pessoa, 1, email)
                logger.info("[%s] Email contact inserted.", raw_cns)
            else:
                logger.info("[%s] Email contact already exists. Skipping.", raw_cns)
    else:
        logger.info("[%s] Contact step skipped: no id_pessoa.", raw_cns)

    assignments = item.get("atribuicoes", [])
    if not assignments:
        raise ValueError(f"[{raw_cns}] Mandatory step failed: no atribuicoes provided.")

    assignment_codes = []
    for assignment in assignments:
        codigo = assignment.get("codigo")
        if codigo is None:
            raise ValueError(f"[{raw_cns}] Found atribuicao without codigo.")
        assignment_codes.append(codigo)

    for codigo in assignment_codes:
        if not assignment_exists(cursor, id_serventia, codigo):
            insert_assignment(cursor, id_serventia, codigo)
            logger.info("[%s] Assignment %s inserted.", raw_cns, codigo)
        else:
            logger.info("[%s] Assignment %s already exists. Skipping.", raw_cns, codigo)

    if id_pessoa:
        responsaveis = item.get("responsaveis", [])
        for responsavel in responsaveis:
            for field_name, qualification_id in (("responsavel", 1), ("substituto", 5)):
                employee_name = responsavel.get(field_name)
                if not employee_name:
                    continue

                employee_name = validate_text(
                    field_name=field_name,
                    value=employee_name,
                    max_length=150,
                    cns=cns,
                    required=True,
                )
                if employee_exists(cursor, id_pessoa_juridica, employee_name, qualification_id):
                    logger.info(
                        "[%s] Employee '%s' with qualification %s already exists. Skipping.",
                        raw_cns,
                        employee_name,
                        qualification_id,
                    )
                    continue

                create_employee(cursor, id_pessoa_juridica, employee_name, qualification_id)
                logger.info(
                    "[%s] Employee '%s' inserted with qualification %s.",
                    raw_cns,
                    employee_name,
                    qualification_id,
                )
    else:
        logger.info("[%s] Employee step skipped: no id_pessoa.", raw_cns)


def process_json_file(file_path, db_config):
    try:
        data = load_json_payload(file_path)
        logger.info("Successfully loaded JSON file: %s", file_path)
    except Exception as exc:
        logger.error("Failed to read or parse the JSON file: %s", exc)
        return 1

    conn = None
    cursor = None
    processed = 0
    failed = 0

    try:
        conn = psycopg2.connect(**db_config)
        conn.autocommit = False
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        logger.info("Successfully connected to the database: %s", db_config["dbname"])

        for item in tqdm(data, desc="Processing CNS Data", unit="record"):
            cns_value = item.get("cns", "unknown")
            try:
                process_record(cursor, item)
                conn.commit()
                processed += 1
                logger.info("[%s] Transaction committed successfully.", cns_value)
            except Exception as exc:
                conn.rollback()
                failed += 1
                logger.error("[%s] Error processing item. Transaction rolled back. Details: %s", cns_value, exc)

        logger.info("Processing finished. Successful: %s. Failed: %s.", processed, failed)
        return 0 if failed == 0 else 2
    except Exception as exc:
        logger.error("Fatal database error: %s", exc)
        return 1
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
            logger.info("Database connection closed.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Import payload JSON into PostgreSQL with progress bar and duplicate-safe inserts."
    )
    parser.add_argument("file_path", help="Path to the JSON file to be imported.")
    parser.add_argument("--host", help="Database host. Falls back to PGHOST.")
    parser.add_argument("--port", help="Database port. Falls back to PGPORT.")
    parser.add_argument("--user", help="Database user. Falls back to PGUSER.")
    parser.add_argument("--password", help="Database password. Falls back to PGPASSWORD.")
    parser.add_argument("--dbname", help="Database name. Falls back to PGDATABASE or dados_dev.")
    parser.add_argument(
        "--log-file",
        default="import_script.log",
        help="Path to the log file. Default: import_script.log",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    setup_logging(arguments.log_file)

    try:
        config = build_db_config(arguments)
    except ValueError as exc:
        logger.error("%s", exc)
        raise SystemExit(1)

    raise SystemExit(process_json_file(arguments.file_path, config))

