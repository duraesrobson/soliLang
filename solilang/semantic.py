"""Análise semântica da SoliLang.

O parser garante que a instrução está escrita corretamente. A análise
semântica verifica se ela faz sentido para o sistema Conecta Solidária.

Regras adotadas pelo grupo:
1. Quantidades de doação e distribuição devem ser maiores que zero.
2. DOACAO cria o item automaticamente quando ele ainda não existe.
3. CONSULTA e DISTRIBUIR exigem que o item já exista no estoque.
4. Não é permitido distribuir mais unidades do que o saldo disponível.
5. O programa inteiro é validado antes de qualquer execução: usamos uma
   cópia do estoque, então nada é alterado se houver erro.
"""

from .ast_nodes import Doacao, Consulta, Distribuicao, Relatorio
from .errors import ErroSemantico


def validar(programa, estoque_inicial=None):
    """percorre as instruções em uma cópia do estoque.
    levanta ErroSemantico na primeira instrução inválida.
    não imprime nada e não altera nenhum estoque real.
    """
    estoque = dict(estoque_inicial or {})

    for instrucao in programa.instrucoes:
        if isinstance(instrucao, Doacao):
            if instrucao.quantidade <= 0:
                raise ErroSemantico(
                    f"a quantidade da doação de '{instrucao.item}' deve ser maior que zero (linha {instrucao.linha})"
                )
            estoque[instrucao.item] = (
                estoque.get(instrucao.item, 0) + instrucao.quantidade
            )

        elif isinstance(instrucao, Distribuicao):
            if instrucao.quantidade <= 0:
                raise ErroSemantico(
                    f"a quantidade da distribuição de '{instrucao.item}' deve ser maior que zero (linha {instrucao.linha})"
                )
            if instrucao.item not in estoque:
                raise ErroSemantico(
                    f"item '{instrucao.item}' não existe no estoque (linha {instrucao.linha})"
                )
            disponivel = estoque[instrucao.item]
            if instrucao.quantidade > disponivel:
                raise ErroSemantico(
                    f"estoque insuficiente para {instrucao.item}: "
                    f"solicitado {instrucao.quantidade}, disponível {disponivel}",
                    instrucao.linha,
                )
            estoque[instrucao.item] = disponivel - instrucao.quantidade

        elif isinstance(instrucao, Consulta):
            if instrucao.item not in estoque:
                raise ErroSemantico(
                    f"o item {instrucao.item} não existe no estoque; "
                    "registre uma doação antes de consultá-lo",
                    instrucao.linha,
                )

        elif isinstance(instrucao, Relatorio):
            continue  # não há validação semântica para relatório
