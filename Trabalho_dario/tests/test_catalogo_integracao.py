
import pytest
from catalogo.service import CatalogoService
from catalogo.errors import ValidacaoError
from catalogo.models import STATUS_DISPONIVEL

def test_fluxo_emprestimo_e_devolucao_mantem_consistencia():
    svc = CatalogoService()
    l = svc.criar_livro(titulo="Livro", autores=["Autor"], copiasTotal=2, copiasDisponiveis=2)
    l = svc.registrar_emprestimo(l.bookId)
    assert l.copiasDisponiveis == 1 and l.status == STATUS_DISPONIVEL
    l = svc.registrar_emprestimo(l.bookId)
    assert l.copiasDisponiveis == 0
    with pytest.raises(ValidacaoError):
        svc.registrar_emprestimo(l.bookId)
    l = svc.registrar_devolucao(l.bookId)
    assert l.copiasDisponiveis == 1

def test_serializacao_contrato_dict():
    svc = CatalogoService()
    l = svc.criar_livro(titulo="Clean Architecture", autores=["Uncle Bob"], ISBN="0123456789", copiasTotal=1, copiasDisponiveis=1)
    d = l.to_dict()
    assert isinstance(d, dict)
    for k in ["bookId","titulo","autores","ISBN","ano","edicao","copiasTotal","copiasDisponiveis","status"]:
        assert k in d

def test_listar_retorna_array_de_livros():
    svc = CatalogoService()
    svc.criar_livro(titulo="A", autores=["X"])  # sem ISBN
    svc.criar_livro(titulo="B", autores=["Y"], ISBN=None)
    arr = svc.listar_livros()
    assert len(arr) == 2 and all(hasattr(x, "bookId") for x in arr)

def test_atualizar_preserva_unicidade_isbn():
    svc = CatalogoService()
    l1 = svc.criar_livro(titulo="A", autores=["X"], ISBN="0123456789")
    l2 = svc.criar_livro(titulo="B", autores=["Y"], ISBN="1234567890")
    with pytest.raises(Exception):
        svc.atualizar_livro(l2.bookId, ISBN="0123456789")  # já usado por l1

def test_ano_limites_aceitos():
    svc = CatalogoService()
    ano_ok = 2020
    l = svc.criar_livro(titulo="Tempo", autores=["Cronos"], ano=ano_ok)
    assert l.ano == ano_ok
