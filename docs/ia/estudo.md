# Sessão de estudo — perguntas do grupo

Perguntas feitas pelos integrantes para entender o próprio projeto, com as
respostas e o ponto exato do código onde cada uma pode ser conferida.

- **Ferramenta:** OpenCode v2.0.29 no terminal · plano OpenCode Go · modelo
  DeepSeek V4.1 Flash

> Leia cada resposta com o arquivo aberto ao lado e rode o comando indicado.

## 1. oq é lexer, parser e ast? e como cada um se encaixa no processamento de um .soli?

**Resposta:**

São três etapas encadeadas, e cada uma entrega um produto para a próxima.

- **Lexer** (analisador léxico): lê o texto **caractere por caractere** e
  agrupa em tokens. Cada token guarda tipo, valor, linha e coluna. Ele não
  sabe gramática nem estoque — só reconhece padrões.
- **Parser** (analisador sintático): recebe a lista de tokens e verifica se
  ela segue a gramática. Se seguir, monta a **AST** — objetos Python com
  significado (`Doacao(item="ARROZ", quantidade=50, linha=2)`).
- **AST** (árvore sintática abstrata): é a representação do programa depois
  de entendido. Aqui ela é "rasa": um `Programa` com uma lista de instruções,
  porque a gramática não tem aninhamento (não há `if` dentro de `if`).

O encaixe está em `main.py:39` (`compilar`): texto → `Lexer.tokenizar()` →
`Parser.analisar()` → `validar()` → AST pronta para o interpretador.

**Onde conferir no código:** `solilang/lexer.py:24` (`tokenizar`),
`solilang/tokens.py:34` (classe `Token`), `solilang/parser.py:41`
(`analisar`), `solilang/ast_nodes.py:11-47` (nós da AST), `main.py:39-45`.

---

## 2. me explica detalhadamente como funciona o .soli (do arquivo até a saída)

**Resposta:**

Pegue `examples/exemplo.soli`:

```
INICIO
    DOACAO ARROZ, 50;
    CONSULTA ARROZ;
    DISTRIBUIR ARROZ, 10;
    CONSULTA ARROZ;
    RELATORIO;
FIM
```

1. `main()` (`main.py:63`) lê o caminho do arquivo em `sys.argv`.
2. `ler_arquivo` (`main.py:33`) abre em UTF-8 e devolve o texto inteiro.
3. `Lexer.tokenizar` (`lexer.py:24`) percorre o texto e produz 21 tokens,
   terminando com `EOF`. Cada token sabe sua linha e coluna.
4. `Parser.analisar` (`parser.py:41`) consome `INICIO`, e no `while`
   (`parser.py:46`) chama `_instrucao()` cinco vezes. Cada método
   (`_doacao`, `_consulta`, `_distribuicao`, `_relatorio`) consome os tokens
   esperados e devolve o nó correspondente. Fecha em `FIM` e exige `EOF`.
5. `validar` (`semantic.py:19`) percorre a AST sobre uma **cópia** do estoque:
   confere quantidade > 0, item existente e saldo suficiente.
6. `Interpretador.executar` (`interpreter.py:19`) percorre a AST de novo,
   agora mutando o dicionário real: soma na `DOACAO`, subtrai na
   `DISTRIBUIR`, imprime na `CONSULTA` e no `RELATORIO`.

Saída:

```
Consulta ARROZ: 50 unidades
Consulta ARROZ: 40 unidades

------------ Estoque atual ------------
ARROZ: 40 unidades
```

Para ver as etapas separadas: `python3 main.py --tokens examples/exemplo.soli`
e `python3 main.py --ast examples/exemplo.soli`.

**Onde conferir no código:** `main.py:63-90`, `solilang/lexer.py:24`,
`solilang/parser.py:41`, `solilang/semantic.py:19`,
`solilang/interpreter.py:19`.

---

## 3. o interpretador funciona como uma forma de compilador? e oq seria o back-end no meu caso?

**Resposta:**

Não. Compilador **produz um artefato** (código de máquina, bytecode ou outra
linguagem). O interpretador **executa na hora** e não deixa arquivo de saída.

A divisão correta do seu projeto:

- **Front-end** = análise: `lexer` + `parser` + `semantic`. Entende o
  programa e é independente do alvo.
- **Back-end** = síntese: `interpreter.py`, que percorre a AST e executa.

Se você quisesse um compilador de verdade, o back-end seria um `codegen.py`
que traduz a AST para código Python e grava um arquivo `.py`. O front-end não
mudaria em nada — é exatamente por isso que a separação existe.

Detalhe honesto: a função `compilar` em `main.py:39` tem esse nome, mas só
analisa e valida; ela não gera código. O nome é herdado do vocabulário do
projeto e vale explicar isso na apresentação.

**Onde conferir no código:** `solilang/interpreter.py:19`,
`main.py:39-45`, `solilang/semantic.py:19`.

