class RelatorioController:
    def __init__(self, relatorio_service):
        self.service = relatorio_service
    
    def obter_livros_mais_emprestados(self, limite=10):
        return self.service.livros_mais_emprestados(limite)
    
    def obter_usuarios_mais_ativos(self, limite=10):
        return self.service.usuarios_mais_ativos(limite)
    
    def obter_status_acervo(self):
        return self.service.status_acervo()
    
    def obter_status_usuarios(self):
        return self.service.status_usuarios()
    
    def obter_emprestimos_ativos(self):
        return self.service.emprestimos_ativos()
    
    def obter_relatorio_completo(self):
        return self.service.relatorio_completo()