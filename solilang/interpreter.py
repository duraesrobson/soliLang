"""Interpretador da soliLang.

Executa as instruções já validadas pela análise semântica, mantendo o
estoque em um dicionário Python: {"ARROZ": 40}.

Saídas:
- DOACAO e DISTRIBUIR alteram o estoque em silêncio;
- CONSULTA mostra o saldo do item;
- RELATORIO lista o estoque inteiro em ordem alfabética.
"""

from .ast_nodes import Doacao, Consulta, Distribuicao, Relatorio


class Interpretador:
    def __init__(self, estoque_inicial=None):
        self.estoque = dict(estoque_inicial or {})

    def executar(self, programa):
        """executa as instruções do programa, alterando o estoque real e devolve o estoque final."""
        for instrucao in programa.instrucoes:
            if isinstance(instrucao, Doacao):
                atual = self.estoque.get(instrucao.item, 0)
                self.estoque[instrucao.item] = atual + instrucao.quantidade

            elif isinstance(instrucao, Distribuicao):
                atual = self.estoque[instrucao.item]
                self.estoque[instrucao.item] = atual - instrucao.quantidade

            elif isinstance(instrucao, Consulta):
                print(
                    f"Consulta {instrucao.item}: "
                    f"{self.estoque[instrucao.item]} unidades"
                )
            elif isinstance(instrucao, Relatorio):
                self.imprimir_relatorio()

        return self.estoque

    def imprimir_relatorio(self):
        print("\n------------ Estoque atual ------------")
        if not self.estoque:
            print("(estoque vazio)")
            return

        for item in sorted(self.estoque):
            print(f"{item}: {self.estoque[item]} unidades")
