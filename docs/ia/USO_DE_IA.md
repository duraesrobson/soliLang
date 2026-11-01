# Uso de IA generativa

Registro do uso de IA generativa no desenvolvimento da soliLang, conforme
exigido pelo roteiro do projeto. Cobre todo o uso no desenvolvimento da
ferramenta, da documentação e da preparação da apresentação.

## Ferramenta

- **Interface:** OpenCode, usado pelo terminal (CLI/TUI)
- **Versão:** v2.0.29
- **Plano:** OpenCode Go
- **Modelo:** DeepSeek V4.1 Flash

## Para que foi usada

- Leitura do material de apoio e organização do passo a passo de construção.
- Explicação de conceitos: lexer, parser, AST, front-end e back-end,
  BNF/EBNF, autômato finito e análise semântica.
- Apoio na escrita dos módulos e revisão das mensagens de erro.
- Revisão da redação do README e do relatório.

## Para que não foi usada

- **Pesquisa de campo:** realizada presencialmente com a instituição
  parceira, com registro de data, perfil do entrevistado e
  respostas.
- **Definição da gramática e das regras semânticas:** discutidas e aprovadas
  pelos integrantes.
- **Execução dos testes:** a suíte é rodada localmente pelos integrantes.

## Evidências

| Evidência | Onde |
|---|---|
| Prompts reais da sessão de construção, com o que cada um gerou | `docs/ia/prompts.md` |
| Sessão de estudo do grupo, com perguntas e respostas conceituais | `docs/ia/estudo.md` |
| Histórico de commits, um por módulo | `git log --oneline --graph` |
| Saída dos testes automatizados | `python3 -m unittest discover -v` |

## Como o conteúdo foi validado

- Cada arquivo foi executado localmente; a suíte fecha em 41 testes, todos
  passando.
- Cada módulo foi lido e explicado pelo grupo antes de entrar no repositório.
- Onde a sugestão da IA não se aplicava, o código foi corrigido — por
  exemplo, mensagens de erro que não passavam o número da linha e a
  expectativa de saída do relatório.
- As decisões de linguagem registradas no README foram tomadas pelo grupo,
  não pela ferramenta.

## Exemplos de prompts

1. "oq é uma gramática livre de contexto? e pq a bnf já basta pra solilang?"
2. "pq recursão à esquerda quebra o parser descendente recursivo?"
3. "qual a diferença entre erro léxico, sintático e semântico? me dá um
   exemplo de cada usando a solilang"
4. "me explica detalhadamente como funciona o .soli"

A lista completa está em `docs/ia/prompts.md`.