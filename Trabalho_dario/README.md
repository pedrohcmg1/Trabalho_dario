# SGBU – Módulo Catálogo de Livros (Python + TDD)

Este repositório implementa o **módulo de Catálogo de Livros** do SGBU em Python,
seguindo **TDD** com **pytest**.

## Estrutura
```
catalogo/
  __init__.py
  errors.py
  models.py
  repository.py
  service.py
tests/
  test_catalogo_unit.py
  test_catalogo_integracao.py
```

## Requisitos
- Python 3.10+
- pytest

## Instalação
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Rodar testes
```
pytest -q
```

## Observações de Domínio
- Campos e validações conforme especificação:
  - `titulo`: 1..200 caracteres
  - `autores`: lista de strings; cada autor 1..100 caracteres
  - `ISBN`: string com 10 ou 13 dígitos (opcional); quando presente, deve ser **único** no repositório
  - `edicao`: string opcional
  - `ano`: inteiro (ex.: 2020)
  - `copiasTotal`: inteiro >= 0
  - `copiasDisponiveis`: inteiro >= 0 e <= total
  - `status`: 'DISPONIVEL' ou 'INDISPONIVEL' (**derivado** de `copiasDisponiveis` > 0)

- O **status** é calculado automaticamente pelo serviço para manter consistência com empréstimos.
