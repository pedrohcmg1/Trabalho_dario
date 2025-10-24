
from __future__ import annotations
from typing import List, Optional
import re, datetime
from .models import Livro, STATUS_DISPONIVEL, STATUS_INDISPONIVEL
from .repository import LivroRepositoryInMemory
from .errors import ValidacaoError, NaoEncontradoError

ISBN_RE = re.compile(r"^\d{10}(\d{3})?$")  

class CatalogoService:
    def __init__(self, repo: Optional[LivroRepositoryInMemory]=None):
        self.repo = repo or LivroRepositoryInMemory()

    def _validar_campos(self, *, titulo: str, autores: List[str], ISBN: Optional[str],
                        edicao: Optional[str], ano: Optional[int],
                        copiasTotal: int, copiasDisponiveis: int):

        if not isinstance(titulo, str) or not (1 <= len(titulo) <= 200):
            raise ValidacaoError("titulo deve ter 1..200 caracteres")

        if not isinstance(autores, list) or len(autores) == 0:
            raise ValidacaoError("autores deve ser uma lista não vazia")
        for a in autores:
            if not isinstance(a, str) or not (1 <= len(a) <= 100):
                raise ValidacaoError("cada autor deve ter 1..100 caracteres")
        if ISBN is not None:
            if not isinstance(ISBN, str) or ISBN.strip() == "":
                ISBN = None  
            else:
                if not ISBN_RE.match(ISBN):
                    raise ValidacaoError("ISBN deve ter 10 ou 13 dígitos numéricos")

        if ano is not None:
            if not isinstance(ano, int):
                raise ValidacaoError("ano deve ser inteiro")
            if ano < 0 or ano > datetime.date.today().year + 1:
                raise ValidacaoError("ano inválido")
        if not isinstance(copiasTotal, int) or copiasTotal < 0:
            raise ValidacaoError("copiasTotal deve ser inteiro >= 0")
        if not isinstance(copiasDisponiveis, int) or copiasDisponiveis < 0:
            raise ValidacaoError("copiasDisponiveis deve ser inteiro >= 0")
        if copiasDisponiveis > copiasTotal:
            raise ValidacaoError("copiasDisponiveis não pode exceder copiasTotal")

        return dict(titulo=titulo, autores=autores, ISBN=ISBN, edicao=edicao,
                    ano=ano, copiasTotal=copiasTotal, copiasDisponiveis=copiasDisponiveis)

    def criar_livro(self, *, titulo: str, autores: List[str], ISBN: Optional[str]=None,
                    edicao: Optional[str]=None, ano: Optional[int]=None,
                    copiasTotal: int=0, copiasDisponiveis: int=0):
        dados = self._validar_campos(titulo=titulo, autores=autores, ISBN=ISBN,
                                     edicao=edicao, ano=ano,
                                     copiasTotal=copiasTotal,
                                     copiasDisponiveis=copiasDisponiveis)
        livro = Livro(bookId=0, **dados)
        return self.repo.criar(livro)

    def obter_livro(self, bookId: int):
        return self.repo.buscar_por_id(bookId)

    def listar_livros(self):
        return self.repo.listar()

    def atualizar_livro(self, bookId: int, **campos):
        livro_atual = self.obter_livro(bookId)
        dados = self._validar_campos(
            titulo=campos.get("titulo", livro_atual.titulo),
            autores=campos.get("autores", livro_atual.autores),
            ISBN=campos.get("ISBN", livro_atual.ISBN),
            edicao=campos.get("edicao", livro_atual.edicao),
            ano=campos.get("ano", livro_atual.ano),
            copiasTotal=campos.get("copiasTotal", livro_atual.copiasTotal),
            copiasDisponiveis=campos.get("copiasDisponiveis", livro_atual.copiasDisponiveis),
        )
        from .models import Livro
        novo = Livro(bookId=bookId, **dados)
        return self.repo.atualizar(bookId, novo)

    def remover_livro(self, bookId: int) -> None:
        self.repo.remover(bookId)

    def registrar_emprestimo(self, bookId: int):
        livro = self.obter_livro(bookId)
        if livro.copiasDisponiveis <= 0:
            raise ValidacaoError("Não há cópias disponíveis para empréstimo")
        return self.atualizar_livro(bookId, copiasDisponiveis=livro.copiasDisponiveis - 1)

    def registrar_devolucao(self, bookId: int):
        livro = self.obter_livro(bookId)
        if livro.copiasDisponiveis >= livro.copiasTotal:
            raise ValidacaoError("Todas as cópias já estão na biblioteca")
        return self.atualizar_livro(bookId, copiasDisponiveis=livro.copiasDisponiveis + 1)
