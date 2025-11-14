# 📑 Índice do Projeto - Guia de Navegação

## 🎯 Por Onde Começar?

### Se você é novo no projeto:
1. 📖 Leia [`QUICK_START.md`](QUICK_START.md) - Guia rápido de 5 minutos
2. 📁 Veja [`ESTRUTURA.md`](ESTRUTURA.md) - Entenda a organização
3. 📚 Leia [`README.md`](README.md) - Documentação completa

### Se você quer fazer algo específico:

| O Que Você Quer Fazer | Arquivo/Diretório |
|----------------------|-------------------|
| 🚀 **Começar a usar agora** | [`QUICK_START.md`](QUICK_START.md) |
| 📁 **Entender a estrutura** | [`ESTRUTURA.md`](ESTRUTURA.md) |
| 📚 **Ler documentação completa** | [`README.md`](README.md) |
| ✏️ **Modificar funcionalidades** | [`app.py`](app.py) |
| 🧪 **Ver/criar testes** | [`tests/e2e/`](tests/e2e/) |
| 📖 **Documentação dos testes** | [`tests/README.md`](tests/README.md) |
| 📦 **Adicionar dependências** | [`requirements.txt`](requirements.txt) |

---

## 📂 Estrutura Visual

```
sistema_grupo_unificado/
│
├── 📄 INDEX.md              ← Você está aqui! Guia de navegação
├── 📄 QUICK_START.md        ← Comece aqui se é novo
├── 📄 README.md             ← Documentação principal
├── 📄 ESTRUTURA.md          ← Explicação da organização
│
├── ⭐ app.py                ← ARQUIVO PRINCIPAL (edite aqui)
├── 📄 requirements.txt      ← Dependências
├── 📄 pytest.ini           ← Configuração de testes
│
└── 📁 tests/                ← Testes automatizados
    ├── 📄 README.md         ← Documentação dos testes
    ├── 📄 conftest.py       ← Configuração compartilhada
    └── 📁 e2e/              ← Testes End-to-End
        ├── test_pits_usuarios.py
        └── test_sistema_completo.py
```

---

## 🗺️ Mapa de Arquivos

### 📄 Arquivos de Documentação

| Arquivo | Propósito | Quando Ler |
|---------|-----------|------------|
| **INDEX.md** | Este arquivo - guia de navegação | Primeiro |
| **QUICK_START.md** | Guia rápido para começar | Se quer começar rápido |
| **README.md** | Documentação completa do projeto | Para referência completa |
| **ESTRUTURA.md** | Explicação detalhada da estrutura | Para entender organização |
| **tests/README.md** | Documentação dos testes | Para trabalhar com testes |

### 💻 Arquivos de Código

| Arquivo | O Que Faz | Quando Editar |
|---------|----------|---------------|
| **app.py** ⭐ | Servidor Flask unificado | Sempre que modificar funcionalidades |
| **requirements.txt** | Lista de dependências | Ao adicionar novas bibliotecas |
| **pytest.ini** | Configuração do pytest | Ao configurar testes |

### 🧪 Arquivos de Testes

| Arquivo | O Que Faz | Quando Editar |
|---------|----------|---------------|
| **tests/conftest.py** | Configuração compartilhada | Ao configurar Selenium/Flask |
| **tests/e2e/test_*.py** | Testes de caixa preta | Ao criar novos testes |

---

## 🔍 Busca Rápida

### "Onde está..."
- **...o código principal?** → `app.py`
- **...a configuração dos testes?** → `tests/conftest.py` ou `pytest.ini`
- **...os testes do PITS?** → `tests/e2e/test_pits_usuarios.py`
- **...os testes completos?** → `tests/e2e/test_sistema_completo.py`
- **...a lista de dependências?** → `requirements.txt`
- **...como executar?** → `QUICK_START.md` ou `README.md`
- **...a explicação da estrutura?** → `ESTRUTURA.md`

---

## 📚 Fluxo de Leitura Recomendado

### Para Desenvolvedores Novos:
```
1. INDEX.md (este arquivo)
   ↓
2. QUICK_START.md
   ↓
3. ESTRUTURA.md
   ↓
4. README.md (consulta)
   ↓
5. app.py (código)
```

### Para Trabalhar com Testes:
```
1. tests/README.md
   ↓
2. tests/conftest.py
   ↓
3. tests/e2e/test_*.py
```

### Para Modificar Funcionalidades:
```
1. ESTRUTURA.md (entender estrutura)
   ↓
2. app.py (editar código)
   ↓
3. tests/e2e/ (criar/atualizar testes)
```

---

## ✅ Checklist de Navegação

- [ ] Li o `INDEX.md` (este arquivo)
- [ ] Li o `QUICK_START.md` para começar
- [ ] Entendi a estrutura lendo `ESTRUTURA.md`
- [ ] Sei onde está o código principal (`app.py`)
- [ ] Sei onde estão os testes (`tests/e2e/`)
- [ ] Sei onde encontrar a documentação (`README.md`)

---

## 💡 Dicas

1. **Sempre comece pelo `QUICK_START.md`** se quer começar rápido
2. **Consulte `ESTRUTURA.md`** quando não souber onde está algo
3. **Use `README.md`** como referência completa
4. **Edite `app.py`** para modificar funcionalidades
5. **Veja `tests/README.md`** para trabalhar com testes

---

**Boa navegação! 🚀**

