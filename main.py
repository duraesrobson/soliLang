"""Ponto de entrada da soliLang.

Orquestra as etapas do processamento na ordem correta:

    arquivo .soli
        -> Lexer        (texto    -> tokens)
        -> Parser       (tokens   -> AST)
        -> validar      (AST      -> checagem das regras)
        -> Interpretador(AST      -> execução e saída)

Modos de uso:
    python3 main.py arquivo.soli                       executa o programa
    python3 main.py --tokens arquivo.soli              mostra os tokens (testador)
    python3 main.py --ast arquivo.soli                 mostra a árvore sintática
"""

import json
import os
import sys

from solilang.errors import SoliLangError
from solilang.interpreter import Interpretador
from solilang.lexer import Lexer
from solilang.parser import Parser
from solilang.repl import iniciar_repl
from solilang.semantic import validar

ESTOQUE_PADRAO = os.path.join("estoque", "estoque_atual.json")

USO = (
    "Uso:\n"
    "  python3 main.py arquivo.soli                       executa o programa\n"
    "  python3 main.py --tokens arquivo.soli              mostra os tokens\n"
    "  python3 main.py --ast arquivo.soli                 mostra a árvore sintática\n"
    "  python3 main.py                                    abre o modo interativo\n"
)


def ler_arquivo(caminho):
    """lê o conteúdo do arquivo e devolve como string UTF-8"""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def carregar_estoque(caminho):
    """lê o estoque salvo em JSON. Arquivo inexistente significa estoque vazio."""
    if not os.path.exists(caminho):
        return {}

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_estoque(caminho, estoque):
    """grava o estoque em JSON de forma atômica.

    Escreve em um arquivo temporário e renomeia no final: se o programa for
    interrompido no meio, o arquivo original continua intacto.
    """
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)

    temporario = f"{caminho}.tmp"

    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(estoque, arquivo, ensure_ascii=False, indent=2, sort_keys=True)
        arquivo.write("\n")

    os.replace(temporario, caminho)


def compilar(caminho, estoque_inicial=None):
    """roda lexer, parser e análise semântica, devolvendo a AST"""
    texto = ler_arquivo(caminho)
    tokens = Lexer(texto).tokenizar()
    programa = Parser(tokens).analisar()
    validar(programa, estoque_inicial)
    return programa


def mostrar_tokens(caminho):
    """mostra os tokens do arquivo"""
    tokens = Lexer(ler_arquivo(caminho)).tokenizar()
    for token in tokens:
        print(token)


def mostrar_ast(caminho, estoque_inicial=None):
    """mostra a árvore sintática do arquivo"""
    programa = compilar(caminho, estoque_inicial)
    print(f"Programa com {len(programa.instrucoes)} instrução(ões):")
    for instrucao in programa.instrucoes:
        print(f"  linha {instrucao.linha}: {instrucao}")


def executar_arquivo(caminho, caminho_estoque=None):
    """executa o programa e, se houver arquivo de estoque, carrega antes e
    grava depois. O arquivo só é gravado se o programa inteiro for válido."""
    estoque_inicial = carregar_estoque(caminho_estoque) if caminho_estoque else {}

    programa = compilar(caminho, estoque_inicial)
    estoque_final = Interpretador(estoque_inicial).executar(programa)

    if caminho_estoque:
        salvar_estoque(caminho_estoque, estoque_final)

    return estoque_final


def interpretar_argumentos(argumentos):
    """separa o modo do caminho do programa.

    O estoque é sempre salvo em ESTOQUE_PADRAO. Não existe opção de escolher
    outro arquivo, para evitar livros-caixa paralelos.
    """
    restantes = []

    for argumento in argumentos:
        if argumento == "--estoque" or argumento.startswith("--estoque="):
            return None, None
        restantes.append(argumento)

    if len(restantes) == 1:
        return "executar", restantes[0]

    if len(restantes) == 2 and restantes[0] in ("--tokens", "--ast"):
        return restantes[0][2:], restantes[1]

    return None, None


def main():
    argumentos = sys.argv[1:]
    modo, caminho = interpretar_argumentos(argumentos)

    if modo is None and caminho is None and argumentos:
        print(USO)
        return 1

    if modo is None and caminho is None:
        # O modo interativo sempre usa o arquivo padrão. Assim, os comandos
        # digitados no terminal não perdem o estoque ao encerrar a sessão.
        estoque = carregar_estoque(ESTOQUE_PADRAO)
        iniciar_repl(
            estoque,
            salvar=lambda atual: salvar_estoque(ESTOQUE_PADRAO, atual),
        )
        return 0

    if modo is None:
        print(USO)
        return 1

    try:
        if modo == "tokens":
            mostrar_tokens(caminho)
        elif modo == "ast":
            mostrar_ast(caminho, carregar_estoque(ESTOQUE_PADRAO))
        else:
            executar_arquivo(caminho, ESTOQUE_PADRAO)

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
        return 1
    except json.JSONDecodeError:
        print(f"Erro: arquivo de estoque inválido: {ESTOQUE_PADRAO}")
        return 1
    except SoliLangError as erro:
        print(erro.formatar())
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
