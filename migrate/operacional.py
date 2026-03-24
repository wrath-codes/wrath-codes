"""Migrate operational tables: edital, pedidos, recibos, andamentos, selos."""

from migrate import pq, step


def run(con) -> None:
    print("\n=== Operacional ===")

    step(con, "edital", f"""
        INSERT INTO edital (id, titulo_id, dt_edital, tipo, nome_publicado, cod_motivo, motivo, serie, livro, folha)
        SELECT
            ROW_NUMBER() OVER (),
            tit.id,
            e.DTEDIT,
            NULLIF(TRIM(e.TIPO), ''),
            NULLIF(TRIM(e.NNOMME), ''),
            NULLIF(TRIM(e.CODMOT), ''),
            NULLIF(TRIM(e.MOTIVO), ''),
            NULLIF(TRIM(e.SERIE), ''),
            NULLIF(TRIM(e.LIV_EDT), ''),
            NULLIF(TRIM(e.FOL_EDT), '')
        FROM read_parquet('{pq("edital")}') e
        LEFT JOIN titulo tit ON tit.protocolo = e.PROTOCOLO
    """)

    step(con, "pedido_certidao", f"""
        INSERT INTO pedido_certidao (
            id, titulo_id, tipo_ato_cod, cod_operacao, cod_recibo,
            dt_pedido, nome_pesquisado, cpf_cnpj_pesquisado, resultado,
            dt_devolucao, selo, selo_aleatorio, ano_tabela
        )
        SELECT
            ROW_NUMBER() OVER (),
            tit.id,
            NULLIF(TRIM(p.CODFUNCAO), ''),
            NULLIF(TRIM(p.CODOPE), ''),
            NULLIF(TRIM(p.CODREC), ''),
            p.DATPED,
            NULLIF(TRIM(p.NNOMME), ''),
            NULLIF(TRIM(p.CPFCGC), ''),
            NULLIF(TRIM(p.RESULTADO), ''),
            p.DATDEV,
            NULLIF(TRIM(p.SSELLO), ''),
            NULLIF(TRIM(p.ALE_SSELLO), ''),
            NULLIF(TRIM(p.ANO_TAB), '')
        FROM read_parquet('{pq("pedidos")}') p
        LEFT JOIN titulo tit ON tit.protocolo = p.PROTOCOLO
    """)

    step(con, "recibo", f"""
        INSERT INTO recibo (
            id, codigo, titulo_id, tipo_ato_cod, dt_recibo,
            emolumentos, fetj, fundperj, funperj, funarpen, ressag,
            funpgalerj, funpgt, fundpguerj, mutua, acoterj, iss,
            taxa_guia, total, ano_tabela
        )
        SELECT
            ROW_NUMBER() OVER (),
            NULLIF(TRIM(r.CODREC), ''),
            tit.id,
            NULLIF(TRIM(r.CODFUNCAO), ''),
            r.DATREC,
            r.EMOL, r.FETJ, r.FUNDPERJ, r.FUNPERJ, r.FUNARPEN, r.RESSAG,
            r.FUNPGALERJ, r.FUNPGT, r.FUNDPGUERJ, r.MUTUA, r.ACOTERJ, r.ISS,
            r.TXGUIA, r.VALTOT,
            NULLIF(TRIM(r.ANO_TAB), '')
        FROM read_parquet('{pq("recibos")}') r
        LEFT JOIN titulo tit ON tit.protocolo = r.PROTOCOLO
    """)

    step(con, "andamento", f"""
        INSERT INTO andamento (id, titulo_id, apresentante_id, tipo_andamento_cod, num_devedor, ocorrido_em)
        SELECT
            ROW_NUMBER() OVER (),
            tit.id,
            ap.id,
            NULLIF(TRIM(a.CODDEVIRR), ''),
            NULLIF(TRIM(a.NUMDEVED), ''),
            CASE
                WHEN a.DATA_AND IS NOT NULL AND TRIM(a.HORA_AND) != ''
                THEN a.DATA_AND + CAST(a.HORA_AND AS TIME)
                ELSE CAST(a.DATA_AND AS TIMESTAMP)
            END
        FROM read_parquet('{pq("tb_andam")}') a
        LEFT JOIN titulo tit ON tit.protocolo = a.PROTOCOLO
        LEFT JOIN apresentante ap ON ap.codigo = a.CODBANCO
    """)

    step(con, "selo (from log_selo)", f"""
        INSERT INTO selo (id, titulo_id, recibo_id, tipo_ato_cod, numero, aleatorio, tipo, situacao, emitido_em)
        SELECT
            ROW_NUMBER() OVER (),
            tit.id,
            rec.id,
            NULLIF(TRIM(s.CODFUNCAO), ''),
            NULLIF(TRIM(s.SELO), ''),
            NULLIF(TRIM(s.ALEA), ''),
            NULLIF(TRIM(s.TIPO), ''),
            NULLIF(TRIM(s.SITUACAO), ''),
            CASE
                WHEN s.DATA IS NOT NULL THEN CAST(s.DATA AS TIMESTAMP)
            END
        FROM read_parquet('{pq("log_selo")}') s
        LEFT JOIN titulo tit ON tit.protocolo = s.PROTOCOLO
        LEFT JOIN (SELECT MIN(id) as id, codigo FROM recibo WHERE codigo IS NOT NULL GROUP BY codigo) rec ON rec.codigo = s.CODREC
    """)

    # Intimações (from titulos where DTINTIMA is filled, with address snapshot)
    step(con, "intimacao", f"""
        INSERT INTO intimacao (id, titulo_id, endereco_snapshot, bairro_snapshot, cidade_snapshot,
            uf_snapshot, cep_snapshot, dt_intimacao, meio, serie, selo, enviado_xml)
        SELECT
            ROW_NUMBER() OVER (),
            tit.id,
            NULLIF(TRIM(t.ENDER), ''),
            NULLIF(TRIM(t.BAIRRO), ''),
            NULLIF(TRIM(t.CID), ''),
            NULLIF(TRIM(t.EST), ''),
            NULLIF(TRIM(t.CEP), ''),
            t.DTINTIMA,
            NULLIF(TRIM(t.MEIOINTIMA), ''),
            NULLIF(TRIM(t.SERIE), ''),
            NULLIF(TRIM(t.SELO_APTM), ''),
            NULL
        FROM read_parquet('{pq("titulos")}') t
        JOIN titulo tit ON tit.protocolo = t.PROTOCOLO
        WHERE t.DTINTIMA IS NOT NULL
    """)

    # Livros
    step(con, "livro", f"""
        INSERT INTO livro (id, tipo, numero, dt_abertura, dt_fechamento, num_folhas)
        SELECT ROW_NUMBER() OVER (), 'PROTESTO', NUMLIV, DTABER, DTFECH, NUMFLS
        FROM read_parquet('{pq("livpro")}')
        UNION ALL
        SELECT ROW_NUMBER() OVER () + 1000, 'APONTAMENTO', NUMLIV, DTABER, DTFECH, NUMFLS
        FROM read_parquet('{pq("livapt")}')
    """)

    # Log operações
    step(con, "log_operacao", f"""
        INSERT INTO log_operacao (id, usuario, operacao, data, detalhes)
        SELECT
            ROW_NUMBER() OVER (),
            NULLIF(TRIM(USUARIO), ''),
            NULLIF(TRIM(OPERACA), ''),
            CASE
                WHEN DATAOPE IS NOT NULL AND TRIM(HORAOPE) != ''
                THEN DATAOPE + CAST(HORAOPE AS TIME)
                ELSE CAST(DATAOPE AS TIMESTAMP)
            END,
            NULLIF(TRIM(OBSERVA), '')
        FROM read_parquet('{pq("logop")}')
        WHERE DATAOPE IS NOT NULL
    """)
