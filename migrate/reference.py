"""Migrate reference/lookup tables."""

from migrate import pq, step


def run(con) -> None:
    print("\n=== Reference Tables ===")

    step(con, "especie_titulo", f"""
        INSERT INTO especie_titulo
        SELECT SIGLA, DESCRICAO, COD_XML, COALESCE(DIVERSOS = 'S', FALSE)
        FROM read_parquet('{pq("tbtiptit")}')
    """)

    step(con, "tipo_ato", f"""
        INSERT INTO tipo_ato
        SELECT CODFUNCAO, FUNCAO
        FROM read_parquet('{pq("tfuncao")}')
    """)

    step(con, "tipo_irregularidade", f"""
        INSERT INTO tipo_irregularidade
        SELECT CODIRREG, DESCIRREG
        FROM read_parquet('{pq("tb_irreg")}')
    """)

    step(con, "tipo_andamento", """
        INSERT INTO tipo_andamento VALUES
        ('AA', 'Apontamento'),
        ('AB', 'Baixa/Retirada pelo Apresentante'),
        ('AC', 'Confirmação de Apontamento'),
        ('AD', 'Desistência pelo Devedor'),
        ('AE', 'Edital (Devedor não localizado)'),
        ('AF', 'Anuência do Apresentante'),
        ('AG', 'Guia de Pagamento'),
        ('AI', 'Intimação'),
        ('AJ', 'Ajuizamento'),
        ('AK', 'Cancelamento')
    """)

    step(con, "feriado", f"""
        INSERT INTO feriado
        SELECT DATAFER, DESCRI
        FROM read_parquet('{pq("feriados")}')
    """)
