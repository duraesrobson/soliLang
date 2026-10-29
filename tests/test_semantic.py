"""testes da análise semântica."""

import unittest

from solilang.errors import ErroSemantico
from solilang.lexer import Lexer
from solilang.parser import Parser
from solilang.semantic import validar


def validar_texto(texto):
    programa = Parser(Lexer(texto).tokenizar()).analisar()
    validar(programa)


class TestSemantica(unittest.TestCase):
    def test_fluxo_valido(self):
        validar_texto(
            "INICIO DOACAO ARROZ, 50; DISTRIBUIR ARROZ, 10; "
            "CONSULTA ARROZ; RELATORIO; FIM"
        )

    def test_doacao_cria_item_novo(self):
        validar_texto("INICIO DOACAO FEIJAO, 1; FIM")

    def test_doacao_com_zero(self):
        with self.assertRaises(ErroSemantico) as contexto:
            validar_texto("INICIO DOACAO ARROZ, 0; FIM")
        self.assertEqual(contexto.exception.linha, 1)
        self.assertIn("maior que zero", contexto.exception.mensagem)

    def test_distribuicao_com_zero(self):
        with self.assertRaises(ErroSemantico) as contexto:
            validar_texto("INICIO DOACAO ARROZ, 5; DISTRIBUIR ARROZ, 0; FIM")
        self.assertEqual(contexto.exception.linha, 1)
        self.assertIn("maior que zero", contexto.exception.mensagem)

    def test_distribuir_mais_que_o_saldo(self):
        with self.assertRaises(ErroSemantico) as contexto:
            validar_texto(
                "INICIO\n" "  DOACAO ARROZ, 4;\n" "  DISTRIBUIR ARROZ, 10;\n" "FIM"
            )
        self.assertEqual(contexto.exception.linha, 3)
        self.assertIn("insuficiente", contexto.exception.mensagem)
        self.assertIn("disponível 4", contexto.exception.mensagem)

    def test_distribuir_item_inexistente(self):
        with self.assertRaises(ErroSemantico) as contexto:
            validar_texto("INICIO DISTRIBUIR ARROZ, 1; FIM")
        self.assertIn("não existe", contexto.exception.mensagem)

    def test_consultar_item_inexistente(self):
        with self.assertRaises(ErroSemantico):
            validar_texto("INICIO CONSULTA ARROZ; FIM")

    def test_itens_independentes(self):
        validar_texto(
            "INICIO DOACAO ARROZ, 10; DOACAO FEIJAO, 5; "
            "DISTRIBUIR ARROZ, 10; CONSULTA FEIJAO; FIM"
        )

    def test_programa_vazio_e_valido(self):
        validar_texto("INICIO FIM")


if __name__ == "__main__":
    unittest.main()
