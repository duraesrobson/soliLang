"""Testes do modo interativo da soliLang."""

import io
import unittest

from solilang.interpreter import Interpretador
from solilang.repl import iniciar_repl, processar_linha


class TestRepl(unittest.TestCase):
    def test_linha_valida_executa(self):
        interpretador = Interpretador()
        saida = io.StringIO()

        resultado = processar_linha(
            "DOACAO ARROZ, 10;", interpretador, saida.write
        )

        self.assertTrue(resultado)
        self.assertEqual(interpretador.estoque, {"ARROZ": 10})
        self.assertEqual(saida.getvalue(), "")

    def test_estado_acumula_entre_linhas(self):
        linhas = iter(
            [
                "DOACAO ARROZ, 10;",
                "DISTRIBUIR ARROZ, 3;",
                "CONSULTA ARROZ;",
                ":sair",
            ]
        )
        saidas = []

        estoque = iniciar_repl(
            entrada=lambda prompt: next(linhas),
            saida=saidas.append,
        )

        self.assertEqual(estoque, {"ARROZ": 7})
        self.assertIn("Consulta ARROZ: 7 unidades", saidas)

    def test_erro_nao_encerra_e_nao_altera_estado(self):
        interpretador = Interpretador({"ARROZ": 4})
        saida = io.StringIO()

        resultado = processar_linha(
            "DISTRIBUIR ARROZ, 10;", interpretador, saida.write
        )

        self.assertFalse(resultado)
        self.assertEqual(interpretador.estoque, {"ARROZ": 4})
        self.assertIn("estoque insuficiente", saida.getvalue())

    def test_persiste_apenas_linhas_validas(self):
        linhas = iter(
            [
                "DOACAO ARROZ, 10;",
                "DISTRIBUIR ARROZ, 50;",
                ":sair",
            ]
        )
        salvos = []

        iniciar_repl(
            entrada=lambda prompt: next(linhas),
            saida=lambda texto: None,
            salvar=lambda estoque: salvos.append(dict(estoque)),
        )

        self.assertEqual(salvos, [{"ARROZ": 10}])

    def test_comandos_de_ajuda_e_saida(self):
        linhas = iter([":ajuda", ":q"])
        saidas = []

        iniciar_repl(
            entrada=lambda prompt: next(linhas),
            saida=saidas.append,
        )

        self.assertTrue(any("DOACAO ITEM" in texto for texto in saidas))


if __name__ == "__main__":
    unittest.main()
