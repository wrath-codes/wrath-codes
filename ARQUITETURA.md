# Arquitetura do Sistema de Protesto — Silva Jardim/RJ

> Documentação técnica do sistema legado de protesto de títulos,
> construído em Harbour/xBase, utilizado pelo Tabelionato de Protesto de Silva Jardim — RJ.

---

## Visão Geral

O sistema gerencia o ciclo completo de **protesto de títulos**, desde o apontamento
até o cancelamento, incluindo:

- Recepção e apontamento de títulos
- Intimação de devedores
- Lavratura de protesto
- Emissão de certidões e recibos
- Cálculo de custas e emolumentos
- Integração com CRA (Central de Remessa de Arquivos)
- Comunicação com Serasa
- Controle de selos e livros

**Números do banco de dados:**

| Métrica | Valor |
|---|---|
| Total de tabelas (DBF) | 363 |
| Tabelas com dados | 260 |
| Tabelas vazias | 103 |
| Período de dados | 2013 — 2026 |
| Total de títulos | 14.078 |

---

## Tabela Central: `TITULOS`

A tabela `titulos` é o **coração do sistema** — todas as demais tabelas se relacionam
a ela através do campo `PROTOCOLO` (chave primária, formato `0000001`).

### Campos Principais

| Campo | Tipo | Descrição |
|---|---|---|
| `PROTOCOLO` | VARCHAR | **PK** — Número sequencial do protocolo |
| `SACADO` | VARCHAR | Nome do devedor |
| `CPF` / `CGC` | VARCHAR | Documento do devedor (PF/PJ) |
| `ENDER`, `BAIRRO`, `CID`, `EST`, `CEP` | VARCHAR | Endereço do devedor |
| `CODBANCO` | VARCHAR | **FK → bancos** — Código do apresentante |
| `CEDENTE` | VARCHAR | Nome do credor/cedente |
| `SACADOR` | VARCHAR | Sacador/avalista |
| `TIPODOC` | VARCHAR | **FK → tbtiptit.SIGLA** — Espécie do título |
| `NUMDOC` | VARCHAR | Número do documento |
| `VALORDOC` | DOUBLE | Valor do documento |
| `VALORTIT` | DOUBLE | Valor do título |
| `CUSTAS` | DOUBLE | Valor das custas |
| `EMISSAO` | DATE | Data de emissão |
| `VENCIMENTO` | DATE | Data de vencimento |
| `DTENTRADA` | DATE | Data de entrada/apontamento |
| `DTINTIMA` | DATE | Data da intimação |
| `DTPROTESTO` | DATE | Data do protesto |
| `DTPAGTO` | DATE | Data do pagamento |
| `SITUACAO` | VARCHAR | Status atual do título |
| `MEIOINTIMA` | VARCHAR | Meio de intimação (I.PESSOAL, EDITAL, etc.) |
| `LIVRO` / `FOLHAS` | VARCHAR/DOUBLE | Registro no livro de protesto |
| `LIVAPT` / `FOLAPT` | VARCHAR | Registro no livro de apontamento |
| `SELO_APTM`, `SELOPROT`, `SELOCAN` | VARCHAR | Números dos selos |
| `ARQREMESSA` / `ARQRETORNO` | VARCHAR | Arquivos CRA |
| `ANO_TAB` | VARCHAR | Ano da tabela de custas aplicada |

### Ciclo de Vida do Título (SITUACAO)

```
APONTADO (77)
   │
   ├──→ PROTESTADO (7.445)    ──→ CANCELADO (965)
   │                               CANCELADO/INTERNET (110)
   │                               CANCELADO/CONVENIO (66)
   │                               CANCELADO/JG (13)
   │                               CANCELADO/SC (4)
   │                               CANCELADO/INTERNET/SC (10)
   │                               CANCELADO/INTERNET/JG (2)
   │
   ├──→ PAGO (3.603)
   │
   ├──→ DEVOLVIDO (1.192)
   │
   ├──→ RETIRADO/INTERNET (536)
   │    RETIRADO (28)
   │    RETIRADO/SERVENTIA (17)
   │
   └──→ SUSTADO (4)
        SUSTADO/DEFINITIVO (2)
        SUSPENSO (1)
        SUSP. EFEITOS (2)
```

---

## Relacionamentos Confirmados

