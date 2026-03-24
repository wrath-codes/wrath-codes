"""Migrate custas tables into consolidated schema."""

from migrate import pq, step


def run(con) -> None:
    print("\n=== Custas ===")

    # -- 1. Create tabela_custas from distinct ANO_TAB in fcustas/ccustas/qcustas --
    step(con, "tabela_custas", f"""
        WITH anos AS (
            SELECT DISTINCT ANO_TAB as ano, 'PROTOCOLIZACAO' as tipo FROM read_parquet('{pq("fcustas")}') WHERE ANO_TAB IS NOT NULL
            UNION
            SELECT DISTINCT ANO_TAB, 'CANCELAMENTO' FROM read_parquet('{pq("ccustas")}') WHERE ANO_TAB IS NOT NULL
            UNION
            SELECT DISTINCT ANO_TAB, 'QUITACAO' FROM read_parquet('{pq("qcustas")}') WHERE ANO_TAB IS NOT NULL
            UNION
            SELECT DISTINCT ANO_TAB, 'ATO_FIXO' FROM read_parquet('{pq("tcustas")}') WHERE ANO_TAB IS NOT NULL
        )
        INSERT INTO tabela_custas (ano, versao, tipo)
        SELECT
            CASE WHEN ano LIKE '%A' THEN REPLACE(ano, 'A', '') ELSE ano END,
            CASE WHEN ano LIKE '%A' THEN 'A' END,
            tipo
        FROM anos
        ORDER BY ano, tipo
    """)

    # -- 2. Faixas de valor (from fcustas — distinct ranges per ano) --
    step(con, "faixa_valor (protocolizacao)", f"""
        INSERT INTO faixa_valor (tabela_custas_id, codigo, valor_de, valor_ate)
        SELECT tc.id, f.FAIXA, f.DE, f.ATE
        FROM read_parquet('{pq("fcustas")}') f
        JOIN tabela_custas tc ON tc.tipo = 'PROTOCOLIZACAO'
            AND CASE WHEN tc.versao = 'A' THEN tc.ano || 'A' ELSE tc.ano END = f.ANO_TAB
    """)

    step(con, "faixa_valor (cancelamento)", f"""
        INSERT INTO faixa_valor (tabela_custas_id, codigo, valor_de, valor_ate)
        SELECT tc.id, f.FAIXA, f.DE, f.ATE
        FROM read_parquet('{pq("ccustas")}') f
        JOIN tabela_custas tc ON tc.tipo = 'CANCELAMENTO'
            AND CASE WHEN tc.versao = 'A' THEN tc.ano || 'A' ELSE tc.ano END = f.ANO_TAB
    """)

    step(con, "faixa_valor (quitacao)", f"""
        INSERT INTO faixa_valor (tabela_custas_id, codigo, valor_de, valor_ate)
        SELECT tc.id, f.FAIXA, f.DE, f.ATE
        FROM read_parquet('{pq("qcustas")}') f
        JOIN tabela_custas tc ON tc.tipo = 'QUITACAO'
            AND CASE WHEN tc.versao = 'A' THEN tc.ano || 'A' ELSE tc.ano END = f.ANO_TAB
    """)

    # -- 3. Custas por faixa (unified) --
    step(con, "custas_faixa (protocolizacao)", f"""
        INSERT INTO custas_faixa (id, faixa_valor_id, emol, fetj, fundperj, funperj, funarpen, ressag,
            funpgalerj, funpgt, fundpguerj, mutua, acoterj, iss, val_selo, total)
        SELECT
            ROW_NUMBER() OVER (),
            fv.id,
            f.EMOL, f.FETJ, f.FUNDPERJ, f.FUNPERJ, f.FUNARPEN, f.RESSAG,
            f.FUNPGALERJ, f.FUNPGT, f.FUNDPGUERJ, f.MUTUA, f.ACOTERJ, f.ISS,
            f.VAL_SELO, f.TOT_CUSTA
        FROM read_parquet('{pq("fcustas")}') f
        JOIN tabela_custas tc ON tc.tipo = 'PROTOCOLIZACAO'
            AND CASE WHEN tc.versao = 'A' THEN tc.ano || 'A' ELSE tc.ano END = f.ANO_TAB
        JOIN faixa_valor fv ON fv.tabela_custas_id = tc.id AND fv.codigo = f.FAIXA
    """)

    con.execute("SELECT COALESCE(MAX(id), 0) FROM custas_faixa")
    offset = con.fetchone()[0]

    step(con, "custas_faixa (cancelamento)", f"""
        INSERT INTO custas_faixa (id, faixa_valor_id, emol, fetj, fundperj, funperj, funarpen, ressag,
            funpgalerj, funpgt, fundpguerj, mutua, acoterj, iss, val_selo, total)
        SELECT
            ROW_NUMBER() OVER () + {offset},
            fv.id,
            f.EMOL, f.FETJ, f.FUNDPERJ, f.FUNPERJ, f.FUNARPEN, f.RESSAG,
            NULL, NULL, NULL, f.MUTUA, f.ACOTERJ, f.ISS,
            f.VAL_SELO, f.TOT_CUSTA
        FROM read_parquet('{pq("ccustas")}') f
        JOIN tabela_custas tc ON tc.tipo = 'CANCELAMENTO'
            AND CASE WHEN tc.versao = 'A' THEN tc.ano || 'A' ELSE tc.ano END = f.ANO_TAB
        JOIN faixa_valor fv ON fv.tabela_custas_id = tc.id AND fv.codigo = f.FAIXA
    """)

    con.execute("SELECT COALESCE(MAX(id), 0) FROM custas_faixa")
    offset = con.fetchone()[0]

    step(con, "custas_faixa (quitacao)", f"""
        INSERT INTO custas_faixa (id, faixa_valor_id, emol, fetj, fundperj, funperj, funarpen, ressag,
            funpgalerj, funpgt, fundpguerj, mutua, acoterj, iss, val_selo, total)
        SELECT
            ROW_NUMBER() OVER () + {offset},
            fv.id,
            f.EMOL, f.FETJ, f.FUNDPERJ, f.FUNPERJ, f.FUNARPEN, f.RESSAG,
            NULL, NULL, NULL, f.MUTUA, f.ACOTERJ, f.ISS,
            f.VAL_SELO, f.TOT_CUSTA
        FROM read_parquet('{pq("qcustas")}') f
        JOIN tabela_custas tc ON tc.tipo = 'QUITACAO'
            AND CASE WHEN tc.versao = 'A' THEN tc.ano || 'A' ELSE tc.ano END = f.ANO_TAB
        JOIN faixa_valor fv ON fv.tabela_custas_id = tc.id AND fv.codigo = f.FAIXA
    """)

    # -- 4. Custas de ato fixo (from tcustas) --
    step(con, "custas_ato_fixo", f"""
        INSERT INTO custas_ato_fixo (id, tabela_custas_id, tipo_ato_cod,
            tabela_tjrj, item_tjrj, subitem_tjrj, descricao, qtd_ato,
            emol, fetj, fundperj, funperj, funarpen, ressag,
            funpgalerj, funpgt, fundpguerj, mutua, acoterj, iss, total)
        SELECT
            ROW_NUMBER() OVER (),
            tc.id,
            NULLIF(TRIM(t.CODFUNCAO), ''),
            NULLIF(TRIM(t.TABELA), ''),
            NULLIF(TRIM(t.ITEM), ''),
            NULLIF(TRIM(t.SUBITEM), ''),
            NULLIF(TRIM(t.DESC_CUSTA), ''),
            t.QTD_ATO,
            t.EMOL, t.FETJ, t.FUNDPERJ, t.FUNPERJ, t.FUNARPEN, t.RESSAG,
            t.FUNPGALERJ, t.FUNPGT, t.FUNDPGUERJ, t.MUTUA, t.ACOTERJ, t.ISS,
            t.TOT_CUSTA
        FROM read_parquet('{pq("tcustas")}') t
        JOIN tabela_custas tc ON tc.tipo = 'ATO_FIXO'
            AND CASE WHEN tc.versao = 'A' THEN tc.ano || 'A' ELSE tc.ano END = t.ANO_TAB
    """)
