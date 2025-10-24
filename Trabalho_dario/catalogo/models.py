
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Optional

STATUS_DISPONIVEL = "DISPONIVEL"
STATUS_INDISPONIVEL = "INDISPONIVEL"

@dataclass
class Livro:
    bookId: int
    titulo: str
    autores: List[str]
    ISBN: Optional[str] = None
    edicao: Optional[str] = None
    ano: Optional[int] = None
    copiasTotal: int = 0
    copiasDisponiveis: int = 0
    status: str = field(init=False)

    def __post_init__(self):
        self._atualizar_status()

    def _atualizar_status(self):
        self.status = STATUS_DISPONIVEL if self.copiasDisponiveis > 0 else STATUS_INDISPONIVEL

    def to_dict(self):
        d = asdict(self)
        return d
