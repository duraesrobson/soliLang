"""testes do analisador sintático (parser)."""

import unittest

from solilang.ast_nodes import Consulta, Distribuicao, Doacao, Relatorio
from solilang.errors import ErroSintatico
from solilang.lexer import Lexer
from solilang.parser import Parser


def analisar(texto):
    """devolve a lista de instruções do texto"""
    return Parser(Lexer(texto).tokenizar()).analisar()


class TestParser(unittest.TestCase):
    def test_programa_completo(self):
        programa = analisar(
            "INICIO\n"
            "    DOACAO ARROZ, 50;\n"
            "    CONSULTA ARROZ;\n"
            "    DISTRIBUIR ARROZ, 10;\n"
            "    CONSULTA ARROZ;\n"
            "    RELATORIO;\n"
            "FIM"
        )
        self.assertEqual(len(programa.instrucoes), 5)

        doacao = programa.instrucoes[0]
        self.assertIsInstance(doacao, Doacao)
        self.assertEqual(doacao.item, "ARROZ")
        self.assertEqual(doacao.quantidade, 50)
        self.assertEqual(doacao.linha, 2)

        self.assertIsInstance(programa.instrucoes[1], Consulta)
        self.assertIsInstance(programa.instrucoes[2], Distribuicao)
        self.assertEqual(programa.instrucoes[2].quantidade, 10)
        self.assertIsInstance(programa.instrucoes[3], Consulta)
        self.assertIsInstance(programa.instrucoes[4], Relatorio)

    def test_programa_vazio_e_aceito(self):
        programa = analisar("INICIO FIM")
        self.assertEqual(programa.instrucoes, [])

    def test_falta_virgula(self):
        with self.assertRaises(ErroSintatico) as contexto:
            analisar("INICIO\n DOACAO ARROZ 50;\nFIM")
        self.assertEqual(contexto.exception.linha, 2)

    def test_falta_ponto_virgula_na_consulta(self):
        with self.assertRaises(ErroSintatico):
            analisar("INICIO CONSULTA ARROZ FIM")

    def test_falta_inicio(self):
        with self.assertRaises(ErroSintatico):
            analisar("DOACAO ARROZ, 50; FIM")

    def test_falta_fim(self):
        with self.assertRaises(ErroSintatico):
            analisar("INICIO DOACAO ARROZ, 50;")

    def test_conteudo_depois_de_fim(self):
        with self.assertRaises(ErroSintatico):
            analisar("INICIO FIM DOACAO ARROZ, 5;")

    def test_comando_desconhecido(self):
        with self.assertRaises(ErroSintatico):
            analisar("INICIO VENDER ARROZ; FIM")

    def test_quantidade_escrita_como_palavra(self):
        with self.assertRaises(ErroSintatico):
            analisar("INICIO DOACAO ARROZ, MUITO; FIM")


if __name__ == "__main__":
    unittest.main()