---

## 4. oq é uma gramática livre de contexto? e pq a bnf já basta pra solilang?

**Resposta:**

Gramática livre de contexto é um conjunto de regras em que **cada regra
reescreve um único símbolo não terminal**, sem depender do que está em volta.
É o que permite escrever a gramática como BNF e implementá-la com um parser
descendente recursivo.

Exemplo da sua linguagem: `DOACAO ARROZ, 50;` é válida em qualquer lugar
dentro de `INICIO ... FIM`, independentemente do que veio antes. Isso é ser
"livre de contexto".

BNF basta porque a soliLang:

- não tem tipos nem declaração de variáveis (isso exigiria regras
  sensíveis ao contexto);
- tem apenas 6 comandos e nenhum aninhamento;
- tem regras que se distinguem pelo primeiro token (é LL(1)).

**Onde conferir no código:** a gramática está na docstring de
`solilang/parser.py:1-20` e no `README.md` (seções "Gramática (BNF)" e
"Expressão EBNF equivalente").

---

## 5. pq recursão à esquerda quebra o parser descendente recursivo? como q vc resolveu isso no meu caso?

**Resposta:**

Recursão à esquerda é uma regra que se chama antes de consumir qualquer
token, por exemplo:

```
<instrucoes> ::= <instrucoes> <instrucao> | ε
```

Num parser descendente recursivo, `_instrucoes()` chamaria `_instrucoes()` na
**mesma posição** da entrada, sem avançar. O resultado é recursão infinita
(na prática, `RecursionError`).

Sua gramática evita isso de duas formas:

1. A regra é **recursiva à direita**
   (`<instrucoes> ::= <instrucao> <instrucoes> | ε`), que é segura para
   descida recursiva.
2. Na implementação, a repetição virou um **laço** `while`
   (`parser.py:45-52`), não uma chamada recursiva. Assim o parser não cresce
   a pilha proporcionalmente ao número de instruções.

Se a gramática tivesse que ser escrita com recursão à esquerda, a saída
clássica seria reescrevê-la (eliminação de recursão à esquerda) antes de
programar o parser.

**Onde conferir no código:** `solilang/parser.py:41-56` (o laço) e
`solilang/parser.py:1-20` (a BNF documentada).

---

## 6. oq é lookahead? pq 1 token já é suficiente nessa gramática?

**Resposta:**

Lookahead é quantos tokens o parser "espreita" antes de decidir qual regra
usar. No seu parser, o lookahead é **1**: `_verificar` só olha
`self.tokens[self.posicao]` (`parser.py:123`).

1 token basta porque **o primeiro token de cada alternativa é único**:

| Token atual | Regra escolhida |
|---|---|
| `DOACAO` | `_doacao` |
| `CONSULTA` | `_consulta` |
| `DISTRIBUIR` | `_distribuicao` |
| `RELATORIO` | `_relatorio` |
| `FIM` | encerra o laço |

Isso é o que se chama de gramática **LL(1)**. Se dois comandos começassem
com a mesma palavra, seria necessário fatorar a gramática ou olhar mais
tokens.

**Onde conferir no código:** `solilang/parser.py:58-75` (a escolha) e
`solilang/parser.py:123` (`_verificar`).

---

## 7. qual a diferença entre erro léxico, sintático e semântico? me dá um exemplo de cada usando a solilang

**Resposta:**

| Tipo | Quando acontece | Exemplo | Mensagem |
|---|---|---|---|
| Léxico | um caractere ou palavra não forma token válido | `DOACAO arroz, 50;` | `Erro léxico na linha 2: identificador inválido começando com 'a'; use letra maiúscula (ex.: ARROZ)` |
| Sintático | tokens válidos, na ordem errada | `DOACAO ARROZ 50;` (sem vírgula) | `Erro sintático na linha 2: esperado ',' após o identificador, mas encontrado '50' (NUM)` |
| Semântico | instrução bem escrita, inválida pelas regras | doar 4 e distribuir 10 | `Erro semântico na linha 3: estoque insuficiente para ARROZ: solicitado 10, disponível 4` |

A ordem importa: o léxico vem antes do sintático, que vem antes do semântico.
Uma entrada pode ter erro nas três camadas, mas só o primeiro é reportado.

**Onde conferir no código:** `solilang/errors.py:17,22,27` (as três classes),
`solilang/lexer.py:51-58`, `solilang/parser.py:134` (`_consumir`) e
`solilang/semantic.py:26-55`. Rode `python3 main.py examples/erro_lexico.soli`
(ou `erro_sintatico.soli`, `erro_semantico.soli`).

---

## 8. como funciona o autômato finito do identificador? desenha os estados pra eu entender

**Resposta:**

```
                 [A-Z]                 [A-Z] / [0-9] / _
    (q0) ─────────────────► ((q1)) ───────────────────────► ((q1))
   inicial                 aceitação                        laço

    (q0) ─────[0-9]────────► ((q2)) ─────[0-9]────────────► ((q2))
```