```
titulos (PROTOCOLO) ─┬──→ coemit        (448 co-emitentes)
                     ├──→ edital         (3.602 editais)
                     ├──→ pedidos        (2.906 pedidos de certidão)
                     ├──→ recibos        (7.924 recibos)
                     ├──→ tb_andam       (18.853 andamentos)
                     ├──→ log_selo       (27.733 registros de selo)
                     ├──→ comunica       (309 comunicações)
                     └──→ intimar        (intimações)

titulos.CODBANCO    ──→ bancos.CODBANCO       (98% match — 248 apresentantes)
titulos.TIPODOC     ──→ tbtiptit.SIGLA        (99% match — 63 espécies)
pedidos.CODFUNCAO   ──→ tfuncao.CODFUNCAO     (99.9% match)
recibos.CODFUNCAO   ──→ tfuncao.CODFUNCAO
pedidos.CODREC      ──→ recibos.CODREC
```

---

## Tabelas de Domínio

### `bancos` — Apresentantes/Portadores (248 registros)

Não são apenas bancos — incluem órgãos públicos e concessionárias:

| Campo | Descrição |
|---|---|
| `CODBANCO` | **PK** — Código do apresentante |
| `NOMEBANCO` | Nome |
| `CGCBANCO` | CNPJ |
| `CONVENIO` | Código de convênio CRA |
| `REMCRA` | Flag de remessa via CRA |
| `TIPO_APR` | Tipo de apresentação |

**Principais apresentantes:**

| Código | Nome | Títulos |
|---|---|---|
| 582 | Procuradoria-Geral da Fazenda | 1.982 |
| IT4 | Município de Silva Jardim | 1.932 |
| 341 | BCO Itaú S.A. | 1.783 |
| 237 | BCO Bradesco S/A | 1.690 |
| 901 | AMPLA (energia) | 1.210 |
| 001 | Banco do Brasil S/A | 993 |
| 911 | Procuradoria Geral do Estado RJ | 754 |
| A64 | TJRJ | 657 |

### `tbtiptit` — Espécies de Título (63 registros)

| Sigla | Descrição | Qtd Títulos |
|---|---|---|
| DMI | Duplicata Mercantil por Indicação | 7.481 |
| CDA | Certidão da Dívida Ativa | 5.040 |
| CDT | Certidão de Crédito do Tribunal | 659 |
| DSI | Duplicata de Serviços por Indicação | 442 |
| CBI | Cédula de Crédito Bancário por Indicação | 180 |
| NP | Nota Promissória | 29 |
| CH | Cheque | 9 |

### `tfuncao` — Funções/Atos (29 registros)

| Código | Função |
|---|---|
| 01 | Protocolização de Títulos |
| 02 | Certidão de Protestos 5 anos |
| 03 | Certidão de Protestos 10 anos |
| 04 | Cancelamento de Títulos |
| 05 | Certidão de Inteiro Teor 5 anos |
| 06 | Certidão de Inteiro Teor 10 anos |
| 07 | Certidão Especial de Cadastro |
| 08 | Guia Bancária |
| 09 | Certidão do Ato de Cancelamento |
| 12 | Retirada de Título (Desistência) |
| 17 | Reconhecimento de Firma |
| 20 | Certidão de Protestos 20 anos |
| 99 | Baixa de Títulos/Diversos |

### `tb_irreg` — Códigos de Irregularidade (65 registros)

Motivos de devolução/irregularidade dos títulos:

| Código | Descrição |
|---|---|
| 01 | Data da apresentação inferior à data de vencimento |
| 03 | Nome do sacado incompleto/incorreto |
| 06 | Endereço do sacado insuficiente |
| 07 | CNPJ/CPF do sacado inválido/incorreto |
| 14 | CEP incorreto |
| 16 | Falta número do título |

---

## Tabelas Operacionais

### `coemit` — Co-emitentes (448 registros)

Co-obrigados/avalistas vinculados a um título.

| Campo | Descrição |
|---|---|
| `PROTOCOLO` | **FK → titulos** |
| `COEMITENTE` | Nome do co-emitente |
| `CPFCOEMIT` / `CGCCOEMIT` | Documento |
| `ENDCOEMIT`, `BAIRCOEMIT`, etc. | Endereço |
| `DTINTIMA` | Data de intimação do co-emitente |
| `MEIOINTIMA` | Meio de intimação |

### `edital` — Editais (3.602 registros)

Publicações de edital para intimação de devedores não encontrados.

| Campo | Descrição |
|---|---|
| `DTEDIT` | Data do edital |
| `PROTOCOLO` | **FK → titulos** |
| `TIPO` | Tipo de publicação |
| `NNOMME` | Nome publicado |
| `CODMOT` / `MOTIVO` | Código e descrição do motivo |
| `LIV_EDT` / `FOL_EDT` | Livro e folha do edital |

