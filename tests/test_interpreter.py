"""Testes de integração: lexer -> parser -> semântica -> interpretador."""

import io
import unittest
from contextlib import redirect_stdout

from solilang.interpreter import Interpretador
from solilang.lexer import Lexer
from solilang.parser import Parser
from solilang.semantic import validar

PROGRAMA_DO_GUIA = """INICIO
    DOACAO ARROZ, 50;
    CONSULTA ARROZ;
    DISTRIBUIR ARROZ, 10;
    CONSULTA ARROZ;
    RELATORIO;
FIM"""


def executar(texto):
    programa = Parser(Lexer(texto).tokenizar()).analisar()
    validar(programa)

    saida = io.StringIO()
    with redirect_stdout(saida):
        estoque = Interpretador().executar(programa)

    return saida.getvalue(), estoque


class TestInterpretador(unittest.TestCase):
    def test_saida_do_exemplo_do_guia(self):
        saida, estoque = executar(PROGRAMA_DO_GUIA)

        self.assertEqual(
            saida,
            "Consulta ARROZ: 50 unidades\n"
            "Consulta ARROZ: 40 unidades\n"
            "\n------------ Estoque atual ------------\n"
            "ARROZ: 40 unidades\n",
        )
        self.assertEqual(estoque, {"ARROZ": 40})

    def test_relatorio_com_estoque_vazio(self):
        saida, estoque = executar("INICIO RELATORIO; FIM")
        self.assertEqual(
            saida,
            "\n------------ Estoque atual ------------\n(estoque vazio)\n",
        )
        self.assertEqual(estoque, {})

    def test_relatorio_em_ordem_alfabetica(self):
        saida, _ = executar("INICIO DOACAO LEITE, 2; DOACAO ARROZ, 5; RELATORIO; FIM")
        self.assertEqual(
            saida,
            "\n------------ Estoque atual ------------\n"
            "ARROZ: 5 unidades\n"
            "LEITE: 2 unidades\n",
        )

    def test_doacao_e_distribuicao_nao_imprimem(self):
        saida, _ = executar("INICIO DOACAO ARROZ, 5; DISTRIBUIR ARROZ, 2; FIM")
        self.assertEqual(saida, "")


if __name__ == "__main__":
    unittest.main()
