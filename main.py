"""Ponto de entrada da soliLang.

Orquestra as etapas do processamento na ordem correta:

    arquivo .soli
        -> Lexer        (texto    -> tokens)
        -> Parser       (tokens   -> AST)
        -> validar      (AST      -> checagem das regras)
        -> Interpretador(AST      -> execução e saída)

Modos de uso:
    python3 main.py arquivo.soli            executa o programa
    python3 main.py --tokens arquivo.soli   mostra os tokens (testador)
    python3 main.py --ast arquivo.soli      mostra a árvore sintática
"""

import sys

from solilang.errors import SoliLangError
from solilang.interpreter import Interpretador
from solilang.lexer import Lexer
from solilang.parser import Parser
from solilang.semantic import validar

USO = (
    "Uso:\n"
    "  python3 main.py arquivo.soli            executa o programa\n"
    "  python3 main.py --tokens arquivo.soli   mostra os tokens (testador)\n"
    "  python3 main.py --ast arquivo.soli      mostra a árvore sintática\n"
)


def ler_arquivo(caminho):
    """lê o conteúdo do arquivo e devolve como string UTF-8"""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def compilar(caminho):
    """roda lexer, parser e análise semântica, devolvendo a AST"""
    texto = ler_arquivo(caminho)
    tokens = Lexer(texto).tokenizar()
    programa = Parser(tokens).analisar()
    validar(programa)
    return programa


def mostrar_tokens(caminho):
    """mostra os tokens do arquivo"""
    tokens = Lexer(ler_arquivo(caminho)).tokenizar()
    for token in tokens:
        print(token)


def mostrar_ast(caminho):
    """mostra a árvore sintática do arquivo"""
    programa = compilar(caminho)
    print(f"Programa com {len(programa.instrucoes)} instrução(ões):")
    for instrucao in programa.instrucoes:
        print(f"  linha {instrucao.linha}: {instrucao}")


def main():
    argumentos = sys.argv[1:]

    if len(argumentos) == 1:
        modo, caminho = "executar", argumentos[0]
    elif len(argumentos) == 2 and argumentos[0] in ("--tokens", "--ast"):
        modo, caminho = argumentos[0][2:], argumentos[1]
    else:
        print(USO)
        return 1

    try:
        if modo == "tokens":
            mostrar_tokens(caminho)
        elif modo == "ast":
            mostrar_ast(caminho)
        else:
            programa = compilar(caminho)
            Interpretador().executar(programa)

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
        return 1
    except SoliLangError as erro:
        print(erro.formatar())
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