### `pedidos` — Pedidos de Certidão (2.906 registros)

Solicitações de certidões e outros serviços.

| Campo | Descrição |
|---|---|
| `CODOPE` | Código da operação |
| `CODREC` | **FK → recibos** — Código do recibo |
| `PROTOCOLO` | **FK → titulos** |
| `CODFUNCAO` | **FK → tfuncao** — Tipo de serviço |
| `DATPED` | Data do pedido |
| `NNOMME` | Nome pesquisado |
| `CPFCGC` | Documento pesquisado |
| `RESULTADO` | Resultado da pesquisa |
| `SSELLO` / `ALE_SSELLO` | Selo e aleatório |

### `recibos` — Recibos (7.924 registros)

Recibos de custas e emolumentos.

| Campo | Descrição |
|---|---|
| `CODREC` | **PK** — Código do recibo |
| `PROTOCOLO` | **FK → titulos** |
| `CODFUNCAO` | **FK → tfuncao** |
| `DATREC` | Data do recibo |
| `EMOL` | Emolumentos |
| `FETJ` | FETJ |
| `FUNDPERJ` | FUNDPERJ |
| `FUNPERJ` | FUNPERJ |
| `FUNARPEN` | FUNARPEN |
| `RESSAG` | Ressarcimento SAG |
| `FUNPGALERJ` | FUNPGALERJ |
| `FUNPGT` | FUNPGT |
| `FUNDPGUERJ` | FUNDPGUERJ |
| `MUTUA` | Mutualidade |
| `ACOTERJ` | ACOTERJ |
| `ISS` | ISS |
| `TXGUIA` | Taxa de guia |
| `VALTOT` | **Valor total** |

### `tb_andam` — Andamentos (18.853 registros)

Registro de movimentações/eventos dos títulos no CRA.

| Campo | Descrição |
|---|---|
| `DATA_AND` | Data do andamento |
| `HORA_AND` | Hora |
| `CODBANCO` | **FK → bancos** |
| `PROTOCOLO` | **FK → titulos** |
| `CODDEVIRR` | Código do evento |
| `NUMDEVED` | Número do devedor |

**Códigos de andamento (CODDEVIRR):**

| Código | Qtd | Significado provável |
|---|---|---|
| AB | 7.290 | Apontamento/Baixa |
| AA | 5.990 | Apontamento/Aceite |
| AE | 2.142 | Apontamento/Edital |
| AK | 1.395 | Apontamento/Cancelamento |
| AG | 916 | Apontamento/Guia |
| AC | 546 | Apontamento/Confirmação |

### `log_selo` — Log de Selos (27.733 registros)

Controle de selos de autenticidade (obrigatórios no RJ).

| Campo | Descrição |
|---|---|
| `PROTOCOLO` | **FK → titulos** |
| `CODFUNCAO` | **FK → tfuncao** |
| `CODREC` | **FK → recibos** |
| `TIPO` | Tipo do selo |
| `SITUACAO` | Status |
| `DATA` | Data de emissão |

### `logop` — Log de Operações (19.942 registros)

Auditoria de operações realizadas pelos usuários no sistema.

---

## Tabelas de Custas e Emolumentos

O sistema possui um conjunto extenso de tabelas de custas, versionadas por ano:

### Estrutura de Faixas

| Tabela | Descrição | Registros |
|---|---|---|
| `tb_faixa` / `tb_f2025a` | Faixas de valor (DE/ATE) com custas | 19 |
| `fcustas` / `fc_2025` | Faixas + custas detalhadas | 419 / 19 |
| `ccustas` / `cc_2025` | Custas de cancelamento | 133 / 19 |
| `qcustas` / `qc_2025` | Custas de quitação | 133 / 19 |
| `tcustas` / `tc_2025` | Custas por tipo de função | 521 / 35 |

### Estrutura de Emolumentos por Ano

| Tabela | Ano | Registros |
|---|---|---|
| `tb_emol` | Atual | 96 |
| `tb_e2026` | 2026 | 96 |
| `tb_e2025a` | 2025 | 96 |
| `tb_e2024` / `tb_e2024a` | 2024 | 96 |
| `tb_e2023` | 2023 | 38 |
| `tb_e2021` | 2021 | 36 |
| `tb_e2020` | 2020 | 36 |

### Composição das Custas (campos comuns)

Cada recibo/tabela de custas detalha a distribuição:

