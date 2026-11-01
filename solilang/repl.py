"""Modo interativo da soliLang (REPL).

Cada linha digitada vira um programa completo temporário:
    INICIO <linha> FIM

Assim a gramática original não precisa mudar para aceitar o modo interativo.
"""

import io
from contextlib import redirect_stdout

from .errors import SoliLangError
from .interpreter import Interpretador
from .lexer import Lexer
from .parser import Parser
from .semantic import validar

PROMPT = "soliLang> "

AJUDA = """Comandos da soliLang:
  DOACAO ITEM, QUANTIDADE;
  CONSULTA ITEM;
  DISTRIBUIR ITEM, QUANTIDADE;
  RELATORIO;

Comandos do terminal:
  :ajuda  mostra esta ajuda
  :sair   encerra o modo interativo
"""


def processar_linha(linha, interpretador, saida=print):
    """valida e executa uma linha sem encerrar o REPL em caso de erro.

    A linha é envolvida por INICIO e FIM para obedecer à gramática completa.
    A validação usa uma cópia do estoque atual; portanto, um erro não altera
    o estado do interpretador.

    Retorna True quando a linha foi válida, False quando teve erro e None
    para uma linha vazia.
    """
    if not linha.strip():
        return None

    texto = f"INICIO\n{linha}\nFIM"

    try:
        tokens = Lexer(texto).tokenizar()
        programa = Parser(tokens).analisar()
        validar(programa, interpretador.estoque)
        # O interpretador usa print; capturamos a saída para que o REPL e os
        # testes possam controlar para onde ela vai.
        impressao = io.StringIO()
        with redirect_stdout(impressao):
            interpretador.executar(programa)
        for texto_saida in impressao.getvalue().splitlines():
            saida(texto_saida)
    except SoliLangError as erro:
        saida(erro.formatar())
        return False

    return True


def iniciar_repl(estoque_inicial=None, salvar=None, entrada=input, saida=print):
    """inicia o loop interativo e devolve o estoque final.

    `salvar`, quando informado, é uma função que recebe o estoque depois de
    cada linha válida. Isso permite ligar o REPL ao JSON sem misturar I/O de
    arquivo com o parser.
    """
    interpretador = Interpretador(estoque_inicial or {})

    saida("soliLang — modo interativo")
    saida('Digite :ajuda para ajuda ou :sair para sair.')

    while True:
        try:
            linha = entrada(PROMPT)
        except EOFError:
            saida("")
            break
        except KeyboardInterrupt:
            saida("\nAté mais!")
            break

        comando = linha.strip().lower()
        if comando in (":sair", ":exit", ":q"):
            break
        if comando == ":ajuda":
            saida(AJUDA.rstrip())
            continue

        if processar_linha(linha, interpretador, saida):
            # Só persiste depois de uma linha válida.
            if salvar is not None:
                salvar(interpretador.estoque)

    return interpretador.estoque
