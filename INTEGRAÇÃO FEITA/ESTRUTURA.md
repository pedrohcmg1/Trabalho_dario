# 📁 Estrutura do Projeto - Sistema Unificado Grupo A

## Visão Geral da Organização

Este documento explica a organização dos arquivos e diretórios do projeto.

```
sistema_grupo_unificado/
│
├── 📄 app.py                    # ⭐ ARQUIVO PRINCIPAL - Servidor Flask unificado
├── 📄 requirements.txt          # Dependências Python do projeto
├── 📄 pytest.ini               # Configuração do pytest para testes
│
├── 📄 README.md                 # Documentação principal do projeto
├── 📄 ESTRUTURA.md              # Este arquivo - explicação da estrutura
├── 📄 QUICK_START.md            # Guia rápido de início
│
└── 📁 tests/                    # Testes automatizados
    ├── 📄 __init__.py
    ├── 📄 conftest.py           # Configuração compartilhada (Selenium + Flask)
    │
    └── 📁 e2e/                  # Testes End-to-End (Caixa Preta)
        ├── 📄 __init__.py
        ├── 📄 test_pits_usuarios.py      # Testes do módulo PITS
        └── 📄 test_sistema_completo.py   # Testes completos do sistema (Selenium)
```

## 📄 Descrição dos Arquivos Principais

### `app.py` ⭐
**O que faz**: Arquivo principal da aplicação Flask unificada.

**Conteúdo**:
- Integra os 4 projetos (PITS, Trabalho-2S, Empréstimo/Devolução, Dácio)
- Define todas as rotas da aplicação
- Configura serviços e controladores
- Inicia o servidor na porta 5050

**Como usar**: Execute `python app.py` para iniciar o servidor.

---

### `requirements.txt`
**O que faz**: Lista todas as dependências Python necessárias.

**Conteúdo**:
- Flask (framework web)
- Selenium (testes automatizados)
- pytest (framework de testes)
- Outras bibliotecas necessárias

**Como usar**: Execute `pip install -r requirements.txt` para instalar tudo.

---

### `pytest.ini`
**O que faz**: Configuração do pytest para executar os testes.

**Conteúdo**:
- Diretórios onde procurar testes
- Opções padrão de execução
- Marcadores customizados

**Como usar**: Execute `pytest` e ele usará essas configurações automaticamente.

---

## 📁 Descrição dos Diretórios

### `tests/` - Testes Automatizados

#### `tests/conftest.py`
**O que faz**: Configuração compartilhada para todos os testes.

**Conteúdo**:
- **Fixture `flask_server`**: Inicia o servidor Flask automaticamente
- **Fixture `driver`**: Cria e configura o Selenium WebDriver
- **Fixture `base_url`**: URL base do servidor (http://127.0.0.1:5050)
- **Fixture `wait`**: Helper para esperas explícitas no Selenium

**Como usar**: As fixtures são usadas automaticamente pelos testes.

---

#### `tests/e2e/` - Testes End-to-End (Caixa Preta)

**O que faz**: Testes que verificam o sistema através da interface web, sem conhecer a implementação interna.

##### `test_pits_usuarios.py`
**O que testa**: Módulo PITS (Gestão de Usuários)
- ✅ Página inicial e menu
- ✅ Listagem de usuários
- ✅ Cadastro de usuários
- ✅ Navegação entre páginas

##### `test_sistema_completo.py` ⭐
**O que testa**: Sistema Unificado Completo (Principal arquivo de testes Selenium)
- ✅ Página inicial e links
- ✅ Todos os módulos integrados (PITS, Trabalho-2S, Empréstimo, Dácio)
- ✅ Navegação entre módulos
- ✅ APIs REST
- ✅ Páginas de listagem e relatórios
- ✅ Integração completa do sistema

**Como usar**: Execute `pytest tests/e2e/ -v` para rodar todos os testes.

---

## 🔄 Fluxo de Trabalho

### 1. Desenvolvimento
```
1. Editar app.py para adicionar/modificar funcionalidades
2. Testar manualmente acessando http://127.0.0.1:5050
3. Executar testes automatizados: pytest tests/e2e/ -v
```

### 2. Testes
```
1. Os testes iniciam o servidor Flask automaticamente
2. O Selenium abre o navegador (headless) e testa as páginas
3. Os testes verificam se tudo funciona corretamente
```

### 3. Estrutura de Dados
```
app.py
  ├── Importa módulos dos 4 projetos
  ├── Configura serviços (mocks, controllers)
  ├── Define rotas Flask
  └── Inicia servidor

tests/
  ├── conftest.py (configuração)
  └── e2e/ (testes de caixa preta)
      ├── test_pits_usuarios.py
      └── test_sistema_completo.py (principal)
```

## 🎯 Onde Encontrar o Quê

| O que você quer fazer | Arquivo/Diretório |
|----------------------|-------------------|
| **Adicionar nova rota** | `app.py` |
| **Modificar funcionalidade** | `app.py` |
| **Adicionar dependência** | `requirements.txt` |
| **Criar novo teste** | `tests/e2e/test_*.py` |
| **Configurar testes** | `tests/conftest.py` ou `pytest.ini` |
| **Ver documentação** | `README.md` |
| **Entender estrutura** | `ESTRUTURA.md` (este arquivo) |

## 📚 Arquivos de Documentação

- **`README.md`**: Documentação principal - como usar, rotas, instalação
- **`ESTRUTURA.md`**: Este arquivo - explicação da organização
- **`QUICK_START.md`**: Guia rápido de início

## 🔍 Dicas de Navegação

1. **Comece pelo `README.md`** para entender o projeto
2. **Veja `ESTRUTURA.md`** (este arquivo) para entender a organização
3. **Edite `app.py`** para modificar funcionalidades
4. **Veja `tests/e2e/`** para entender como os testes funcionam
5. **Consulte `QUICK_START.md`** para começar rapidamente

## ✅ Checklist de Entendimento

- [ ] Entendi que `app.py` é o arquivo principal
- [ ] Sei onde adicionar novas rotas (`app.py`)
- [ ] Sei onde criar novos testes (`tests/e2e/`)
- [ ] Entendi a estrutura de diretórios
- [ ] Sei onde encontrar a documentação
- [ ] Sei que `test_sistema_completo.py` é o principal arquivo de testes Selenium