| Campo | Descrição |
|---|---|
| `EMOL` | Emolumentos (receita da serventia) |
| `FETJ` | Fundo Especial do Tribunal de Justiça |
| `FUNDPERJ` | Fundo Especial do Poder Judiciário |
| `FUNPERJ` | Fundo Penitenciário |
| `FUNARPEN` | Fundo da Assoc. de Registradores |
| `RESSAG` | Ressarcimento SAG |
| `FUNPGALERJ` | Fundo PG ALERJ |
| `FUNPGT` | Fundo PG Trabalho |
| `FUNDPGUERJ` | Fundo PGU ERJ |
| `MUTUA` | Mutualidade |
| `ACOTERJ` | ACOTERJ |
| `ISS` | Imposto sobre Serviços |
| `TOT_CUSTA` | Total |

---

## Tabelas de Controle

### `livros` / `livpro` / `livapt` / `livenc` — Livros

Controle dos livros obrigatórios:
- **livapt** — Livro de Apontamento (28 registros)
- **livpro** — Livro de Protesto (123 registros)
- **livenc** — Livro de Encerramento (30 registros)

### `feriados` — Feriados (49 registros)

Calendário de feriados para cálculo de prazos.

### `usuarios` — Usuários (5 registros)

Controle de acesso ao sistema.

### `acesso` — Permissões (56 registros)

Permissões por rotina e nível de acesso.

### `setcart` / `setmage` — Configuração da Serventia

Configurações gerais do cartório: dados cadastrais, paths, selos, etc.
Tabela de 1 registro com ~84 colunas de configuração.

### `codigos` — Identificação do Cartório (1 registro)

| Campo | Descrição |
|---|---|
| `MUNICIPIO` | Código IBGE do município |
| `CODIGOCRA` | Código no CRA |
| `ULTARQUIVO` | Último arquivo processado |

---

## Tabelas TP* — Lotes CRA (200+ tabelas)

As tabelas com prefixo `TP` (ex: `tp093947`, `tp170034`) são **snapshots de lotes
processados via CRA** (Central de Remessa de Arquivos). Possuem 48 colunas no formato
padronizado CRA com campos como:

- `DEV_NOME`, `DEV_DOCBAS`, `DEV_ENDERE` — Dados do devedor
- `NM_SACADOR`, `NUMBASESAC` — Dados do sacador
- `VALOR_PROT`, `DT_VENCMTO`, `DT_EMISSAO` — Dados do título
- `DATA_PROT`, `N_CARTORIO`, `SEQUENCIA` — Dados do protesto
- `COD_ERROS` — Códigos de erro de processamento
- `TIPOINF`, `TIPO_PROT`, `ESP_PROT` — Classificações

São arquivos de troca entre a serventia e os apresentantes (bancos).

---

## Integrações Externas

### CRA — Central de Remessa de Arquivos

Diretório `CRA/` com subpastas:
- `REMESSA/` — Arquivos enviados aos apresentantes
- `RETORNO/` — Arquivos recebidos dos apresentantes
- `CONFIRMACAO/` — Confirmações de processamento
- `BAIXADOS/` — Títulos baixados

### Serasa

Diretório `SERASA/` com 35 arquivos TXT de comunicação de protestos.

### Edital Eletrônico

Diretório `TMP/` com ~230 XMLs de editais eletrônicos (`Edital_eletronico_3305604_*.XML`),
código IBGE 3305604 = Silva Jardim.

---

## Diagrama de Relacionamentos

```
                        ┌─────────────┐
                        │   bancos    │
                        │  (248 reg)  │
                        └──────┬──────┘
                               │ CODBANCO
                               │
┌──────────┐           ┌───────┴───────┐           ┌───────────┐
│ tbtiptit │──SIGLA───→│   TITULOS     │←─PROTOCOLO─│  coemit   │
│ (63 esp) │  TIPODOC  │  (14.078 reg) │            │ (448 reg) │
└──────────┘           └───────┬───────┘            └───────────┘
                               │ PROTOCOLO
                    ┌──────────┼──────────┬──────────┐
                    ▼          ▼          ▼          ▼
              ┌──────────┐┌────────┐┌─────────┐┌──────────┐
              │  edital   ││pedidos ││ recibos ││ tb_andam │
              │(3.602 reg)││(2.906) ││ (7.924) ││ (18.853) │
              └──────────┘└───┬────┘└────┬────┘└──────────┘
                              │          │
                              │ CODFUNCAO│ CODFUNCAO
                              ▼          ▼
                        ┌─────────────┐
                        │  tfuncao    │
                        │  (29 atos)  │
                        └─────────────┘
```
