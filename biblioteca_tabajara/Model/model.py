from Model.Livro import Livro

livros_list = []

def adicionar_livro(livro):
    livros_list.append(livro)

def listar_livros():
    return livros_list

def remover_livro(id):
    global livros_list
    livros_list = [l for l in livros_list if l.get_id() != id]

def buscar_livro_por_id(id):
    for livro in livros_list:
        if livro.get_id() == id:
            return livro
    return None
