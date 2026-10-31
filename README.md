# soliLang

Linguagem e processador para controle de doações: registrar entradas,
consultar estoque, distribuir itens e emitir relatórios.

Projeto acadêmico do Tema Integrador VIII — Projeto de Linguagens.

## Problema

Instituições comunitárias e ONGs que recebem e redistribuem doações
frequentemente controlam o estoque em cadernos ou planilhas manuais. Isso
gera perda de itens, distribuição desigual e falta de transparência.

A soliLang permite registrar as movimentações em uma linguagem simples, com
mensagens de erro claras e estoque sempre consistente.

## Relação com os ODS

- **ODS 10 — Redução das Desigualdades.** A instituição atende pessoas em
  situação de vulnerabilidade e distribui bens doados. Sem controle de
  estoque, itens se perdem, a distribuição fica desigual e não há registro
  do que entrou e do que saiu.
  - **Meta 10.2** (inclusão social de pessoas em vulnerabilidade): o
    registro confiável amplia o alcance real das doações.
  - **Meta 10.3** (igualdade de oportunidades e remoção de barreiras): a
    linguagem substitui o controle manual, que depende de memória e papel,
    por um registro verificável.
- **ODS 4 (meta 4.5) — alinhamento secundário.** A linguagem também serve
  para controlar itens de uso escolar (caderno, lápis, mochila, uniforme)
  quando a instituição os distribui. Com o estoque sob controle, a entrega
  de material didático não é interrompida por falta de itens, o que ajuda a
  reduzir disparidades de acesso.

## Etapas do processamento

```
arquivo .soli -> Lexer -> Parser -> Análise semântica -> Interpretador
```

O projeto **não gera código de máquina**: é um processador de linguagem com
um interpretador.

## Front-end e back-end

O processador está dividido em duas fases:

| Fase | Módulo | Entrada | Saída | Erro |
|---|---|---|---|---|
| Léxica | `solilang/lexer.py` | texto | tokens | `ErroLexico` |
| Sintática | `solilang/parser.py` | tokens | AST | `ErroSintatico` |
| Semântica | `solilang/semantic.py` | AST | AST validada | `ErroSemantico` |
| Síntese | `solilang/interpreter.py` | AST | saída | — |

**Front-end** = análise (léxica + sintática + semântica). É a parte do
processador que **entende** o programa e é independente do alvo: poderia
alimentar tanto um interpretador quanto um gerador de código.

**Back-end** = síntese. Neste projeto é um **interpretador de árvore**: ele
percorre a AST já validada e executa as instruções, sem produzir artefato.

O `main.py` é o driver do front-end e serve como testador das fases:

```bash
python3 main.py --tokens examples/exemplo.soli   # revela a fase léxica
python3 main.py --ast examples/exemplo.soli      # revela a fase sintática
```

A geração de código não faz parte do escopo; é apontada como trabalho futuro
e entraria exatamente na saída do front-end (a AST), no lugar do
interpretador.

## Como executar

Requisito: Python 3.10 ou superior. Nenhuma dependência externa.

```bash
python3 main.py examples/exemplo.soli
```

Saída:

```
Consulta ARROZ: 50 unidades
Consulta ARROZ: 40 unidades

------------ Estoque atual ------------
ARROZ: 40 unidades
```

Outros modos (úteis para inspecionar as etapas):

```bash
python3 main.py --tokens examples/exemplo.soli   # lista de tokens
python3 main.py --ast examples/exemplo.soli      # árvore sintática
```

Sem argumentos, o programa exibe o modo de uso:

```bash
python3 main.py
```

### Persistência do estoque

Sem a flag, o estoque vive só em memória e começa vazio. Com `--estoque`, o
programa lê o arquivo antes de executar e grava o resultado depois:

```bash
python3 main.py --estoque examples/exemplo.soli
```

O arquivo padrão é `estoque_atual.json`, criado na pasta do projeto. Para usar
outro caminho, informe com `=`:

```bash
python3 main.py --estoque=dados.json examples/exemplo.soli
```

O arquivo é JSON puro e legível:

```json
{
  "ARROZ": 40
}
```

Comportamento:

- **Arquivo inexistente** = estoque vazio (a primeira execução não é erro).
- **Só grava se o programa for válido.** Havendo erro léxico, sintático ou
  semântico, o arquivo não é tocado.
- **Gravação atômica**: escreve em `estoque_atual.json.tmp` e renomeia no final, então
  uma interrupção no meio não corrompe o estoque.
- **Acumula entre execuções**: uma `DOACAO` de 50 num estoque de 40 resulta em
  90 na execução seguinte.
- **Fora do Git**: `estoque_atual.json` está no `.gitignore` — é dado da
  instituição, não código.

Não há SGBD. A persistência em arquivo cobre o caso de uso da instituição sem
trazer a complexidade de banco de dados para dentro do escopo da linguagem.

## A linguagem

| Comando | Forma | Efeito |
|---|---|---|
| `INICIO` | `INICIO` | abre o programa |
| `FIM` | `FIM` | fecha o programa |
| `DOACAO` | `DOACAO ITEM, QTD;` | soma unidades (cria o item se não existir) |
| `CONSULTA` | `CONSULTA ITEM;` | mostra o saldo (erro se o item não existir) |
| `DISTRIBUIR` | `DISTRIBUIR ITEM, QTD;` | subtrai unidades (erro se faltar saldo) |
| `RELATORIO` | `RELATORIO;` | mostra o estoque completo |

### Gramática (BNF)

