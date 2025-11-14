# Testes de Caixa Preta com Selenium

## 📋 Visão Geral

Este diretório contém testes de **caixa preta (black box testing)** usando Selenium WebDriver. Os testes verificam o comportamento da aplicação através da interface web, sem conhecer a implementação interna.

## 🎯 Estratégia de Testes

### O que são Testes de Caixa Preta?

Testes de caixa preta testam o sistema apenas através de suas interfaces (neste caso, a interface web), sem conhecer a implementação interna. Focamos em:

- ✅ **Funcionalidade**: O sistema faz o que deveria fazer?
- ✅ **Interface**: As páginas carregam corretamente?
- ✅ **Navegação**: Os links e botões funcionam?
- ✅ **APIs**: As APIs retornam dados válidos?

### Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py          # Configuração compartilhada (fixtures)
├── e2e/                 # Testes End-to-End (Caixa Preta)
│   ├── __init__.py
│   ├── test_pits_usuarios.py      # Testes do módulo PITS
│   └── test_sistema_completo.py   # Testes completos do sistema (principal)
└── README.md            # Este arquivo
```

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
cd "/Users/marcoscardoso/Desktop/GRUPOS A/sistema_grupo_unificado"
pip install -r requirements.txt
```

Isso instalará:
- `selenium` - Framework de automação web
- `webdriver-manager` - Gerenciamento automático de drivers
- `pytest` - Framework de testes

### 2. Executar Todos os Testes

```bash
pytest tests/e2e/ -v
```

### 3. Executar Testes Específicos

```bash
# Apenas testes do PITS
pytest tests/e2e/test_pits_usuarios.py -v

# Apenas testes completos do sistema
pytest tests/e2e/test_sistema_completo.py -v
```

### 4. Executar com Relatório Detalhado

```bash
pytest tests/e2e/ -v --tb=long
```

## 🔧 Configuração

### Modo Headless (sem interface gráfica)

Por padrão, os testes rodam em modo **headless** (sem abrir janela do navegador). Isso está configurado em `conftest.py`:

```python
chrome_options.add_argument("--headless")
```

Para ver o navegador durante os testes, comente essa linha em `conftest.py`.

### Porta do Servidor

O servidor Flask inicia automaticamente na porta **5050** durante os testes. Certifique-se de que essa porta está livre.

## 📝 Testes Implementados

### PITS - Gestão de Usuários (`test_pits_usuarios.py`)

- ✅ Página inicial com links
- ✅ Menu principal
- ✅ Listagem de usuários
- ✅ Cadastro de usuários
- ✅ Navegação entre páginas

### Sistema Completo (`test_sistema_completo.py`) ⭐

- ✅ Página inicial e links
- ✅ Todos os módulos integrados (PITS, Trabalho-2S, Empréstimo, Dácio)
- ✅ Navegação entre módulos
- ✅ APIs REST
- ✅ Páginas de listagem e relatórios
- ✅ Integração completa do sistema

## 🐛 Solução de Problemas

### Erro: "ChromeDriver not found"

O `webdriver-manager` baixa automaticamente o ChromeDriver. Se houver problemas:

```bash
pip install --upgrade webdriver-manager
```

### Erro: "Port 5050 already in use"

Certifique-se de que não há outra instância do app rodando:

```bash
# No macOS/Linux
lsof -ti:5050 | xargs kill -9

# Ou simplesmente feche a aplicação que está usando a porta
```

### Testes falhando por timeout

Aumente o timeout em `conftest.py`:

```python
driver.implicitly_wait(20)  # Aumentar de 10 para 20 segundos
```

## 📊 Cobertura de Testes

Os testes de caixa preta cobrem:

- ✅ **Navegação**: Todas as rotas principais
- ✅ **Carregamento**: Todas as páginas carregam corretamente
- ✅ **APIs**: Endpoints JSON retornam dados válidos
- ✅ **Formulários**: Submissão de formulários funciona
- ✅ **Links**: Navegação entre páginas

## 🔄 Adicionando Novos Testes

Para adicionar novos testes de caixa preta:

1. Crie um novo arquivo em `tests/e2e/` ou adicione ao arquivo existente
2. Use as fixtures do `conftest.py`:
   - `driver`: WebDriver do Selenium
   - `base_url`: URL base do servidor
   - `wait`: WebDriverWait para esperas explícitas

Exemplo:

```python
def test_nova_funcionalidade(driver, base_url, wait):
    driver.get(f"{base_url}/nova_rota")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    # Seus testes aqui...
```

## 📚 Recursos

- [Documentação Selenium](https://www.selenium.dev/documentation/)
- [Documentação Pytest](https://docs.pytest.org/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)

