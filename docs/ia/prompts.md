# Prompts da sessão de construção

Seleção dos pedidos mais relevantes feitos durante o desenvolvimento da
soliLang, na ordem em que aconteceram, com o que cada um produziu e o que foi
decidido a partir dele.

- **Ferramenta:** OpenCode v2.0.29 no terminal
- **Plano:** OpenCode Go
- **Modelo:** DeepSeek V4.1 Flash
- **Sessão:** `ses_e8449a7a2ffeOUv519jX74Jp4s`

## Desenvolvimento

| # | Prompt (resumido) | O que gerou | Decisão tomada |
|---|---|---|---|
| 1 | "lê o pdf da pasta e planeja o projeto; depois cria um .md com o passo a passo e o que cada arquivo faz" | leitura do material, 8 decisões de projeto, plano de construção | seguir o plano arquivo por arquivo |
| 2 | "isso seria criar um compilador?" | distinção entre compilador e processador de linguagem | descrever o projeto como processador com interpretador |
| 3 | [roteiro da faculdade] "segue o que o roteiro pede? me fala antes e explica" | comparação roteiro × projeto, conflito CAA × doações | pedir aval do professor para o público-alvo |
| 4 | "e se eu quiser um compilador? o roteiro oficial pede isso não?" | análise do escopo real (scanner + parser) | manter interpretador; geração de código como trabalho futuro |
| 5 | "e essa questão de front-end como faríamos?" | front-end de compilador × front-end web | documentar as fases no README |
| 6 | "a consulta não retorna a quantidade não?" | separação entre análise e execução | `CONSULTA` imprime no interpretador |
| 7 | "mantém o banner; corrige o detalhe do `.get`" | decisão de saída do relatório | banner `Estoque atual` e acesso direto ao estoque |
| 8 | "cria o readme seguindo o passo a passo" | `README.md` completo | README como porta de entrada do repositório |
| 9 | "tudo que citar a linguagem é soliLang e não SoliLang" | padronização do nome | `soliLang` nos documentos e docstrings |
| 10 | "o que a gente teria que fazer para entrar o ODS 4?" | três caminhos (documentar, `CAMPANHA`, `DESTINATARIO`) | documentar e confirmar na entrevista |
| 11 | "analisando o projeto todo, ele segue o roteiro oficial?" | auditoria de conformidade | lista de pendências (pesquisa, relatório, vídeo, repo público) |
| 12 | "como comprovar o uso de IA?" | formato de registro e evidências | este documento e o `USO_DE_IA.md` |

## Como usar este registro

- Os prompts acima são pedidos reais feitos durante o desenvolvimento, na
  ordem em que ocorreram.
- Cada linha associa o pedido a um resultado verificável no repositório
  (arquivo, commit, teste ou decisão).
- As perguntas conceituais do grupo estão em `docs/ia/estudo.md`.
