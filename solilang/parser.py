"""Analisador sintático (parser) da SoliLang.

Recebe a lista de tokens produzida pelo lexer e verifica se ela segue a
gramática da linguagem. Se estiver correta, devolve um Programa (AST).

Gramática implementada (BNF):
    <programa>      ::= INICIO <instrucoes> FIM
    <instrucoes>    ::= <instrucao> <instrucoes> | ε
    <instrucao>     ::= <doacao> | <consulta> | <distribuicao> | <relatorio>
    <doacao>        ::= DOACAO ID , NUM ;
    <consulta>      ::= CONSULTA ID ;
    <distribuicao>  ::= DISTRIBUIR ID , NUM ;
    <relatorio>     ::= RELATORIO ;

O parser é descendente recursivo: cada não terminal da gramática virou um
método deste arquivo.
"""

from .ast_nodes import Programa, Doacao, Consulta, Distribuicao, Relatorio
from .errors import ErroSintatico
from .tokens import (
    CONSULTA,
    DOACAO,
    DISTRIBUIR,
    FIM,
    ID,
    INICIO,
    NUM,
    RELATORIO,
    PONTO_VIRGULA,
    VIRGULA,
    EOF,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def analisar(self):
        """<programa> ::= INICIO <instrucoes> FIM"""
        self._consumir(INICIO, "esperado INICIO no começo do programa")

        instrucoes = []
        while not self._verificar(FIM):
            if self._verificar(EOF):
                raise ErroSintatico(
                    "esperado FIM no final do programa",
                    self._atual().linha,
                )
            instrucoes.append(self._instrucao())

        self._consumir(FIM, "esperado FIM no final do programa")
        self._consumir(EOF, "conteúdo inesperado após FIM do programa")
        return Programa(instrucoes)

    def _instrucao(self):
        """<instrucao> ::= <doacao> | <consulta> | <distribuicao> | <relatorio>"""
        if self._verificar(DOACAO):
            return self._doacao()
        if self._verificar(CONSULTA):
            return self._consulta()
        if self._verificar(DISTRIBUIR):
            return self._distribuicao()
        if self._verificar(RELATORIO):
            return self._relatorio()

        token = self._atual()
        raise ErroSintatico(
            "esperado um comando (DOACAO, CONSULTA, DISTRIBUIR ou RELATORIO), "
            f"mas encontrado {self._descrever(token)}",
            token.linha,
        )

    def _doacao(self):
        """<doacao> ::= DOACAO ID , NUM ;"""
        token = self._consumir(
            DOACAO, "esperado DOACAO no início da instrução de doação"
        )
        item = id_token = self._consumir(ID, "esperado um identificador após DOACAO")
        self._consumir(VIRGULA, "esperado ',' após o identificador")
        numero = self._consumir(NUM, "esperado quantidade após ','")
        self._consumir(PONTO_VIRGULA, "esperado ';' no final da instrução de doação")
        return Doacao(item.valor, int(numero.valor), token.linha)

    def _consulta(self):
        """<consulta> ::= CONSULTA ID ;"""
        token = self._consumir(
            CONSULTA, "esperado CONSULTA no início da instrução de consulta"
        )
        item = self._consumir(ID, "esperado um identificador após CONSULTA")
        self._consumir(PONTO_VIRGULA, "esperado ';' no final da instrução de consulta")
        return Consulta(item.valor, token.linha)

    def _distribuicao(self):
        """<distribuicao> ::= DISTRIBUIR ID , NUM ;"""
        token = self._consumir(
            DISTRIBUIR, "esperado DISTRIBUIR no início da instrução de distribuição"
        )
        item = self._consumir(ID, "esperado um identificador após DISTRIBUIR")
        self._consumir(VIRGULA, "esperado ',' após o identificador")
        numero = self._consumir(NUM, "esperado quantidade após ','")
        self._consumir(
            PONTO_VIRGULA, "esperado ';' no final da instrução de distribuição"
        )
        return Distribuicao(item.valor, int(numero.valor), token.linha)

    def _relatorio(self):
        """<relatorio> ::= RELATORIO ;"""
        token = self._consumir(
            RELATORIO, "esperado RELATORIO no início da instrução de relatório"
        )
        self._consumir(PONTO_VIRGULA, "esperado ';' no final da instrução de relatório")
        return Relatorio(token.linha)

    # --- Funções auxiliares de leitura de tokens -------------------------

    def _atual(self):
        """retorna o token atual (onde o parser está)"""
        return self.tokens[self.posicao]
    
    def _verificar(self, tipo):
        """verifica se o token atual é do tipo esperado"""
        return self._atual().tipo == tipo
    
    def _avançar(self):
        """avança para o próximo token e retorna o token atual"""
        token = self.tokens[self.posicao]
        if token.tipo != EOF:
            self.posicao += 1
        return token
    
    def _consumir(self, tipo, mensagem_erro):
        """consome o token atual se for do tipo esperado, caso contrário lança um erro"""
        if self._verificar(tipo):
            return self._avançar()
        token = self._atual()
        raise ErroSintatico(
            f"{mensagem_erro}, mas encontrado {self._descrever(token)}",
            token.linha,
        )
        
    def _descrever(self, token):
        """retorna uma descrição legível do token"""
        if token.tipo == EOF:
            return "fim do arquivo"
        return f"'{token.valor}' ({token.tipo})"