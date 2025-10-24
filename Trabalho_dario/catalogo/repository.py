
from __future__ import annotations
from typing import Dict, List, Optional
from .models import Livro
from .errors import NaoEncontradoError, ConflitoError

class LivroRepositoryInMemory:
    """Repositório em memória para facilitar TDD e testes."""
    def __init__(self):
        self._data: Dict[int, Livro] = {}
        self._idx = 0

    def _next_id(self) -> int:
        self._idx += 1
        return self._idx

    def listar(self) -> List[Livro]:
        return list(self._data.values())

    def buscar_por_id(self, bookId: int) -> Livro:
        if bookId not in self._data:
            raise NaoEncontradoError(f"Livro {bookId} não encontrado")
        return self._data[bookId]

    def buscar_por_isbn(self, isbn: str) -> Optional[Livro]:
        for l in self._data.values():
            if l.ISBN == isbn:
                return l
        return None

    def criar(self, livro: Livro) -> Livro:
        if livro.ISBN:
            existente = self.buscar_por_isbn(livro.ISBN)
            if existente is not None:
                raise ConflitoError("ISBN já cadastrado")
        livro.bookId = self._next_id()
        self._data[livro.bookId] = livro
        return livro

    def atualizar(self, bookId: int, livro: Livro) -> Livro:
        if bookId not in self._data:
            raise NaoEncontradoError(f"Livro {bookId} não encontrado")
        if livro.ISBN:
            existente = self.buscar_por_isbn(livro.ISBN)
            if existente and existente.bookId != bookId:
                raise ConflitoError("ISBN já cadastrado")
        self._data[bookId] = livro
        return livro

    def remover(self, bookId: int) -> None:
        if bookId not in self._data:
            raise NaoEncontradoError(f"Livro {bookId} não encontrado")
        del self._data[bookId]
