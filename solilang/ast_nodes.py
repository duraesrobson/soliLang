"""Nós da árvore sintática abstrata (AST) da soliLang.

Cada classe representa uma instrução já reconhecida pelo parser.
O parser produz esses objetos; a análise semântica e o interpretador os usam.
"""

from dataclasses import dataclass


@dataclass
class Doacao:
    """DOACAO ITEM, QUANTIDADE;"""

    item: str
    quantidade: int
    linha: int


@dataclass
class Consulta:
    """CONSULTA ITEM;"""

    item: str
    linha: int


@dataclass
class Distribuicao:
    """DISTRIBUIR ITEM, QUANTIDADE;"""

    item: str
    quantidade: int
    linha: int


@dataclass
class Relatorio:
    """RELATORIO;"""

    linha: int


@dataclass
class Programa:
    """Programa completo, com todas as instruções."""

    instrucoes: list
