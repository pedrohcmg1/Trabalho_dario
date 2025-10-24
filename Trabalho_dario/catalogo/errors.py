
class CatalogoError(Exception):
    """Erro base do módulo Catálogo."""

class ValidacaoError(CatalogoError):
    """Dados inválidos ou violação de regra de domínio."""

class NaoEncontradoError(CatalogoError):
    """Livro não encontrado."""

class ConflitoError(CatalogoError):
    """Conflito de integridade (ex.: ISBN duplicado)."""
