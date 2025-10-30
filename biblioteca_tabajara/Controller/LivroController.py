from Model import model as md
from Model.Livro import Livro

class LivroController:
    def __init__(self):
        pass

    def cadastrar_livro(self, id, titulo, autor, estoque):
        novo_livro = Livro(id, titulo, autor, estoque)
        md.adicionar_livro(novo_livro)
        return novo_livro

    def listar_livros(self):
        return md.listar_livros()

    def remover_livro(self, id):
        md.remover_livro(id)

    def buscar_livro(self, id):
        return md.buscar_livro_por_id(id)