- Em `q0`, uma letra **maiúscula** leva a `q1` (início de palavra).
- Em `q1`, letra maiúscula, dígito ou `_` mantêm o autômato em `q1`.
- Qualquer outro caractere **encerra** o token; o que vem depois é lido do
  zero.
- Letra minúscula em `q0` não tem transição → erro léxico.
- Dígito em `q0` vai para `q2`, o autômato dos números.

No código, isso não é uma tabela de estados: é um `if/elif` sobre o caractere
atual (`lexer.py:38-58`) mais dois laços (`_ler_palavra` e `_ler_numero`).

**Onde conferir no código:** `solilang/lexer.py:11-13` (alfabetos),
`solilang/lexer.py:38-58` (transições), `solilang/lexer.py:77-101` (laços).

---

## 9. pq a análise semântica tem q vir depois do parser?

**Resposta:**

Porque ela trabalha com **significado**, não com texto. Antes do parser você
tem tokens; só depois de montar a AST você tem "uma distribuição de 10
unidades de ARROZ na linha 3". A semântica precisa desses campos (item,
quantidade, linha) para aplicar as regras.

Além disso, checar saldo antes de saber que a instrução é uma `DISTRIBUIR`
bem formada não faria sentido: `DISTRIBUIR ARROZ 10;` não é uma distribuição,
é um erro de sintaxe.

**Onde conferir no código:** `solilang/semantic.py:26-55` (usa `isinstance`
sobre os nós da AST) e `main.py:42-44` (a ordem: parser → `validar`).

---

## 10. pq validar numa cópia do estoque antes de executar? oq aconteceria se validasse direto no estoque real?

**Resposta:**

Se a validação acontecesse junto com a execução, um erro na terceira
instrução deixaria as duas primeiras já aplicadas. O estoque ficaria
**inconsistente e parcial**, e o usuário veria saídas de um programa que
"falhou".

Por isso `validar` (`semantic.py:19`) simula tudo em uma cópia:

```python
estoque = dict(estoque_inicial or {})
```

Se qualquer regra falhar, a exceção sobe, o interpretador nem é chamado e
nada muda. É o "tudo ou nada": ou o programa inteiro é válido e executa, ou
nada executa.

**Onde conferir no código:** `solilang/semantic.py:19-24` e `main.py:39-45`
(validar antes de executar).

---

## 11. oq mudaria na gramática se eu quisesse aceitar expressão aritmética tipo DOACAO ARROZ, 50+10;?

**Resposta:**

Mudaria em cinco lugares:

1. **Lexer**: novos tokens para `+`, `-`, `*`, `/` (e provavelmente `(` e
   `)`). Hoje `lexer.py:57-58` rejeitaria `+` como caractere inesperado.
2. **Gramática**: `NUM` deixaria de ser terminal direto e entraria uma regra
   de expressão, com precedência:
   ```
   <expressao> ::= <termo> { ("+" | "-") <termo> }
   <termo>     ::= <fator> { ("*" | "/") <fator> }
   <fator>     ::= NUM | "(" <expressao> ")"
   ```
3. **AST**: um nó novo, por exemplo `Expressao(operador, esquerda, direita)`,
   no lugar de `quantidade` ser sempre um inteiro.
4. **Parser**: `_doacao` deixaria de usar `_consumir(NUM, ...)` e passaria a
   chamar `_expressao()`.
5. **Interpretador/semântica**: a quantidade passaria a ser **calculada**
   antes de usar, e a regra "maior que zero" seria aplicada ao resultado.

Atenção à recursão à esquerda: `expressao ::= expressao + termo` não pode ser
implementada direto — a forma acima (com `{ }`, que vira laço) já evita o
problema.

**Onde conferir no código:** `solilang/lexer.py:38-58` (onde `+` é rejeitado),
`solilang/parser.py:76-86` (`_doacao` consumindo `NUM`) e
`solilang/ast_nodes.py:11-18` (campo `quantidade`).

---

## 12. pq o lexer não sabe se o arroz existe no estoque?

**Resposta:**

Porque o lexer só vê **caracteres**. Para ele, `ARROZ` é apenas um
identificador que começa com letra maiúscula — não existe "item" nessa fase.

O estoque nem existe durante a análise: ele é criado em memória quando o
interpretador começa (`interpreter.py:16-17`). Saber se `ARROZ` está
cadastrado é uma regra de negócio, e regra de negócio fica na análise
semântica (`semantic.py:41-44`).

Essa separação é o que torna cada fase testável isoladamente: você testa o
lexer com texto, o parser com tokens e a semântica com a AST.

**Onde conferir no código:** `solilang/lexer.py:38-41` (identificador),
`solilang/interpreter.py:16-17` (criação do estoque) e
`solilang/semantic.py:45-50` (verificação de existência).
