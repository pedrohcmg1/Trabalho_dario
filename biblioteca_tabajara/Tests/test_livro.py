import pytest
from Model.Livro import Livro

def test_criar_livro():
    livro = Livro(1, "1984", "George Orwell", 3)
    assert livro.get_titulo() == "1984"
    assert livro.get_autor() == "George Orwell"
    assert livro.get_estoque() == 3
    assert livro.get_status() == "disponível"

def test_emprestar_livro_disponivel():
    livro = Livro(2, "Dom Casmurro", "Machado de Assis", 1)
    livro.emprestar()
    assert livro.get_estoque() == 0
    assert livro.get_status() == "emprestado"

def test_emprestar_livro_indisponivel():
    livro = Livro(3, "Memórias Póstumas", "Machado de Assis", 0)
    with pytest.raises(ValueError):
        livro.emprestar()

def test_devolver_livro():
    livro = Livro(4, "O Alienista", "Machado de Assis", 0, "emprestado")
    livro.devolver()
    assert livro.get_estoque() == 1
    assert livro.get_status() == "disponível"
