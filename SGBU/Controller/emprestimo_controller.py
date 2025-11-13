class EmprestimoController:
    def __init__(self, emprestimo_repository):
        self.repository = emprestimo_repository
    
    def realizar_emprestimo(self, matricula_usuario, codigo_livro):
        try:
            return self.repository.registrar_emprestimo(matricula_usuario, codigo_livro)
        except ValueError as e:
            raise e
    
    def realizar_devolucao(self, id_emprestimo):
        try:
            return self.repository.registrar_devolucao(id_emprestimo)
        except ValueError as e:
            raise e
    
    def buscar_emprestimo(self, id_emprestimo):
        return self.repository.buscar(id_emprestimo)
    
    def listar_emprestimos(self):
        return self.repository.listar()
    
    def listar_emprestimos_usuario(self, matricula_usuario):
        return self.repository.listar_por_usuario(matricula_usuario)
    
    def listar_emprestimos_livro(self, codigo_livro):
        return self.repository.listar_por_livro(codigo_livro)
    
    def listar_emprestimos_ativos(self):
        return self.repository.listar_ativos()