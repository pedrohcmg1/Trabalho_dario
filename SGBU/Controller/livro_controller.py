from Model.livro import Livro

class LivroController:
    def __init__(self, livro_repository):
        self.repository = livro_repository
    
    def cadastrar_livro(self, codigo, titulo, autor, quantidade_total):
        try:
            livro = Livro(codigo, titulo, autor, quantidade_total)
            return self.repository.cadastrar(livro)
        except ValueError as e:
            raise e
    
    def buscar_livro(self, codigo):
        return self.repository.buscar(codigo)
    
    def listar_livros(self):
        return self.repository.listar()
    
    def editar_livro(self, codigo, titulo=None, autor=None, quantidade_total=None):
        return self.repository.editar(codigo, titulo, autor, quantidade_total)
    
    def remover_livro(self, codigo):
        return self.repository.remover(codigo)
    
    def verificar_disponibilidade(self, codigo):
        return self.repository.verificar_disponibilidade(codigo)