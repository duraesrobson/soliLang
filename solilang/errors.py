"""Erros da soliLang. Todos os erros carregam a linha do arquivo em que aconteceram."""

class SoliLangError(Exception):
    """Erro base. Não deve ser usado diretamente"""
    
    rotulo = "Erro"
    
    def __init__(self, mensagem, linha):
        self.mensagem = mensagem
        self.linha = linha
        super().__init__(f"{self.rotulo} na linha {self.linha}: {self.mensagem}")
        
    def formatar(self):
        """monta a mensagem final mostrada no termina"""
        return f"{self.rotulo} na linha {self.linha}: {self.mensagem}"
    
class ErroLexico(SoliLangError):
    """caractere ou sequência que não forem um token válido"""
    
    rotulo = "Erro léxico"
        
class ErroSintatico(SoliLangError):
    """tokens organizados de forma diferente da gramática"""
    
    rotulo = "Erro semântico"    
    
class ErroSemantico(SoliLangError):
    """instrução bem escrita, mas invalida pelas regras do sistema"""
    
    rotulo = "Erro semântico"    