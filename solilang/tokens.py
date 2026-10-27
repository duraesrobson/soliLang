"""Tipos de tokens e palavras reservadas da SoliLang.

Um token é a menor unidade significativa do programa: uma palavra reservada,
um identificador, um número ou um sinal de pontuação.
"""

from dataclasses import dataclass

# tipos de token da soliLang. texto em vez de números para que os teste e as mensagem fiquem legíveis
INICIO = "INICIO"
FIM = "FIM"
DOACAO = "DOACAO"
CONSULTA = "CONSULTA"
DISTRIBUIR = "DISTRIBUIR"
RELATORIO = "RELATORIO"
ID = "ID"
NUM = "NUM"
VIRGULA = "VIRGULA"
PONTO_VIRGULA = "PONTO_VIRGULA"
EOF = "EOF"  # end of file

# dicionario usado pelo lexer: se o texto for uma destas palavras, o token recebe o tipo da palavra; else, vira ID
PALAVRAS_RESERVADAS = {
    "INICIO": INICIO,
    "FIM": FIM,
    "DOACAO": DOACAO,
    "CONSULTA": CONSULTA,
    "DISTRIBUIR": DISTRIBUIR,
    "RELATORIO": RELATORIO,
}


@dataclass
class Token:
    """um token encontrado no código fonte"""

    tipo: str
    valor: str
    linha: int
    coluna: int

    def __repr__(self):
        return (
            f"Token({self.tipo}, {self.valor!r}, "
            f"linha={self.linha}, coluna={self.coluna})"
        )
