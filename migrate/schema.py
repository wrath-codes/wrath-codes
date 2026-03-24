"""DDL: Create all tables for the new schema."""


def run(con) -> None:
    print("\n=== Schema ===")

    con.execute("""
    -- Reference tables
    CREATE TABLE especie_titulo (
        sigla VARCHAR PRIMARY KEY,
        descricao VARCHAR NOT NULL,
        cod_xml VARCHAR,
        aceita_diversos BOOLEAN DEFAULT FALSE
    );
    CREATE TABLE tipo_ato (
        codigo VARCHAR PRIMARY KEY,
        descricao VARCHAR NOT NULL
    );
    CREATE TABLE tipo_irregularidade (
        codigo VARCHAR PRIMARY KEY,
        descricao VARCHAR NOT NULL
    );
    CREATE TABLE tipo_andamento (
        codigo VARCHAR PRIMARY KEY,
        descricao VARCHAR
    );
    CREATE TABLE feriado (
        data DATE PRIMARY KEY,
        descricao VARCHAR
    );

    -- Person / Role
    CREATE SEQUENCE seq_pessoa START 1;
    CREATE TABLE pessoa (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_pessoa'),
        nome VARCHAR NOT NULL,
        cpf_cnpj VARCHAR,
        tipo_documento VARCHAR,
        endereco VARCHAR,
        bairro VARCHAR,
        cidade VARCHAR,
        uf VARCHAR,
        cep VARCHAR
    );

    CREATE SEQUENCE seq_apresentante START 1;
    CREATE TABLE apresentante (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_apresentante'),
        pessoa_id INTEGER NOT NULL REFERENCES pessoa(id),
        codigo VARCHAR UNIQUE NOT NULL,
        convenio_cra VARCHAR,
        remessa_cra BOOLEAN,
        tipo_apresentacao VARCHAR
    );

    CREATE SEQUENCE seq_devedor START 1;
    CREATE TABLE devedor (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_devedor'),
        pessoa_id INTEGER NOT NULL REFERENCES pessoa(id),
        falencia BOOLEAN DEFAULT FALSE,
        sustacao BOOLEAN DEFAULT FALSE,
        cod_irregularidade VARCHAR,
        oficio VARCHAR
    );

    CREATE SEQUENCE seq_credor START 1;
    CREATE TABLE credor (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_credor'),
        pessoa_id INTEGER NOT NULL REFERENCES pessoa(id),
        agencia VARCHAR,
        nosso_numero VARCHAR
    );

    CREATE SEQUENCE seq_sacador START 1;
    CREATE TABLE sacador (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_sacador'),
        pessoa_id INTEGER NOT NULL REFERENCES pessoa(id)
    );

    -- Core
    CREATE SEQUENCE seq_titulo START 1;
    CREATE TABLE titulo (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_titulo'),
        protocolo VARCHAR UNIQUE NOT NULL,
        devedor_id INTEGER REFERENCES devedor(id),
        credor_id INTEGER REFERENCES credor(id),
        sacador_id INTEGER REFERENCES sacador(id),
        apresentante_id INTEGER REFERENCES apresentante(id),
        especie VARCHAR,
        num_documento VARCHAR,
        valor_documento DOUBLE,
        valor_titulo DOUBLE,
        custas DOUBLE,
        emissao DATE,
        vencimento DATE,
        dt_entrada DATE,
        dt_intimacao DATE,
        meio_intimacao VARCHAR,
        dt_protesto DATE,
        dt_pagamento DATE,
        situacao VARCHAR NOT NULL,
        canal VARCHAR,
        sub_tipo VARCHAR,
        aceite VARCHAR,
        endosso VARCHAR,
        moeda VARCHAR,
        razoes VARCHAR,
        razao_protesto VARCHAR,
        num_distribuicao VARCHAR,
        livro VARCHAR,
        folha INTEGER,
        livro_apontamento VARCHAR,
        folha_apontamento VARCHAR,
        ano_tabela VARCHAR,
        arquivo_remessa VARCHAR,
        arquivo_retorno VARCHAR,
        data_retorno DATE,
        gratuidade BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE titulo_cheque (
        id INTEGER PRIMARY KEY,
        titulo_id INTEGER UNIQUE NOT NULL REFERENCES titulo(id),
        numero VARCHAR,
        banco VARCHAR,
        agencia VARCHAR,
        valor DOUBLE,
        data DATE
    );

    CREATE TABLE coemitente (
        id INTEGER PRIMARY KEY,
        titulo_id INTEGER NOT NULL REFERENCES titulo(id),
        devedor_id INTEGER NOT NULL REFERENCES devedor(id),
        dt_intimacao DATE,
        meio_intimacao VARCHAR
    );

    CREATE TABLE intimacao (
        id INTEGER PRIMARY KEY,
        titulo_id INTEGER NOT NULL REFERENCES titulo(id),
        endereco_snapshot VARCHAR,
        bairro_snapshot VARCHAR,
        cidade_snapshot VARCHAR,
        uf_snapshot VARCHAR,
        cep_snapshot VARCHAR,
        dt_intimacao DATE,
        meio VARCHAR,
        serie VARCHAR,
        selo VARCHAR,
        enviado_xml BOOLEAN
    );

    CREATE TABLE edital (
        id INTEGER PRIMARY KEY,
        titulo_id INTEGER REFERENCES titulo(id),
        dt_edital DATE,
        tipo VARCHAR,
        nome_publicado VARCHAR,
        cod_motivo VARCHAR,
        motivo VARCHAR,
        serie VARCHAR,
        livro VARCHAR,
        folha VARCHAR
    );

    CREATE TABLE pedido_certidao (
        id INTEGER PRIMARY KEY,
        titulo_id INTEGER REFERENCES titulo(id),
        tipo_ato_cod VARCHAR REFERENCES tipo_ato(codigo),
        cod_operacao VARCHAR,
        cod_recibo VARCHAR,
        dt_pedido DATE,
        nome_pesquisado VARCHAR,
        cpf_cnpj_pesquisado VARCHAR,
        resultado VARCHAR,
        dt_devolucao DATE,
        selo VARCHAR,
        selo_aleatorio VARCHAR,
        ano_tabela VARCHAR
    );

    CREATE TABLE recibo (
        id INTEGER PRIMARY KEY,
        codigo VARCHAR,
        titulo_id INTEGER REFERENCES titulo(id),
        tipo_ato_cod VARCHAR REFERENCES tipo_ato(codigo),
        dt_recibo DATE,
        emolumentos DOUBLE,
        fetj DOUBLE,
        fundperj DOUBLE,
        funperj DOUBLE,
        funarpen DOUBLE,
        ressag DOUBLE,
        funpgalerj DOUBLE,
        funpgt DOUBLE,
        fundpguerj DOUBLE,
        mutua DOUBLE,
        acoterj DOUBLE,
        iss DOUBLE,
        taxa_guia DOUBLE,
        total DOUBLE,
        ano_tabela VARCHAR
    );

    CREATE TABLE selo (
        id INTEGER PRIMARY KEY,
        titulo_id INTEGER REFERENCES titulo(id),
        recibo_id INTEGER REFERENCES recibo(id),
        tipo_ato_cod VARCHAR REFERENCES tipo_ato(codigo),
        numero VARCHAR,
        aleatorio VARCHAR,
        tipo VARCHAR,
        situacao VARCHAR,
        emitido_em TIMESTAMP
    );

    CREATE TABLE andamento (
        id INTEGER PRIMARY KEY,
        titulo_id INTEGER REFERENCES titulo(id),
        apresentante_id INTEGER REFERENCES apresentante(id),
        tipo_andamento_cod VARCHAR REFERENCES tipo_andamento(codigo),
        num_devedor VARCHAR,
        ocorrido_em TIMESTAMP
    );

    -- Custas
    CREATE SEQUENCE seq_tab_custas START 1;
    CREATE TABLE tabela_custas (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_tab_custas'),
        ano VARCHAR NOT NULL,
        versao VARCHAR,
        tipo VARCHAR NOT NULL
    );

    CREATE SEQUENCE seq_faixa START 1;
    CREATE TABLE faixa_valor (
        id INTEGER PRIMARY KEY DEFAULT nextval('seq_faixa'),
        tabela_custas_id INTEGER NOT NULL REFERENCES tabela_custas(id),
        codigo VARCHAR NOT NULL,
        valor_de DOUBLE,
        valor_ate DOUBLE
    );

    CREATE TABLE custas_faixa (
        id INTEGER PRIMARY KEY,
        faixa_valor_id INTEGER NOT NULL REFERENCES faixa_valor(id),
        emol DOUBLE,
        fetj DOUBLE,
        fundperj DOUBLE,
        funperj DOUBLE,
        funarpen DOUBLE,
        ressag DOUBLE,
        funpgalerj DOUBLE,
        funpgt DOUBLE,
        fundpguerj DOUBLE,
        mutua DOUBLE,
        acoterj DOUBLE,
        iss DOUBLE,
        val_selo DOUBLE,
        total DOUBLE
    );

    CREATE TABLE custas_ato_fixo (
        id INTEGER PRIMARY KEY,
        tabela_custas_id INTEGER NOT NULL REFERENCES tabela_custas(id),
        tipo_ato_cod VARCHAR,
        tabela_tjrj VARCHAR,
        item_tjrj VARCHAR,
        subitem_tjrj VARCHAR,
        descricao VARCHAR,
        qtd_ato DOUBLE,
        emol DOUBLE,
        fetj DOUBLE,
        fundperj DOUBLE,
        funperj DOUBLE,
        funarpen DOUBLE,
        ressag DOUBLE,
        funpgalerj DOUBLE,
        funpgt DOUBLE,
        fundpguerj DOUBLE,
        mutua DOUBLE,
        acoterj DOUBLE,
        iss DOUBLE,
        total DOUBLE
    );

    -- Livros
    CREATE TABLE livro (
        id INTEGER PRIMARY KEY,
        tipo VARCHAR NOT NULL,
        numero VARCHAR,
        dt_abertura DATE,
        dt_fechamento DATE,
        num_folhas INTEGER
    );

    -- Log
    CREATE TABLE log_operacao (
        id INTEGER PRIMARY KEY,
        usuario VARCHAR,
        operacao VARCHAR,
        data TIMESTAMP,
        detalhes VARCHAR
    );
    """)
    print("  Schema created OK")
