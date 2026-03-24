# Decisões de Arquitetura — Sistema de Protesto de Títulos (Silva Jardim/RJ)

Este documento registra as decisões de arquitetura aprovadas para a rearquitetura do sistema legado de protesto de títulos do cartório de Silva Jardim/RJ. O sistema original utiliza um banco de dados com centenas de tabelas, campos redundantes, dados desnormalizados e convenções inconsistentes. As decisões abaixo orientam a migração para um modelo relacional limpo, normalizado e preparado para evolução.

---

## 1. Padrão Party Role para Pessoas

### Problema

No sistema legado, os dados de pessoas (devedores, credores, sacadores, apresentantes) estão espalhados e duplicados em diversas tabelas e campos de títulos. A mesma pessoa física ou jurídica pode aparecer repetida com dados divergentes, e não há separação entre a identidade da pessoa e o papel que ela exerce em cada título.

### Solução

Adotar o padrão **Party Role** com uma tabela base `pessoa` e tabelas de papel (role):

**Tabela `pessoa`** (identidade única):
- `id`, `nome`, `cpf_cnpj`, `tipo_documento`, `endereco`, `bairro`, `cidade`, `uf`, `cep`, `created_at`, `updated_at`

**Tabelas de papel:**
- `devedor` — `pessoa_id` FK, `falencia`, `sustacao`, `cod_irregularidade`, `oficio`, `vid_livro`
- `credor` — `pessoa_id` FK, `agencia`, `nosso_numero`
- `sacador` — `pessoa_id` FK
- `apresentante` — `pessoa_id` FK, `codigo` UK, `convenio_cra`, `remessa_cra`, `tipo_apresentacao`

A tabela `titulo` referencia `devedor_id`, `credor_id`, `sacador_id` e `apresentante_id`. A tabela `coemitente` referencia `devedor_id` (mesmo papel de devedor).

### Benefícios

- A mesma pessoa pode ser devedor em um título e credor em outro, sem duplicação de cadastro.
- Campos específicos de cada papel ficam isolados em suas respectivas tabelas, sem poluir a tabela base.
- Facilita deduplicação e atualização cadastral centralizada.

---

## 2. `titulo_cheque` como Tabela 1:1 Opcional

### Problema

A tabela de títulos do sistema legado contém campos específicos de cheque (`NUMCHEQUE`, `BCO`, `AGENCIA`, `VLRCHEQUE`, `DTCHEQUE`) que são preenchidos apenas quando `TIPODOC = 'CH'`. Dos 14.078 títulos, apenas 9 são cheques. Esses campos ficam nulos em 99,94% dos registros.

### Solução

Criar uma tabela auxiliar `titulo_cheque` com relacionamento 1:1 opcional:

**Tabela `titulo_cheque`:**
- `titulo_id` FK, `numero`, `banco`, `agencia`, `valor`, `data`

O registro só existe quando o título é do tipo cheque.

### Benefícios

- A tabela `titulo` fica limpa de campos raramente utilizados.
- O modelo explicita que dados de cheque são uma extensão opcional do título.
- Sem desperdício de armazenamento com colunas nulas.

---

## 3. `situacao` como Enum + `canal` + `sub_tipo`

### Problema

No sistema legado, a situação do título é armazenada como texto livre com valores compostos como `"CANCELADO/INTERNET/JG"`, totalizando 19 combinações distintas. Isso dificulta consultas, filtragens e relatórios, além de ser frágil a erros de digitação.

### Solução

Decompor a string em três campos tipados:

- **`situacao`** — ENUM: `APONTADO`, `PROTESTADO`, `PAGO`, `DEVOLVIDO`, `RETIRADO`, `CANCELADO`, `SUSTADO`, `SUSPENSO`
- **`canal`** — ENUM nullable: `BALCAO`, `INTERNET`, `CONVENIO`, `SERVENTIA`, `JUDICIAL`
- **`sub_tipo`** — VARCHAR nullable: `SC` (sem custas), `JG` (justiça gratuita), `DEFINITIVO`, etc.

**Exemplo de migração:**

| Legado                    | `situacao`  | `canal`    | `sub_tipo` |
|---------------------------|-------------|------------|------------|
| `CANCELADO/INTERNET/JG`  | `CANCELADO` | `INTERNET` | `JG`       |
| `PROTESTADO`             | `PROTESTADO`| `NULL`     | `NULL`     |
| `PAGO/BALCAO/SC`         | `PAGO`      | `BALCAO`   | `SC`       |

### Benefícios

- Consultas por situação, canal ou sub-tipo tornam-se simples e indexáveis.
- Enums garantem integridade referencial e impedem valores inválidos.
- Facilita geração de relatórios e dashboards com agrupamentos limpos.