```bnf
<programa>      ::= INICIO <instrucoes> FIM
<instrucoes>    ::= <instrucao> <instrucoes> | ε
<instrucao>     ::= <doacao> | <consulta> | <distribuicao> | <relatorio>
<doacao>        ::= DOACAO ID , NUM ;
<consulta>      ::= CONSULTA ID ;
<distribuicao>  ::= DISTRIBUIR ID , NUM ;
<relatorio>     ::= RELATORIO ;
ID              ::= [A-Z][A-Z0-9_]*
NUM             ::= [0-9]+
```

### Tokens e expressões regulares

| Token | Expressão | Exemplos |
|---|---|---|
| `ID` | `[A-Z][A-Z0-9_]*` | `ARROZ`, `FEIJAO_2`, `ITEM7` |
| `NUM` | `[0-9]+` | `1`, `50`, `2026` |
| `VIRGULA` | `,` | `,` |
| `PONTO_VIRGULA` | `;` | `;` |
| espaços | `[ \t\r\n]+` | ignorados |

### Autômato finito do identificador

```
        [A-Z]              [A-Z] / [0-9] / _
(q0) -----------> ((q1)) ---------------------> ((q1))
inicial           aceitação                     laço
```

O estado inicial só avança ao receber uma letra maiúscula; a partir daí o
autômato permanece em um estado de aceitação enquanto recebe letras
maiúsculas, dígitos ou sublinhado. Qualquer outro símbolo encerra o
reconhecimento — se for um caractere inválido fora desse padrão, o lexer
reporta erro léxico com a linha.

### Expressão EBNF equivalente

```ebnf
programa    = "INICIO" , { instrucao } , "FIM" ;
instrucao   = doacao | consulta | distribuicao | relatorio ;
doacao      = "DOACAO" , identificador , "," , numero , ";" ;
consulta    = "CONSULTA" , identificador , ";" ;
distribuicao= "DISTRIBUIR" , identificador , "," , numero , ";" ;
relatorio   = "RELATORIO" , ";" ;
identificador = letra_maiuscula , { letra_maiuscula | digito | "_" } ;
numero      = digito , { digito } ;
```

## Regras semânticas

1. Quantidades devem ser maiores que zero.
2. `DOACAO` cria o item automaticamente.
3. `CONSULTA` e `DISTRIBUIR` exigem item existente.
4. Não é permitido distribuir mais do que o saldo.
5. O programa inteiro é validado antes da execução: se houver erro, nada é
   aplicado ao estoque.

A validação roda sobre uma cópia do estoque. Assim, ou o programa inteiro é
válido e executa, ou nada executa — não existe estado parcial.

## Decisões de projeto

| # | Decisão | Escolha |
|---|---|---|
| 1 | Extensão dos fontes | `.soli` |
| 2 | Identificador | `[A-Z][A-Z0-9_]*` — só maiúsculas |
| 3 | Quantidade | inteiro positivo, validado `> 0` na semântica |
| 4 | `DOACAO` de item novo | cria o item automaticamente |
| 5 | `CONSULTA` de item inexistente | erro semântico com a linha |
| 6 | Programa vazio (`INICIO FIM`) | aceito (produção ε) |
| 7 | Erro no meio do programa | erro semântico; nada é executado |
| 8 | Saída | `DOACAO`/`DISTRIBUIR` silenciosos; `CONSULTA` e `RELATORIO` imprimem |
| 9 | Estoque | dicionário em memória; persistência opcional em JSON via `--estoque` |
| 10 | Comentários na linguagem | não existem (escopo mínimo) |

## Estrutura do projeto

```
main.py                 driver do front-end, modos de inspeção e persistência
solilang/tokens.py      [front-end] tipos de token e palavras reservadas
solilang/errors.py      [front-end] erros com número de linha
solilang/lexer.py       [front-end] texto -> tokens
solilang/ast_nodes.py   [front-end] nós da árvore sintática
solilang/parser.py      [front-end] tokens -> AST (descendente recursivo)
solilang/semantic.py    [front-end] regras de negócio
solilang/interpreter.py [back-end]  execução e saída
examples/               programas de exemplo (válidos e inválidos)
tests/                  testes automatizados com unittest
```

## Testes

```bash
python3 -m unittest discover -v
```

São 38 testes: 7 de lexer, 9 de parser, 9 de semântica, 4 de integração e 9
de persistência em arquivo.

## Exemplos de erro

| Arquivo | Erro |
|---|---|
| `examples/erro_lexico.soli` | `Erro léxico na linha 2: identificador inválido começando com 'a'; use letra maiúscula (ex.: ARROZ)` |
| `examples/erro_sintatico.soli` | `Erro sintático na linha 2: esperado ',' após o identificador, mas encontrado '50' (NUM)` |
| `examples/erro_semantico.soli` | `Erro semântico na linha 3: estoque insuficiente para ARROZ: solicitado 10, disponível 4` |

Rode qualquer um deles para ver a mensagem completa:

```bash
python3 main.py examples/erro_semantico.soli
```

## Limitações

- Sem SGBD: a persistência é um arquivo JSON opcional (`--estoque`), não um
  banco de dados relacional.
- Sem funções, laços, variáveis ou comentários na linguagem.
- Sem interface gráfica, autenticação ou controle de usuários.
- A linguagem é de domínio específico para gestão de doações; não é uma
  linguagem de Comunicação Alternativa e Aumentativa (CAA).

## Uso de IA generativa

O apoio de IA foi usado na organização do material, na revisão de mensagens
de erro e na explicação dos conceitos de análise léxica, sintática e
semântica. Os integrantes leram, executaram e explicaram cada módulo, e a
suíte de testes é executada localmente antes de cada commit.

A pesquisa de campo é realizada diretamente com a instituição parceira e não
é gerada por IA.

O registro completo — ferramenta, plano, modelo, prompts e evidências — está
em [`USO_DE_IA.md`](/docs/ia/USO_DE_IA.md).
