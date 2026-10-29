"""testes do analisador léxico (lexer)."""

import unittest

from solilang import tokens as tk
from solilang.errors import ErroLexico
from solilang.lexer import Lexer


def tipos(texto):
    """devolve a lista de tipos de tokens do texto"""
    return [token.tipo for token in Lexer(texto).tokenizar()]


class TestLexer(unittest.TestCase):
    def test_programa_completo(self):
        texto = "INICIO DOACAO ARROZ, 50; FIM"
        self.assertEqual(
            tipos(texto),
            [
                tk.INICIO,
                tk.DOACAO,
                tk.ID,
                tk.VIRGULA,
                tk.NUM,
                tk.PONTO_VIRGULA,
                tk.FIM,
                tk.EOF,
            ],
        )

    def test_valores_e_linhas(self):
        tokens = Lexer("INICIO\n DOACAO ARROZ, 50;\n FIM").tokenizar()

        self.assertEqual(tokens[1].tipo, tk.DOACAO)
        self.assertEqual(tokens[1].linha, 2)

        self.assertEqual(tokens[2].tipo, tk.ID)
        self.assertEqual(tokens[2].valor, "ARROZ")
        self.assertEqual(tokens[2].linha, 2)

        self.assertEqual(tokens[4].tipo, tk.NUM)
        self.assertEqual(tokens[4].valor, "50")

    def test_identificador_com_numero_e_sublinhado(self):
        token = Lexer("FEIJAO_2").tokenizar()[0]
        self.assertEqual(token.tipo, tk.ID)
        self.assertEqual(token.valor, "FEIJAO_2")

    def test_palavras_reservadas_nao_viram_id(self):
        for palavra in (
            "INICIO",
            "FIM",
            "DOACAO",
            "CONSULTA",
            "DISTRIBUIR",
            "RELATORIO",
        ):
            self.assertEqual(tipos(palavra)[0], palavra)

    def test_erro_lexico_com_minuscula(self):
        with self.assertRaises(ErroLexico) as contexto:
            Lexer("INICIO\n DOACAO arroz, 50;\nFIM").tokenizar()
        self.assertEqual(contexto.exception.linha, 2)

    def test_erro_lexico_com_caractere_invalido(self):
        with self.assertRaises(ErroLexico):
            Lexer("INICIO DOACAO ARROZ, 50 @; FIM").tokenizar()

    def test_espacos_e_quebras_sao_ignorados(self):
        self.assertEqual(
            tipos("  \n\t INICIO   FIM  \n"),
            [
                tk.INICIO,
                tk.FIM,
                tk.EOF,
            ],
        )


if __name__ == "__main__":
    unittest.main()