---

## 4. Consolidação de ~40 Tabelas de Custas

### Problema

O cálculo de custas cartorárias está fragmentado em cerca de 40 tabelas com nomes como `fcustas`, `ccustas`, `qcustas`, `tcustas` (cada uma com variantes anuais), além de `tb_e20XX`, `tb_faixa`, `tb_f2025a`, `fc_2025`, `cc_2025`, `qc_2025`, `tc_2025`, entre outras. A lógica de negócio está dispersa e é difícil de manter, auditar ou versionar.

### Solução

Consolidar em um modelo normalizado:

**Tabela `tabela_custas`:**
- `id`, `ano`, `versao`, `vigencia_inicio`, `vigencia_fim`, `ativa`

**Tabela `faixa_valor`:**
- `id`, `tabela_custas_id` FK, `codigo` (a..s), `valor_de`, `valor_ate`

**Tabelas de custas por tipo de ato:**
- `custas_protocolizacao` — `faixa_valor_id` FK + 12 campos de distribuição
- `custas_cancelamento` — mesma estrutura
- `custas_quitacao` — mesma estrutura

**Tabela `custas_ato_fixo`:**
- `tabela_custas_id` FK, `tipo_ato_cod` FK, `tabela_tjrj`, `item_tjrj`, `subitem_tjrj`, `descricao`, `qtd_ato` + 12 campos de distribuição

**Os 12 campos de distribuição (comuns a todas as tabelas de custas):**

| Campo         | Descrição                        |
|---------------|----------------------------------|
| `emol`        | Emolumentos                      |
| `fetj`        | Fundo Especial do TJ/RJ         |
| `fundperj`    | FUNDPERJ                         |
| `funperj`     | FUNPERJ                          |
| `funarpen`    | FUNARPEN                         |
| `ressag`      | Ressarcimento                    |
| `funpgalerj`  | Fundo PGA LERJ                   |
| `funpgt`      | Fundo PGT                        |
| `fundpguerj`  | Fundo PGU ERJ                    |
| `mutua`       | Mútua                            |
| `acoterj`     | ACOTERJ                          |
| `iss`         | ISS                              |
| `val_selo`    | Valor do selo                    |
| `total`       | Total                            |

**Fluxo de cálculo:** valor do título → enquadramento em uma `faixa_valor` → consulta à tabela de custas correspondente ao tipo de ato → cada componente representa um repasse obrigatório a um fundo estadual do RJ.

### Benefícios

- ~40 tabelas consolidadas em 6, com versionamento temporal explícito.
- Nova tabela de custas para um ano é apenas um novo registro em `tabela_custas` com suas faixas.
- Auditoria e conferência de valores simplificadas.
- Lógica de cálculo de custas torna-se determinística e testável.

---

## 5. Consolidação de 200+ Tabelas TP* → `lote_cra` + `lote_cra_item`

### Problema

O sistema legado cria uma tabela nova para cada lote CRA (Central de Remessa de Arquivos) processado, com nomes no formato `TP{timestamp}` (ex: `TP093947`, `TP170034`). Existem mais de 200 dessas tabelas, todas com a mesma estrutura de 48 colunas no formato padrão de lote CRA. Isso torna impossível consultar o histórico de lotes sem queries dinâmicas e inviabiliza qualquer manutenção.

### Solução

Consolidar em duas tabelas:

**Tabela `lote_cra`:**
- `id`, `apresentante_id` FK, `arquivo_nome`, `direcao` ENUM (`REMESSA`, `RETORNO`), `processado_em`, `status`

**Tabela `lote_cra_item`:**
- `id`, `lote_id` FK, `titulo_id` FK nullable, `sequencia`, `dev_nome`, `dev_documento`, `dev_endereco`, `valor`, `dt_vencimento`, `dt_emissao`, `especie_titulo`, `cod_erros`, `tipo_informacao`

Os campos `EM_BRANCO1` a `EM_BRANCO7` são descartados. As 48 colunas originais são reduzidas a ~15 campos relevantes mais dados complementares.

### Benefícios

- 200+ tabelas consolidadas em 2.
- Consulta unificada de todo o histórico de lotes CRA.
- Relacionamento direto entre item do lote e título (quando aplicável).
- Eliminação de campos vazios e redundantes.

---

## 6. `selo` como Entidade Própria

### Problema

No sistema legado, selos de autenticidade estão espalhados por pelo menos 6 pares de campos na tabela de títulos (`SELO_APTM`, `SELOPROT`+`ALE_PROT`, `SELOCAN`+`ALE_CAN`, `SSELLO`+`ALE_SSELLO`, `SELO`+`ALE_SELO`), além de campos em `pedidos`, `intimar` e `log_selo`. Não há uma visão centralizada dos selos emitidos, e a rastreabilidade é precária.

