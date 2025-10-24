
import pytest
from catalogo.service import CatalogoService
from catalogo.errors import ValidacaoError, NaoEncontradoError, ConflitoError
from catalogo.models import STATUS_DISPONIVEL, STATUS_INDISPONIVEL

def criar_svc():
    return CatalogoService()

def test_criar_livro_valido():
    svc = criar_svc()
    l = svc.criar_livro(titulo="Clean Code", autores=["Robert C. Martin"], ISBN="9780132350884", ano=2008, copiasTotal=2, copiasDisponiveis=1)
    assert l.bookId > 0
    assert l.status == STATUS_DISPONIVEL

def test_status_indisponivel_quando_sem_copias():
    svc = criar_svc()
    l = svc.criar_livro(titulo="DDD", autores=["Eric Evans"], copiasTotal=1, copiasDisponiveis=0)
    assert l.status == STATUS_INDISPONIVEL

def test_titulo_invalido():
    svc = criar_svc()
    with pytest.raises(ValidacaoError):
        svc.criar_livro(titulo="", autores=["A"])

def test_autores_nao_pode_ser_vazio():
    svc = criar_svc()
    with pytest.raises(ValidacaoError):
        svc.criar_livro(titulo="Livro", autores=[])

def test_autor_com_tamanho_invalido():
    svc = criar_svc()
    with pytest.raises(ValidacaoError):
        svc.criar_livro(titulo="Livro", autores=[""])

def test_isbn_deve_ter_10_ou_13_digitos_quando_presente():
    svc = criar_svc()
    with pytest.raises(ValidacaoError):
        svc.criar_livro(titulo="Livro", autores=["Autor"], ISBN="123") 

def test_copias_disponiveis_nao_pode_exceder_total():
    svc = criar_svc()
    with pytest.raises(ValidacaoError):
        svc.criar_livro(titulo="Livro", autores=["Autor"], copiasTotal=1, copiasDisponiveis=2)

def test_isbn_unico():
    svc = criar_svc()
    svc.criar_livro(titulo="A", autores=["X"], ISBN="0123456789") 
    with pytest.raises(ConflitoError):
        svc.criar_livro(titulo="B", autores=["Y"], ISBN="0123456789") 

def test_buscar_e_nao_encontrar():
    svc = criar_svc()
    with pytest.raises(NaoEncontradoError):
        svc.obter_livro(999)

def test_atualizar_e_mudar_status():
    svc = criar_svc()
    l = svc.criar_livro(titulo="Livro", autores=["Autor"], copiasTotal=1, copiasDisponiveis=1)
    l2 = svc.atualizar_livro(l.bookId, copiasDisponiveis=0)
    assert l2.status == STATUS_INDISPONIVEL
