"""analisador léxico (lexer) da solilang.

responsabilidade: transformar o texto do arquivo .soli em uma lista de tokens.
o lexer não sabe se o item existe no estoque: ele apenas reconhece pedaços
de texto, seguindo as expressões regulares da linguagem.
"""

from .errors import ErroLexico
from .tokens import EOF, ID, NUM, PALAVRAS_RESERVADAS, PONTO_VIRGULA, VIRGULA, Token

LETRAS_MAIUSCULAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETRAS_MINUSCULAS = "abcdefghijklmnopqrstuvwxyz"
DIGITOS = "0123456789"
ESPACOS = " \t\n\r"


class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.posicao = 0
        self.linha = 1
        self.coluna = 1

    def tokenizar(self):
        """devolve a lista completa de tokens, terminando com EOF"""
        tokens = []

        while True:
            self._pular_espacos()

            if self.posicao >= len(self.texto):
                tokens.append(Token(EOF, "", self.linha, self.coluna))
                return tokens

            linha, coluna = self.linha, self.coluna
            caractere = self.texto[self.posicao]

            if caractere in LETRAS_MAIUSCULAS:
                texto = self._ler_palavra()
                tipo = PALAVRAS_RESERVADAS.get(texto, ID)
                tokens.append(Token(tipo, texto, linha, coluna))
            elif caractere in DIGITOS:
                texto = self._ler_numero()
                tokens.append(Token(NUM, texto, linha, coluna))
            elif caractere == ",":
                self._avancar()
                tokens.append(Token(VIRGULA, ",", linha, coluna))
            elif caractere == ";":
                self._avancar()
                tokens.append(Token(PONTO_VIRGULA, ";", linha, coluna))
            elif caractere in LETRAS_MINUSCULAS:
                raise ErroLexico(
                    f"identificador inválido começando com '{caractere}'; "
                    "use letra maiúscula (ex.: ARROZ)",
                    linha,
                )
            else:
                raise ErroLexico(f"caractere inesperado: '{caractere}'", linha)

    def _pular_espacos(self):
        """Ignora espaços, tabulações e quebras de linha."""
        while self.posicao < len(self.texto) and self.texto[self.posicao] in ESPACOS:
            self._avancar()

    def _avancar(self):
        """consome um caractere e atualiza a posição na linha e na coluna."""
        caractere = self.texto[self.posicao]
        self.posicao += 1
        if caractere == "\n":
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1

        return caractere

    def _ler_palavra(self):
        """lê o padrão [A-Z][A-Z0-9_]* a partir da posição atual."""
        inicio = self.posicao

        while self.posicao < len(self.texto):
            caractere = self.texto[self.posicao]
            if (
                caractere in LETRAS_MAIUSCULAS
                or caractere in DIGITOS
                or caractere == "_"
            ):
                self._avancar()
            else:
                break

        return self.texto[inicio : self.posicao]

    def _ler_numero(self):
        """lê o padrão [0-9]+ a partir da posição atual."""
        inicio = self.posicao

        while self.posicao < len(self.texto) and self.texto[self.posicao] in DIGITOS:
            self._avancar()

        return self.texto[inicio : self.posicao]