### Solução

Criar uma entidade dedicada:

**Tabela `selo`:**
- `id`, `titulo_id` FK, `recibo_id` FK nullable, `tipo_ato_cod` FK, `numero`, `aleatorio`, `tipo` ENUM (`APONTAMENTO`, `PROTESTO`, `CANCELAMENTO`, `CERTIDAO`), `situacao`, `emitido_em`

Cada registro representa um selo emitido, com rastreabilidade completa do ato, título e momento de emissão.

### Benefícios

- Um registro por selo emitido, em vez de campos dispersos.
- Rastreabilidade completa: qual selo, para qual ato, de qual título, quando.
- Facilita auditoria e consultas ao TJ/RJ sobre selos utilizados.
- Modelo extensível para novos tipos de ato sem alterar a tabela de títulos.

---

## 7. `andamento` com Timestamp Real + `tipo_andamento`

### Problema

Na tabela `tb_andam` do sistema legado, a data e hora do andamento são armazenadas separadamente: `DATA_AND` (tipo DATE) e `HORA_AND` (tipo VARCHAR, ex: `"08:51:19"`). Além disso, os códigos de tipo de andamento são usados diretamente sem tabela de referência, dificultando a compreensão do significado de cada código.

### Solução

Unificar em um modelo limpo:

**Tabela `andamento`:**
- `id`, `titulo_id` FK, `apresentante_id` FK, `tipo_andamento_cod` FK, `num_devedor`, `ocorrido_em` TIMESTAMP

**Tabela de referência `tipo_andamento`:**
- `codigo` PK, `descricao`

Códigos de andamento: `AA`, `AB`, `AC`, `AD`, `AE`, `AF`, `AG`, `AI`, `AJ`, `AK`.

### Benefícios

- Data e hora unificadas em um único campo TIMESTAMP, eliminando a necessidade de concatenação e parsing.
- Tabela de referência `tipo_andamento` torna o modelo autodocumentado.
- Consultas temporais (ordenação, filtragem por período) tornam-se triviais.

---

## Entidades do Novo Modelo

Abaixo, a lista completa de entidades resultantes das decisões aprovadas:

### Cadastro de Pessoas (Party Role)
| Entidade        | Descrição                                      |
|-----------------|-------------------------------------------------|
| `pessoa`        | Cadastro base de pessoa física ou jurídica      |
| `devedor`       | Papel de devedor (vinculado a pessoa)           |
| `credor`        | Papel de credor (vinculado a pessoa)            |
| `sacador`       | Papel de sacador (vinculado a pessoa)           |
| `apresentante`  | Papel de apresentante (vinculado a pessoa)      |

### Títulos e Extensões
| Entidade         | Descrição                                      |
|------------------|-------------------------------------------------|
| `titulo`         | Título protestado, com FK para devedor, credor, sacador e apresentante |
| `titulo_cheque`  | Extensão 1:1 opcional para títulos do tipo cheque |
| `coemitente`     | Coemitentes do título (referencia devedor)      |

### Custas e Faixas de Valor
| Entidade                  | Descrição                                    |
|---------------------------|----------------------------------------------|
| `tabela_custas`           | Tabela de custas por ano/versão com vigência |
| `faixa_valor`             | Faixas de valor vinculadas a uma tabela      |
| `custas_protocolizacao`   | Custas de protocolização por faixa           |
| `custas_cancelamento`     | Custas de cancelamento por faixa             |
| `custas_quitacao`         | Custas de quitação por faixa                 |
| `custas_ato_fixo`         | Custas de atos fixos por tabela              |

### Lotes CRA
| Entidade        | Descrição                                      |
|-----------------|-------------------------------------------------|
| `lote_cra`      | Lote de remessa/retorno CRA                    |
| `lote_cra_item` | Item individual de um lote CRA                 |

### Selos
| Entidade | Descrição                                         |
|----------|---------------------------------------------------|
| `selo`   | Selo de autenticidade emitido por ato             |

### Andamentos
| Entidade          | Descrição                                    |
|-------------------|----------------------------------------------|
| `andamento`       | Registro de andamento de um título           |
| `tipo_andamento`  | Tabela de referência dos códigos de andamento|

### Referência de Atos
| Entidade       | Descrição                                       |
|----------------|-------------------------------------------------|
| `tipo_ato`     | Tabela de referência dos tipos de ato (usado em custas e selos) |

---

*Documento gerado em março de 2026. Todas as decisões foram aprovadas para o projeto de rearquitetura do sistema de protesto de Silva Jardim/RJ.*
