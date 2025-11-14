# Sistema Unificado - Grupo A

> 📖 **Novo no projeto?** Comece lendo o arquivo [`ESTRUTURA.md`](ESTRUTURA.md) para entender a organização dos arquivos.

## ✅ Integração Completa

Aplicação Flask que integra **4 projetos** em uma única aplicação:

1. **Atividade_PITS-main** - Sistema de gestão de usuários (CRUD completo)
2. **Trabalho-2S-master** - Sistema de gestão de biblioteca (usuários, livros, empréstimos, relatórios)
3. **Empr-stimo-e-Devolu-o-main** - Sistema de empréstimos e devoluções (Flask)
4. **TrabalhoProfDacioIntegracoes-main** - CRUD de livros (HTML/CSS)

## 🚀 Como Executar

> 💡 **Dica**: Para um guia mais rápido, veja [`QUICK_START.md`](QUICK_START.md)

```bash
cd "/Users/marcoscardoso/Desktop/GRUPOS A/sistema_grupo_unificado"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

A aplicação estará disponível em: **http://127.0.0.1:5050**

> 📁 **Quer entender a estrutura?** Veja [`ESTRUTURA.md`](ESTRUTURA.md) para uma explicação detalhada dos arquivos e diretórios.

## 📋 Rotas Disponíveis

### Home
- `/` - Página inicial com links para todas as seções

### PITS - Gestão de Usuários
- `/pits/menu` - Menu principal do módulo PITS
- `/pits/usuarios` - Lista todos os usuários
- `/pits/cadastrar_usuario` - Formulário de cadastro de usuário
- `/pits/editar_usuario` - Formulário de edição de usuário (GET com ?id=...)
- `/pits/criar_usuario` - Endpoint para criar usuário (POST)
- `/pits/atualizar_usuario` - Endpoint para atualizar usuário (POST)
- `/pits/excluir_usuario` - Endpoint para excluir usuário (POST)
- `/pits/buscar_usuario` - Endpoint para buscar usuário por ID (GET com ?id=...)

### Trabalho-2S (Sistema de Gestão)
- `/t2s/menu` - Menu principal
- `/t2s/listar_usuarios` - Lista todos os usuários
- `/t2s/listar_livros` - Lista todos os livros
- `/t2s/listar_emprestimos` - Lista empréstimos ativos
- `/t2s/relatorios` - Relatórios e analytics
- `/t2s/relatorios_livros` - Relatório de livros mais emprestados
- `/t2s/relatorios_usuarios` - Relatório de usuários mais ativos

### Empréstimo/Devolução (Flask)
- `/emprestimos` - Interface de empréstimos
- `/devolucoes` - Interface de devoluções
- `/api/loans` - API JSON com lista de empréstimos
- `/api/loans/<id>/return` - API para devolver empréstimo (POST)

### Dácio (CRUD Livros Completo)
- `/dacio/menu` - Menu do módulo Dácio
- `/dacio/listar_livros` - Lista livros com ações de editar/remover
- `/dacio/cadastrar_livro` - Formulário de cadastro
- `/dacio/cadastrar` - Endpoint para cadastrar (POST)
- `/dacio/alterar_livro` - Formulário de edição (GET com ?isbn=...)
- `/dacio/alterar_livro` - Endpoint para salvar edição (POST)
- `/dacio/remover_livro` - Endpoint para remover livro (POST)

## 🔧 Arquitetura

- **Flask** como framework web unificado
- **Banco de dados em memória** para Trabalho-2S (não requer MongoDB)
- **Isolamento de módulos** para evitar conflitos de namespace
- **Mocks** para serviços de usuários e catálogo (projeto Empréstimo)

## 📦 Dependências

- Flask 3.0.3
- pytest 8.2.0
- dataclasses-json 0.6.1
- pymongo 4.6.0 (opcional - só se usar MongoDB)
- python-dotenv 1.0.0
- pydantic 2.8.2
- selenium 4.15.2
- webdriver-manager 4.0.1

## ✅ Status da Integração

- ✅ **PITS (Gestão de Usuários)**: Totalmente integrado
  - CRUD completo de usuários
  - Menu, listagem, cadastro, edição e exclusão
- ✅ **Trabalho-2S**: Totalmente integrado
  - Menu, listagem de usuários, livros e empréstimos
  - Relatórios completos (livros mais emprestados, usuários mais ativos)
- ✅ **Empréstimo/Devolução**: Totalmente integrado
  - Interface de empréstimos e devoluções
  - API REST para listagem e devolução
- ✅ **Dácio**: CRUD completo integrado (com isolamento de módulos)
  - Criar, Listar, Editar e Remover livros
  - Interface completa com Bootstrap
- ✅ **Banco de dados**: Em memória (sem dependência de MongoDB)
- ✅ **Todas as rotas**: Funcionando e testadas

## 🧪 Testes de Caixa Preta (Selenium)

O projeto inclui uma suíte completa de testes de caixa preta usando Selenium WebDriver.

### Executar Testes

```bash
# Instalar dependências (inclui Selenium)
pip install -r requirements.txt

# Executar todos os testes
pytest tests/e2e/ -v

# Executar testes específicos
pytest tests/e2e/test_pits_usuarios.py -v
pytest tests/e2e/test_sistema_completo.py -v
```

### Estrutura de Testes

- `tests/e2e/test_pits_usuarios.py` - Testes do módulo PITS (Gestão de Usuários)
- `tests/e2e/test_sistema_completo.py` - Testes completos do sistema unificado (principal arquivo Selenium)
- `tests/conftest.py` - Configuração compartilhada (servidor Flask + Selenium)

**Documentação completa**: Veja `tests/README.md` para detalhes.

## 📝 Notas Técnicas

- O módulo Dácio usa um sistema de import isolado para evitar conflitos com o Model do Trabalho-2S
- O Trabalho-2S foi configurado para usar banco em memória por padrão
- Todas as rotas HTML foram convertidas para Flask templates
- Testes de caixa preta rodam em modo headless por padrão (sem interface gráfica)
- O módulo PITS foi totalmente integrado com todas as rotas CRUD funcionais

## 👥 Equipe - Grupo A

Este sistema foi desenvolvido pelo Grupo A, integrando os trabalhos de todos os membros da equipe.

