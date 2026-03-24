"""Migrate pessoa + role tables (apresentante, devedor, credor, sacador)."""

from migrate import pq, step


def run(con) -> None:
    print("\n=== Pessoas & Roles ===")

    # -- 1. Apresentantes (from bancos) --
    step(con, "pessoa (apresentantes)", f"""
        INSERT INTO pessoa (nome, cpf_cnpj, tipo_documento, endereco, bairro, cidade, uf, cep)
        SELECT
            NOMEBANCO,
            NULLIF(TRIM(CGCBANCO), ''),
            CASE WHEN NULLIF(TRIM(CGCBANCO), '') IS NOT NULL THEN 'CNPJ' END,
            NULLIF(TRIM(ENDBANCO), ''),
            NULLIF(TRIM(BAIBANCO), ''),
            NULLIF(TRIM(CIDBANCO), ''),
            NULLIF(TRIM(UFBANCO), ''),
            NULLIF(TRIM(CEPBANCO), '')
        FROM read_parquet('{pq("bancos")}')
        WHERE NOMEBANCO IS NOT NULL AND TRIM(NOMEBANCO) != ''
    """)

    # Need row-level join since multiple bancos can share same name/CNPJ
    # Use a temp mapping table
    con.execute(f"""
        CREATE TEMP TABLE _banco_pessoa AS
        SELECT b.CODBANCO, p.id as pessoa_id,
            ROW_NUMBER() OVER (PARTITION BY b.CODBANCO ORDER BY p.id) as rn
        FROM read_parquet('{pq("bancos")}') b
        JOIN pessoa p ON p.nome = b.NOMEBANCO
            AND COALESCE(p.cpf_cnpj, '') = COALESCE(NULLIF(TRIM(b.CGCBANCO), ''), '')
        WHERE b.NOMEBANCO IS NOT NULL AND TRIM(b.NOMEBANCO) != ''
    """)

    step(con, "apresentante", f"""
        INSERT INTO apresentante (pessoa_id, codigo, convenio_cra, remessa_cra, tipo_apresentacao)
        SELECT
            bp.pessoa_id,
            b.CODBANCO,
            NULLIF(TRIM(b.CONVENIO), ''),
            COALESCE(b.REMCRA = 'S', FALSE),
            NULLIF(TRIM(b.TIPO_APR), '')
        FROM read_parquet('{pq("bancos")}') b
        JOIN _banco_pessoa bp ON bp.CODBANCO = b.CODBANCO AND bp.rn = 1
    """)

    # -- 2. Devedores (from titulos — deduplicated) --
    # Use CPF/CGC as primary dedup key, fallback to name
    step(con, "pessoa (devedores)", f"""
        WITH dedup AS (
            SELECT
                TRIM(SACADO) as nome,
                COALESCE(NULLIF(TRIM(CPF), ''), NULLIF(TRIM(CGC), '')) as doc,
                NULLIF(TRIM(ENDER), '') as endereco,
                NULLIF(TRIM(BAIRRO), '') as bairro,
                NULLIF(TRIM(CID), '') as cidade,
                NULLIF(TRIM(EST), '') as uf,
                NULLIF(TRIM(CEP), '') as cep,
                ROW_NUMBER() OVER (
                    PARTITION BY COALESCE(
                        NULLIF(TRIM(CPF), ''),
                        NULLIF(TRIM(CGC), ''),
                        UPPER(TRIM(SACADO))
                    )
                    ORDER BY DTENTRADA DESC NULLS LAST
                ) as rn
            FROM read_parquet('{pq("titulos")}')
            WHERE SACADO IS NOT NULL AND TRIM(SACADO) != ''
        )
        INSERT INTO pessoa (nome, cpf_cnpj, tipo_documento, endereco, bairro, cidade, uf, cep)
        SELECT
            nome, doc,
            CASE
                WHEN doc IS NOT NULL AND LENGTH(doc) > 11 THEN 'CNPJ'
                WHEN doc IS NOT NULL THEN 'CPF'
            END,
            endereco, bairro, cidade, uf, cep
        FROM dedup WHERE rn = 1
    """)

    step(con, "devedor", f"""
        WITH dedup AS (
            SELECT
                COALESCE(
                    NULLIF(TRIM(CPF), ''),
                    NULLIF(TRIM(CGC), ''),
                    UPPER(TRIM(SACADO))
                ) as dedup_key,
                MAX(CASE WHEN TRIM(FALENCIA) = 'S' THEN TRUE ELSE FALSE END) as falencia
            FROM read_parquet('{pq("titulos")}')
            WHERE SACADO IS NOT NULL AND TRIM(SACADO) != ''
            GROUP BY 1
        )
        INSERT INTO devedor (pessoa_id, falencia)
        SELECT p.id, d.falencia
        FROM dedup d
        JOIN pessoa p ON COALESCE(p.cpf_cnpj, UPPER(TRIM(p.nome))) = d.dedup_key
        WHERE p.id NOT IN (SELECT pessoa_id FROM apresentante)
    """)

    # -- 3. Co-emitentes extras (from coemit, not already in devedor) --
    step(con, "pessoa (co-emitentes novos)", f"""
        WITH existing_docs AS (
            SELECT cpf_cnpj FROM pessoa WHERE cpf_cnpj IS NOT NULL
        ),
        existing_names AS (
            SELECT UPPER(TRIM(nome)) as nome FROM pessoa
        ),
        coem AS (
            SELECT
                TRIM(COEMITENTE) as nome,
                COALESCE(NULLIF(TRIM(CPFCOEMIT), ''), NULLIF(TRIM(CGCCOEMIT), '')) as doc,
                NULLIF(TRIM(ENDCOEMIT), '') as endereco,
                NULLIF(TRIM(BAIRCOEMIT), '') as bairro,
                NULLIF(TRIM(CIDCOEMIT), '') as cidade,
                NULLIF(TRIM(ESTCOEMIT), '') as uf,
                NULLIF(TRIM(CEPCOEMIT), '') as cep,
                ROW_NUMBER() OVER (
                    PARTITION BY COALESCE(
                        NULLIF(TRIM(CPFCOEMIT), ''),
                        NULLIF(TRIM(CGCCOEMIT), ''),
                        UPPER(TRIM(COEMITENTE))
                    )
                    ORDER BY COEMITENTE
                ) as rn
            FROM read_parquet('{pq("coemit")}')
            WHERE COEMITENTE IS NOT NULL AND TRIM(COEMITENTE) != ''
        )
        INSERT INTO pessoa (nome, cpf_cnpj, tipo_documento, endereco, bairro, cidade, uf, cep)
        SELECT nome, doc,
            CASE WHEN doc IS NOT NULL AND LENGTH(doc) > 11 THEN 'CNPJ'
                 WHEN doc IS NOT NULL THEN 'CPF' END,
            endereco, bairro, cidade, uf, cep
        FROM coem
        WHERE rn = 1
          AND (doc IS NOT NULL AND doc NOT IN (SELECT cpf_cnpj FROM existing_docs)
               OR doc IS NULL AND UPPER(TRIM(nome)) NOT IN (SELECT nome FROM existing_names))
    """)

    step(con, "devedor (co-emitentes novos)", f"""
        WITH coem_keys AS (
            SELECT DISTINCT COALESCE(
                NULLIF(TRIM(CPFCOEMIT), ''),
                NULLIF(TRIM(CGCCOEMIT), ''),
                UPPER(TRIM(COEMITENTE))
            ) as dedup_key,
            MAX(CASE WHEN TRIM(FALENCIA) = 'S' THEN TRUE ELSE FALSE END) as falencia
            FROM read_parquet('{pq("coemit")}')
            WHERE COEMITENTE IS NOT NULL AND TRIM(COEMITENTE) != ''
            GROUP BY 1
        )
        INSERT INTO devedor (pessoa_id, falencia)
        SELECT p.id, ck.falencia
        FROM coem_keys ck
        JOIN pessoa p ON COALESCE(p.cpf_cnpj, UPPER(TRIM(p.nome))) = ck.dedup_key
        WHERE p.id NOT IN (SELECT pessoa_id FROM devedor)
          AND p.id NOT IN (SELECT pessoa_id FROM apresentante)
    """)

    # -- 4. Credores (from titulos — deduplicated by name) --
    step(con, "pessoa (credores novos)", f"""
        WITH existing AS (
            SELECT UPPER(TRIM(nome)) as nome FROM pessoa
        ),
        cred AS (
            SELECT DISTINCT TRIM(CEDENTE) as nome
            FROM read_parquet('{pq("titulos")}')
            WHERE CEDENTE IS NOT NULL AND TRIM(CEDENTE) != ''
        )
        INSERT INTO pessoa (nome)
        SELECT nome FROM cred
        WHERE UPPER(TRIM(nome)) NOT IN (SELECT nome FROM existing)
    """)

    step(con, "credor", f"""
        WITH cred_data AS (
            SELECT
                TRIM(CEDENTE) as nome,
                NULLIF(TRIM(AG_CEDEN), '') as agencia,
                NULLIF(TRIM(NOSSONUM), '') as nosso_numero,
                ROW_NUMBER() OVER (PARTITION BY UPPER(TRIM(CEDENTE)) ORDER BY DTENTRADA DESC NULLS LAST) as rn
            FROM read_parquet('{pq("titulos")}')
            WHERE CEDENTE IS NOT NULL AND TRIM(CEDENTE) != ''
        )
        INSERT INTO credor (pessoa_id, agencia, nosso_numero)
        SELECT p.id, cd.agencia, cd.nosso_numero
        FROM cred_data cd
        JOIN pessoa p ON UPPER(TRIM(p.nome)) = UPPER(TRIM(cd.nome))
        WHERE cd.rn = 1
          AND p.id NOT IN (SELECT pessoa_id FROM credor)
          AND p.id NOT IN (SELECT pessoa_id FROM apresentante)
    """)

    # -- 5. Sacadores (from titulos — deduplicated) --
    step(con, "pessoa (sacadores novos)", f"""
        WITH existing AS (
            SELECT UPPER(TRIM(nome)) as nome FROM pessoa
            UNION
            SELECT cpf_cnpj FROM pessoa WHERE cpf_cnpj IS NOT NULL
        ),
        sac AS (
            SELECT
                TRIM(SACADOR) as nome,
                NULLIF(TRIM(DOCSACADOR), '') as doc,
                NULLIF(TRIM(ENDSACADOR), '') as endereco,
                NULLIF(TRIM(CIDSACADOR), '') as cidade,
                NULLIF(TRIM(UFSACADOR), '') as uf,
                NULLIF(TRIM(BAISACADOR), '') as bairro,
                NULLIF(TRIM(CEPSACADOR), '') as cep,
                ROW_NUMBER() OVER (
                    PARTITION BY COALESCE(NULLIF(TRIM(DOCSACADOR), ''), UPPER(TRIM(SACADOR)))
                    ORDER BY DTENTRADA DESC NULLS LAST
                ) as rn
            FROM read_parquet('{pq("titulos")}')
            WHERE SACADOR IS NOT NULL AND TRIM(SACADOR) != ''
        )
        INSERT INTO pessoa (nome, cpf_cnpj, tipo_documento, endereco, bairro, cidade, uf, cep)
        SELECT nome, doc,
            CASE WHEN doc IS NOT NULL AND LENGTH(doc) > 11 THEN 'CNPJ'
                 WHEN doc IS NOT NULL THEN 'CPF' END,
            endereco, bairro, cidade, uf, cep
        FROM sac
        WHERE rn = 1
          AND COALESCE(doc, UPPER(TRIM(nome))) NOT IN (SELECT nome FROM existing)
    """)

    step(con, "sacador", f"""
        WITH sac_keys AS (
            SELECT DISTINCT COALESCE(NULLIF(TRIM(DOCSACADOR), ''), UPPER(TRIM(SACADOR))) as dedup_key
            FROM read_parquet('{pq("titulos")}')
            WHERE SACADOR IS NOT NULL AND TRIM(SACADOR) != ''
        )
        INSERT INTO sacador (pessoa_id)
        SELECT p.id
        FROM sac_keys sk
        JOIN pessoa p ON COALESCE(p.cpf_cnpj, UPPER(TRIM(p.nome))) = sk.dedup_key
        WHERE p.id NOT IN (SELECT pessoa_id FROM sacador)
          AND p.id NOT IN (SELECT pessoa_id FROM devedor)
          AND p.id NOT IN (SELECT pessoa_id FROM credor)
          AND p.id NOT IN (SELECT pessoa_id FROM apresentante)
    """)

    total = con.execute("SELECT COUNT(*) FROM pessoa").fetchone()[0]
    print(f"  {'TOTAL pessoa':<45} {total:>8,} rows")
