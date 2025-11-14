# 🚀 Quick Start - Guia Rápido

## Para Começar Agora (5 minutos)

### 1️⃣ Instalar Dependências
```bash
cd "/Users/marcoscardoso/Desktop/GRUPOS A/sistema_grupo_unificado"
pip install -r requirements.txt
```

### 2️⃣ Executar a Aplicação
```bash
python app.py
```

### 3️⃣ Acessar no Navegador
Abra: **http://127.0.0.1:5050**

---

## 📋 O Que Você Vai Ver

### Página Inicial (`/`)
- Links para os 4 módulos integrados
- Navegação para todas as seções

### PITS - Gestão de Usuários (`/pits/*`)
- Menu principal
- Listagem de usuários
- Cadastro, edição e exclusão de usuários

### Trabalho-2S (`/t2s/*`)
- Menu principal
- Listagem de usuários, livros, empréstimos
- Relatórios e analytics

### Empréstimo/Devolução (`/emprestimos`, `/devolucoes`)
- Interface de empréstimos
- Interface de devoluções
- API REST

### Dácio (`/dacio/*`)
- CRUD completo de livros
- Cadastrar, listar, editar, remover

---

## 🧪 Executar Testes

```bash
# Todos os testes
pytest tests/e2e/ -v

# Testes específicos
pytest tests/e2e/test_pits_usuarios.py -v
pytest tests/e2e/test_sistema_completo.py -v
```

---

## 📚 Próximos Passos

1. **Ler documentação completa**: [`README.md`](README.md)
2. **Entender estrutura**: [`ESTRUTURA.md`](ESTRUTURA.md)
3. **Ver testes**: `tests/e2e/test_sistema_completo.py` (principal arquivo Selenium)

---

## ❓ Problemas Comuns

### Porta 5050 já em uso
```bash
# Encontrar processo usando a porta
lsof -ti:5050

# Encerrar processo
kill -9 $(lsof -ti:5050)
```

### Erro ao instalar dependências
```bash
# Atualizar pip
pip install --upgrade pip

# Instalar novamente
pip install -r requirements.txt
```

### Testes não funcionam
- Certifique-se de que o Chrome está instalado
- O webdriver-manager baixa o ChromeDriver automaticamente
- Verifique se a porta 5050 está livre

---

## 🎯 Arquivos Importantes

| Arquivo | Para Que Serve |
|---------|---------------|
| `app.py` | ⭐ Arquivo principal - edite aqui para modificar |
| `requirements.txt` | Dependências do projeto |
| `README.md` | Documentação completa |
| `ESTRUTURA.md` | Explicação da organização |
| `tests/e2e/test_sistema_completo.py` | ⭐ Principal arquivo de testes Selenium |
| `tests/` | Testes automatizados |

---

**Pronto!** Agora você pode começar a usar o sistema. 🎉

