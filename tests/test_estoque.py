"""Testes da persistência do estoque em arquivo JSON."""

import json
import os
import tempfile
import unittest

from main import (
    ESTOQUE_PADRAO,
    carregar_estoque,
    executar_arquivo,
    interpretar_argumentos,
    salvar_estoque,
)
from solilang.errors import ErroSemantico


class TestEstoqueEmArquivo(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.estoque = os.path.join(self.pasta.name, "dados.json")
        self.programa = os.path.join(self.pasta.name, "programa.soli")

    def tearDown(self):
        self.pasta.cleanup()

    def escrever_programa(self, texto):
        with open(self.programa, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

    def test_arquivo_inexistente_significa_estoque_vazio(self):
        self.assertEqual(carregar_estoque(self.estoque), {})

    def test_salvar_e_carregar(self):
        salvar_estoque(self.estoque, {"ARROZ": 40, "FEIJAO": 25})
        self.assertEqual(carregar_estoque(self.estoque), {"ARROZ": 40, "FEIJAO": 25})

    def test_arquivo_e_json_legivel_e_ordenado(self):
        salvar_estoque(self.estoque, {"LEITE": 5, "ARROZ": 10})

        with open(self.estoque, encoding="utf-8") as arquivo:
            conteudo = arquivo.read()

        self.assertEqual(
            conteudo,
            '{\n  "ARROZ": 10,\n  "LEITE": 5\n}\n',
        )

    def test_execucao_acumula_no_estoque_salvo(self):
        salvar_estoque(self.estoque, {"ARROZ": 10})
        self.escrever_programa("INICIO DOACAO ARROZ, 5; DISTRIBUIR ARROZ, 3; FIM")

        executar_arquivo(self.programa, self.estoque)

        self.assertEqual(carregar_estoque(self.estoque), {"ARROZ": 12})

    def test_erro_semantico_nao_altera_o_arquivo(self):
        salvar_estoque(self.estoque, {"ARROZ": 4})
        self.escrever_programa("INICIO DISTRIBUIR ARROZ, 10; FIM")

        with self.assertRaises(ErroSemantico):
            executar_arquivo(self.programa, self.estoque)

        self.assertEqual(carregar_estoque(self.estoque), {"ARROZ": 4})

    def test_flag_estoque_usa_o_arquivo_padrao(self):
        modo, caminho, estoque = interpretar_argumentos(
            ["--estoque", "programa.soli"]
        )

        self.assertEqual(modo, "executar")
        self.assertEqual(caminho, "programa.soli")
        self.assertEqual(estoque, ESTOQUE_PADRAO)

    def test_flag_estoque_aceita_caminho_com_igual(self):
        modo, caminho, estoque = interpretar_argumentos(
            ["--estoque=outro.json", "programa.soli"]
        )

        self.assertEqual(modo, "executar")
        self.assertEqual(caminho, "programa.soli")
        self.assertEqual(estoque, "outro.json")

    def test_sem_a_flag_nao_ha_persistencia(self):
        modo, caminho, estoque = interpretar_argumentos(["programa.soli"])

        self.assertEqual(modo, "executar")
        self.assertEqual(caminho, "programa.soli")
        self.assertIsNone(estoque)

    def test_modo_ast_aceita_a_flag(self):
        modo, caminho, estoque = interpretar_argumentos(
            ["--ast", "--estoque", "programa.soli"]
        )

        self.assertEqual(modo, "ast")
        self.assertEqual(caminho, "programa.soli")
        self.assertEqual(estoque, ESTOQUE_PADRAO)


if __name__ == "__main__":
    unittest.main()
