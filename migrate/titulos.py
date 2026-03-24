"""Migrate titulo, titulo_cheque, coemitente."""

from migrate import pq, step


def run(con) -> None:
    print("\n=== Títulos ===")

    step(con, "titulo", f"""
        WITH sit_map AS (
            SELECT
                t.*,
                CASE
                    WHEN SITUACAO LIKE 'APONTADO%' THEN 'APONTADO'
                    WHEN SITUACAO LIKE 'PROTESTADO%' THEN 'PROTESTADO'
                    WHEN SITUACAO LIKE 'PAGO%' THEN 'PAGO'
                    WHEN SITUACAO LIKE 'DEVOLVIDO%' THEN 'DEVOLVIDO'
                    WHEN SITUACAO LIKE 'RETIRADO%' THEN 'RETIRADO'
                    WHEN SITUACAO LIKE 'CANCELADO%' THEN 'CANCELADO'
                    WHEN SITUACAO LIKE 'SUSTADO%' THEN 'SUSTADO'
                    WHEN SITUACAO IN ('SUSPENSO', 'SUSP. EFEITOS') THEN 'SUSPENSO'
                    ELSE 'DESCONHECIDO'
                END as sit,
                CASE
                    WHEN SITUACAO LIKE '%/INTERNET%' THEN 'INTERNET'
                    WHEN SITUACAO LIKE '%/CONVENIO%' THEN 'CONVENIO'
                    WHEN SITUACAO LIKE '%/SERVENTIA%' THEN 'SERVENTIA'
                    WHEN SITUACAO = 'RETIRADO' THEN 'BALCAO'
                    WHEN SITUACAO = 'CANCELADO' THEN 'BALCAO'
                END as can,
                CASE
                    WHEN SITUACAO LIKE '%/JG%' THEN 'JG'
                    WHEN SITUACAO LIKE '%/SC%' THEN 'SC'
                    WHEN SITUACAO LIKE '%DEFINITIVO%' THEN 'DEFINITIVO'
                    WHEN SITUACAO = 'SUSP. EFEITOS' THEN 'EFEITOS'
                END as sub
            FROM read_parquet('{pq("titulos")}') t
        )
        INSERT INTO titulo (
            protocolo, devedor_id, credor_id, sacador_id, apresentante_id,
            especie, num_documento, valor_documento, valor_titulo, custas,
            emissao, vencimento, dt_entrada, dt_intimacao, meio_intimacao,
            dt_protesto, dt_pagamento, situacao, canal, sub_tipo,
            aceite, endosso, moeda, razoes, razao_protesto,
            num_distribuicao, livro, folha, livro_apontamento, folha_apontamento,
            ano_tabela, arquivo_remessa, arquivo_retorno, data_retorno, gratuidade
        )
        SELECT
            t.PROTOCOLO,
            d.id,
            cr.id,
            sa.id,
            ap.id,
            NULLIF(TRIM(t.TIPODOC), ''),
            NULLIF(TRIM(t.NUMDOC), ''),
            t.VALORDOC,
            t.VALORTIT,
            t.CUSTAS,
            t.EMISSAO,
            t.VENCIMENTO,
            t.DTENTRADA,
            t.DTINTIMA,
            NULLIF(TRIM(t.MEIOINTIMA), ''),
            t.DTPROTESTO,
            t.DTPAGTO,
            t.sit,
            t.can,
            t.sub,
            NULLIF(TRIM(t.ACEITE), ''),
            NULLIF(TRIM(t.ENDOSSO), ''),
            NULLIF(TRIM(t.MOEDA), ''),
            NULLIF(TRIM(t.RAZOES), ''),
            NULLIF(TRIM(t.RAZPROT), ''),
            NULLIF(TRIM(t.NUMDISTRIB), ''),
            NULLIF(TRIM(t.LIVRO), ''),
            CAST(t.FOLHAS AS INTEGER),
            NULLIF(TRIM(t.LIVAPT), ''),
            NULLIF(TRIM(t.FOLAPT), ''),
            NULLIF(TRIM(t.ANO_TAB), ''),
            NULLIF(TRIM(t.ARQREMESSA), ''),
            NULLIF(TRIM(t.ARQRETORNO), ''),
            t.DATRETORNO,
            COALESCE(TRIM(t.GRATUIDADE) = 'S', FALSE)
        FROM sit_map t
        LEFT JOIN (
            SELECT d.id, p.cpf_cnpj, UPPER(TRIM(p.nome)) as nome_upper
            FROM devedor d JOIN pessoa p ON d.pessoa_id = p.id
        ) d ON COALESCE(d.cpf_cnpj, d.nome_upper) = COALESCE(
            NULLIF(TRIM(t.CPF), ''),
            NULLIF(TRIM(t.CGC), ''),
            UPPER(TRIM(t.SACADO))
        )
        LEFT JOIN (
            SELECT cr.id, UPPER(TRIM(p.nome)) as nome_upper
            FROM credor cr JOIN pessoa p ON cr.pessoa_id = p.id
        ) cr ON cr.nome_upper = UPPER(TRIM(t.CEDENTE))
        LEFT JOIN (
            SELECT sa.id, p.cpf_cnpj, UPPER(TRIM(p.nome)) as nome_upper
            FROM sacador sa JOIN pessoa p ON sa.pessoa_id = p.id
        ) sa ON COALESCE(sa.cpf_cnpj, sa.nome_upper) = COALESCE(
            NULLIF(TRIM(t.DOCSACADOR), ''),
            UPPER(TRIM(t.SACADOR))
        )
        LEFT JOIN apresentante ap ON ap.codigo = t.CODBANCO
        WHERE t.PROTOCOLO IS NOT NULL AND TRIM(t.PROTOCOLO) != ''
        QUALIFY ROW_NUMBER() OVER (PARTITION BY t.PROTOCOLO ORDER BY t.DTENTRADA DESC NULLS LAST) = 1
    """)

    step(con, "titulo_cheque", f"""
        INSERT INTO titulo_cheque (id, titulo_id, numero, banco, agencia, valor, data)
        SELECT
            ROW_NUMBER() OVER (),
            tit.id,
            NULLIF(TRIM(t.NUMCHEQUE), ''),
            NULLIF(TRIM(t.BCO), ''),
            NULLIF(TRIM(t.AGENCIA), ''),
            t.VLRCHEQUE,
            t.DTCHEQUE
        FROM read_parquet('{pq("titulos")}') t
        JOIN titulo tit ON tit.protocolo = t.PROTOCOLO
        WHERE TRIM(t.TIPODOC) = 'CH'
    """)

    step(con, "coemitente", f"""
        INSERT INTO coemitente (id, titulo_id, devedor_id, dt_intimacao, meio_intimacao)
        SELECT
            ROW_NUMBER() OVER (),
            tit.id,
            d.id,
            c.DTINTIMA,
            NULLIF(TRIM(c.MEIOINTIMA), '')
        FROM read_parquet('{pq("coemit")}') c
        JOIN titulo tit ON tit.protocolo = c.PROTOCOLO
        LEFT JOIN (
            SELECT d.id, p.cpf_cnpj, UPPER(TRIM(p.nome)) as nome_upper
            FROM devedor d JOIN pessoa p ON d.pessoa_id = p.id
        ) d ON COALESCE(d.cpf_cnpj, d.nome_upper) = COALESCE(
            NULLIF(TRIM(c.CPFCOEMIT), ''),
            NULLIF(TRIM(c.CGCCOEMIT), ''),
            UPPER(TRIM(c.COEMITENTE))
        )
        WHERE d.id IS NOT NULL
    """)
