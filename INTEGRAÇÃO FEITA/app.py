from flask import Flask, jsonify, render_template_string, send_from_directory, request, redirect
import os
import sys

# Paths dos projetos existentes
ROOT = "/Users/marcoscardoso/Desktop/GRUPOS A"
PROJ_PITS = os.path.join(ROOT, "Atividade_PITS-main")
PROJ_TRAB2 = os.path.join(ROOT, "Trabalho-2S-master")
PROJ_EMP = os.path.join(ROOT, "Empr-stimo-e-Devolu-o-main", "src")
PROJ_DACIO = os.path.join(ROOT, "TrabalhoProfDacioIntegracoes-main")

# Garantir que possamos importar módulos dos projetos
for p in [PROJ_PITS, PROJ_TRAB2, os.path.join(PROJ_TRAB2, "src"), PROJ_EMP, PROJ_DACIO]:
    if p not in sys.path:
        sys.path.append(p)

# Importar serviços/controladores existentes
from emprestimo.service import LoanService  # do projeto de empréstimo/devolução (Flask)

# Controller e Model do Trabalho-2S
from Controller.controller import Controller as T2SController  # interface limpa
from Model import model as t2s_model
from src.report_service import ReportService

# Controller do PITS (Atividade_PITS-main)
PITS_AVAILABLE = False
pits_controller = None
def _load_pits_controller():
    global PITS_AVAILABLE, pits_controller
    try:
        # Mudar para o diretório do PITS temporariamente para importar
        import importlib.util
        ctrl_path = os.path.join(PROJ_PITS, "controler.py")
        ctrl_spec = importlib.util.spec_from_file_location("pits_controller", ctrl_path)
        pits_ctrl = importlib.util.module_from_spec(ctrl_spec)
        assert ctrl_spec and ctrl_spec.loader
        ctrl_spec.loader.exec_module(pits_ctrl)  # type: ignore
        pits_controller = pits_ctrl.Controler(True)
        PITS_AVAILABLE = True
    except Exception as e:
        print(f"Erro ao carregar controller PITS: {e}")
        import traceback
        traceback.print_exc()
        PITS_AVAILABLE = False

_load_pits_controller()

# Controller do Dácio
DACIO_AVAILABLE = False
dacio_controller = None
def _load_dacio_controller():
    global DACIO_AVAILABLE, dacio_controller
    try:
        import importlib.util, types
        # 1) Carrega Model.book do Dácio sob alias isolado
        book_path = os.path.join(PROJ_DACIO, "Model", "book.py")
        book_spec = importlib.util.spec_from_file_location("dacio_model_book", book_path)
        book_module = importlib.util.module_from_spec(book_spec)
        assert book_spec and book_spec.loader
        book_spec.loader.exec_module(book_module)  # type: ignore

        # 2) Injeta um pacote fake 'Model' temporário com submódulo 'book'
        fake_pkg = types.SimpleNamespace()
        fake_pkg.__path__ = [os.path.join(PROJ_DACIO, "Model")]  # type: ignore[attr-defined]
        sys.modules["Model"] = fake_pkg  # type: ignore
        sys.modules["Model.book"] = book_module

        # 3) Importa o controller do Dácio que faz 'from Model.book import Book'
        ctrl_path = os.path.join(PROJ_DACIO, "controller.py")
        ctrl_spec = importlib.util.spec_from_file_location("dacio_controller", ctrl_path)
        dacio_controller = importlib.util.module_from_spec(ctrl_spec)
        assert ctrl_spec and ctrl_spec.loader
        ctrl_spec.loader.exec_module(dacio_controller)  # type: ignore

        DACIO_AVAILABLE = True
    except Exception as e:
        print(f"Erro ao carregar controller Dácio: {e}")
        DACIO_AVAILABLE = False
    finally:
        # 4) Remove o pacote fake para não conflitar com o Model do Trabalho-2S
        if "Model.book" in sys.modules:
            del sys.modules["Model.book"]
        if "Model" in sys.modules and getattr(sys.modules["Model"], "__name__", "") != "Model":
            del sys.modules["Model"]

_load_dacio_controller()


app = Flask(__name__)


# ============== Adaptação do projeto Empr-stimo-e-Devolu-o (Flask) ==============
class MockUserService:
    def __init__(self):
        self.users = {
            1: {"id": 1, "name": "Alice", "active": True},
            2: {"id": 2, "name": "Bob", "active": True},
        }

    def get_user(self, user_id: int):
        return self.users.get(user_id)

    def is_active(self, user_id: int) -> bool:
        user = self.users.get(user_id)
        return user.get("active", False) if user else False


class MockCatalogService:
    def __init__(self):
        self.books = {
            1: {"id": 1, "title": "1984", "available": True},
            2: {"id": 2, "title": "Dom Casmurro", "available": True},
        }

    def get_book(self, book_id: int):
        return self.books.get(book_id)

    def is_available(self, book_id: int) -> bool:
        book = self.books.get(book_id)
        return book.get("available", False) if book else False

    def mark_loaned(self, book_id: int):
        if book_id in self.books:
            self.books[book_id]["available"] = False

    def mark_available(self, book_id: int):
        if book_id in self.books:
            self.books[book_id]["available"] = True


user_service = MockUserService()
catalog_service = MockCatalogService()
loan_service = LoanService(user_service, catalog_service)


@app.get("/")
def home():
    # Página de entrada com links para seções integradas
    return render_template_string(
        """
        <!doctype html>
        <html lang=pt-BR><head><meta charset=utf-8><title>Sistema Unificado - Grupo A</title>
        <style>
        body{font-family:system-ui,Arial;margin:40px;background:#f5f5f5}
        h1{color:#333;border-bottom:3px solid #4CAF50;padding-bottom:10px}
        h3{color:#666;margin-top:30px;margin-bottom:15px}
        a{display:block;margin:8px 0;padding:10px;background:white;border-left:4px solid #4CAF50;text-decoration:none;color:#333;border-radius:4px}
        a:hover{background:#e8f5e9;border-left-color:#2E7D32}
        </style>
        </head><body>
        <h1>🚀 Sistema Unificado - Grupo A</h1>
        <h3>👥 Gestão de Usuários (PITS)</h3>
        <a href="/pits/menu">Menu Usuários</a>
        <a href="/pits/usuarios">Listar Usuários</a>
        <a href="/pits/cadastrar_usuario">Cadastrar Usuário</a>
        <h3>📚 Catálogo/Usuários/Relatórios (Trabalho-2S)</h3>
        <a href="/t2s/menu">Menu</a>
        <a href="/t2s/listar_usuarios">Listar usuários</a>
        <a href="/t2s/listar_livros">Listar livros</a>
        <a href="/t2s/listar_emprestimos">Listar empréstimos</a>
        <a href="/t2s/relatorios">Relatórios</a>
        <h3>📖 Empréstimo/Devolução (Projeto Flask)</h3>
        <a href="/emprestimos">Página Empréstimos</a>
        <a href="/devolucoes">Página Devoluções</a>
        <a href="/api/loans">API Loans</a>
        <h3>📝 CRUD Livros (Dácio)</h3>
        <a href="/dacio/menu">Menu Livros</a>
        <a href="/dacio/listar_livros">Listar Livros</a>
        <a href="/dacio/cadastrar_livro">Cadastrar Livro</a>
        </body></html>
        """
    )


# ===== Seção: PITS - Gestão de Usuários =====
def _read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/pits/menu")
def pits_menu():
    if not PITS_AVAILABLE:
        return "Módulo PITS indisponível nesta execução.", 503
    html_path = os.path.join(PROJ_PITS, "View_and_Interface", "menu.html")
    return render_template_string(_read_file(html_path))


@app.get("/pits/usuarios")
def pits_usuarios():
    if not PITS_AVAILABLE or not pits_controller:
        return "Módulo PITS indisponível nesta execução.", 503
    html_path = os.path.join(PROJ_PITS, "View_and_Interface", "usuarios.html")
    conteudo = _read_file(html_path)
    # Substituir URLs para funcionar no contexto unificado
    conteudo = conteudo.replace("/cadastrar_usuario", "/pits/cadastrar_usuario")
    conteudo = conteudo.replace("/editar_usuario", "/pits/editar_usuario")
    conteudo = conteudo.replace("/listar_usuarios", "/pits/listar_usuarios")
    conteudo = conteudo.replace("/excluir_usuario", "/pits/excluir_usuario")
    conteudo = conteudo.replace("/menu", "/pits/menu")
    return render_template_string(conteudo)


@app.get("/pits/cadastrar_usuario")
def pits_cadastrar_usuario():
    if not PITS_AVAILABLE:
        return "Módulo PITS indisponível nesta execução.", 503
    html_path = os.path.join(PROJ_PITS, "View_and_Interface", "cadastrar_usuario.html")
    conteudo = _read_file(html_path)
    conteudo = conteudo.replace("/criar_usuario", "/pits/criar_usuario")
    conteudo = conteudo.replace("/menu", "/pits/menu")
    conteudo = conteudo.replace("/usuarios", "/pits/usuarios")
    return render_template_string(conteudo)


@app.get("/pits/editar_usuario")
def pits_editar_usuario():
    if not PITS_AVAILABLE or not pits_controller:
        return "Módulo PITS indisponível nesta execução.", 503
    html_path = os.path.join(PROJ_PITS, "View_and_Interface", "editar_usuario.html")
    conteudo = _read_file(html_path)
    usuario_id = request.args.get("id", "")
    
    if usuario_id:
        usuario = pits_controller.Ctr_Buscar_Usuario_Por_Id(int(usuario_id))
        if usuario:
            def _esc(v):
                from html import escape
                return escape("" if v is None else str(v))
            conteudo = conteudo.replace("<!--ID-->", _esc(str(usuario.get_id())))
            conteudo = conteudo.replace("<!--NOME-->", _esc(usuario.get_nome()))
            conteudo = conteudo.replace("<!--MATRICULA-->", _esc(usuario.get_matricula()))
            conteudo = conteudo.replace("<!--TIPO-->", _esc(usuario.get_tipo()))
            conteudo = conteudo.replace("<!--EMAIL-->", _esc(usuario.get_email() or ""))
            conteudo = conteudo.replace("<!--STATUS-->", _esc(usuario.get_status()))
    
    conteudo = conteudo.replace("/atualizar_usuario", "/pits/atualizar_usuario")
    conteudo = conteudo.replace("/buscar_usuario", "/pits/buscar_usuario")
    conteudo = conteudo.replace("/menu", "/pits/menu")
    conteudo = conteudo.replace("/usuarios", "/pits/usuarios")
    return render_template_string(conteudo)


@app.get("/pits/listar_usuarios")
def pits_listar_usuarios():
    if not PITS_AVAILABLE or not pits_controller:
        return "Módulo PITS indisponível nesta execução.", 503
    usuarios = pits_controller.Ctr_Listar_Usuarios()
    
    def _esc(v):
        from html import escape
        return escape("" if v is None else str(v))
    
    resposta = ""
    for usuario in usuarios:
        status_class = f"status-{usuario.get_status().lower()}"
        tipo_class = f"tipo-{usuario.get_tipo().lower()}"
        resposta += f'''
        <tr>
            <td>{usuario.get_id()}</td>
            <td>{_esc(usuario.get_nome())}</td>
            <td>{_esc(usuario.get_matricula())}</td>
            <td><span class="{tipo_class}">{_esc(usuario.get_tipo())}</span></td>
            <td>{_esc(usuario.get_email() or '')}</td>
            <td><span class="{status_class}">{_esc(usuario.get_status())}</span></td>
            <td>{_esc(usuario.get_ativoDeRegistro())}</td>
            <td>
                <a href="/pits/editar_usuario?id={usuario.get_id()}" class="btn btn-warning">Editar</a>
                <button onclick="excluirUsuario({usuario.get_id()})" class="btn btn-danger">Excluir</button>
            </td>
        </tr>
        '''
    return resposta


@app.post("/pits/criar_usuario")
def pits_criar_usuario():
    if not PITS_AVAILABLE or not pits_controller:
        return "Módulo PITS indisponível nesta execução.", 503
    nome = request.form.get("nome", "")
    matricula = request.form.get("matricula", "")
    tipo = request.form.get("tipo", "")
    email = request.form.get("email", "") or None
    
    sucesso, resultado = pits_controller.Ctr_Criar_Usuario(nome, matricula, tipo, email)
    
    if sucesso:
        return redirect("/pits/usuarios")
    else:
        return f"Erro: {resultado}", 400


@app.post("/pits/atualizar_usuario")
def pits_atualizar_usuario():
    if not PITS_AVAILABLE or not pits_controller:
        return "Módulo PITS indisponível nesta execução.", 503
    id_usuario = int(request.form.get("id", 0))
    nome = request.form.get("nome", "")
    matricula = request.form.get("matricula", "")
    tipo = request.form.get("tipo", "")
    email = request.form.get("email", "") or None
    status = request.form.get("status", "")
    
    sucesso, resultado = pits_controller.Ctr_Atualizar_Usuario(id_usuario, nome, matricula, tipo, email, status)
    
    if sucesso:
        return redirect("/pits/usuarios")
    else:
        return f"Erro: {resultado}", 400


@app.post("/pits/excluir_usuario")
def pits_excluir_usuario():
    if not PITS_AVAILABLE or not pits_controller:
        return "Módulo PITS indisponível nesta execução.", 503
    id_usuario = int(request.form.get("id", 0))
    sucesso, resultado = pits_controller.Ctr_Excluir_Usuario(id_usuario)
    
    if sucesso:
        return redirect("/pits/usuarios")
    else:
        return f"Erro: {resultado}", 400


@app.get("/pits/buscar_usuario")
def pits_buscar_usuario():
    if not PITS_AVAILABLE or not pits_controller:
        return jsonify({"erro": "Módulo PITS indisponível"}), 503
    usuario_id = int(request.args.get("id", 0))
    usuario = pits_controller.Ctr_Buscar_Usuario_Por_Id(usuario_id)
    
    if usuario:
        return jsonify(usuario.to_dict())
    else:
        return jsonify({"erro": "Usuário não encontrado"}), 404


# ===== Seção: Empr-stimo-e-Devolu-o (reuso das rotas principais) =====
@app.get("/emprestimos")
def emprestimos_page():
    templates_dir = os.path.join(PROJ_EMP, "interface", "templates")
    html_content = _read_file(os.path.join(templates_dir, "emprestimo.html"))
    # Ajustar URLs para funcionar no contexto unificado
    import re
    html_content = re.sub(r"\{\{ url_for\('static', filename='([^']+)'\) \}\}", r'/static/emprestimo/\1', html_content)
    html_content = html_content.replace("{{ url_for('index') }}", '/')
    return render_template_string(html_content)


@app.get("/devolucoes")
def devolucoes_page():
    templates_dir = os.path.join(PROJ_EMP, "interface", "templates")
    html_content = _read_file(os.path.join(templates_dir, "devolucoes.html"))
    # Ajustar URLs para funcionar no contexto unificado
    import re
    html_content = re.sub(r"\{\{ url_for\('static', filename='([^']+)'\) \}\}", r'/static/emprestimo/\1', html_content)
    html_content = html_content.replace("{{ url_for('index') }}", '/')
    return render_template_string(html_content)


# Rotas para servir arquivos estáticos (CSS/JS) do projeto Empréstimo
@app.get("/static/emprestimo/<path:filename>")
def static_emprestimo(filename):
    static_dir = os.path.join(PROJ_EMP, "interface", "static")
    return send_from_directory(static_dir, filename)


@app.get("/api/loans")
def api_get_loans():
    return jsonify(loan_service.list_loans())


@app.post("/api/loans/<int:loan_id>/return")
def api_return_loan(loan_id: int):
    return jsonify(loan_service.return_book(loan_id))


# ===== Seção: Trabalho-2S (port das views para Flask) =====
t2s_controller = T2SController(login_required=False)
t2s_report_service = ReportService()


@app.get("/t2s/menu")
def t2s_menu():
    html_path = os.path.join(PROJ_TRAB2, "View_and_Interface", "menu.html")
    return render_template_string(_read_file(html_path))


@app.get("/t2s/listar_usuarios")
def t2s_listar_usuarios():
    usuarios = t2s_controller.get_usuarios()
    conteudo_path = os.path.join(PROJ_TRAB2, "View_and_Interface", "listar_usuarios.html")
    conteudo = _read_file(conteudo_path)
    bloco = []
    for u in usuarios:
        if u.id and u.name and u.email and u.type:
            bloco.append(f"<div><strong>{u.name}</strong> — {u.email} ({u.type})</div>")
    html = conteudo.replace("<!--USUARIOS-->", "".join(bloco) or "<div>Nenhum usuário.</div>")
    return render_template_string(html)


@app.get("/t2s/listar_livros")
def t2s_listar_livros():
    livros = t2s_controller.get_livros()
    conteudo_path = os.path.join(PROJ_TRAB2, "View_and_Interface", "listar_livros.html")
    conteudo = _read_file(conteudo_path)
    bloco = []
    for l in livros:
        if l.id and l.title and l.author and l.isbn:
            bloco.append(
                f"<div class='book-card'><h3>{l.title}</h3><div>Autor: {l.author}</div><div>ISBN: {l.isbn}</div></div>"
            )
    html = conteudo.replace("<!--LIVROS-->", "".join(bloco) or "<div>Nenhum livro.</div>")
    return render_template_string(html)


@app.get("/t2s/listar_emprestimos")
def t2s_listar_emprestimos():
    emprestimos = t2s_controller.get_emprestimos()
    livros = {l.id: l for l in t2s_controller.get_livros()}
    usuarios = {u.id: u for u in t2s_controller.get_usuarios()}
    conteudo_path = os.path.join(PROJ_TRAB2, "View_and_Interface", "listar_emprestimos.html")
    conteudo = _read_file(conteudo_path)
    bloco = []
    for e in emprestimos:
        l = livros.get(e.book_id)
        u = usuarios.get(e.user_id)
        if l and u:
            bloco.append(
                f"<div class='loan-card'><h3>{l.title}</h3><div>Usuário: {u.name}</div></div>"
            )
    html = conteudo.replace("<!--EMPRESTIMOS-->", "".join(bloco) or "<div>Nenhum empréstimo.</div>")
    return render_template_string(html)


@app.get("/t2s/relatorios")
def t2s_relatorios():
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatórios Executivos - Sistema de Biblioteca</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,sans-serif;background:#f8fafc;min-height:100vh;color:#1e293b;padding:20px}
.header{background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:50px 20px;text-align:center;margin-bottom:40px;box-shadow:0 4px 6px -1px rgba(0,0,0,0.1)}
.header h1{font-size:2.5em;font-weight:700;margin-bottom:12px;letter-spacing:-0.025em}
.header p{font-size:1.125em;opacity:0.9;font-weight:400}
.container{max-width:1000px;margin:0 auto;background:white;border-radius:16px;padding:50px;box-shadow:0 10px 25px -5px rgba(0,0,0,0.1),0 10px 10px -5px rgba(0,0,0,0.04);border:1px solid #e2e8f0}
.reports-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:30px;margin:40px 0}
.report-card{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:32px;text-align:center;transition:all 0.2s ease;box-shadow:0 1px 3px 0 rgba(0,0,0,0.1)}
.report-card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.15);border-color:#3b82f6}
.report-card-icon{font-size:3em;margin-bottom:20px;display:block;color:#3b82f6}
.report-card h3{font-size:1.5em;font-weight:600;margin-bottom:16px;color:#1e293b;letter-spacing:-0.025em}
.report-card p{color:#64748b;margin-bottom:24px;line-height:1.6;font-weight:400}
.report-card a{display:inline-flex;align-items:center;gap:8px;padding:12px 20px;background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white;text-decoration:none;border-radius:8px;font-weight:500;transition:all 0.2s;box-shadow:0 1px 3px 0 rgba(59,130,246,0.3)}
.report-card a:hover{background:linear-gradient(135deg,#1d4ed8,#1e40af);transform:translateY(-1px);box-shadow:0 4px 12px rgba(59,130,246,0.4)}
.back-btn{display:inline-flex;align-items:center;gap:8px;margin-top:40px;padding:12px 24px;background:#64748b;color:white;text-decoration:none;border-radius:8px;font-weight:500;transition:all 0.2s}
.back-btn:hover{background:#475569;transform:translateY(-1px)}
@media(max-width:768px){.container{padding:30px 20px}.reports-grid{grid-template-columns:1fr;gap:24px}.header{padding:40px 20px}.header h1{font-size:2em}}
</style>
</head>
<body>
<div class="header">
<h1>Relatórios e Analytics</h1>
<p>Análises estatísticas e métricas do sistema bibliotecário</p>
</div>
<div class="container">
<div class="reports-grid">
<div class="report-card">
<span class="report-card-icon"><i class="fas fa-book"></i></span>
<h3>Análise de Acervo</h3>
<p>Relatório detalhado dos livros mais emprestados, identificando tendências de demanda e preferências dos usuários.</p>
<a href="/t2s/relatorios_livros"><i class="fas fa-chart-line"></i> Ver Relatório de Livros</a>
</div>
<div class="report-card">
<span class="report-card-icon"><i class="fas fa-users"></i></span>
<h3>Perfil dos Usuários</h3>
<p>Métricas sobre o comportamento dos usuários, destacando os mais ativos e padrões de utilização.</p>
<a href="/t2s/relatorios_usuarios"><i class="fas fa-chart-bar"></i> Ver Relatório de Usuários</a>
</div>
</div>
<div style="text-align:center">
<a href="/t2s/menu" class="back-btn"><i class="fas fa-arrow-left"></i> Retornar ao Portal</a>
</div>
</div>
</body>
</html>"""
    return render_template_string(html)


@app.get("/t2s/relatorios_livros")
def t2s_relatorios_livros():
    emprestimos = t2s_controller.get_emprestimos()
    livros = t2s_controller.get_livros()
    relatorio_livros = t2s_report_service.get_most_borrowed_books(emprestimos, livros)
    
    def _esc(v):
        from html import escape
        return escape("" if v is None else str(v))
    
    tabela = ""
    if relatorio_livros:
        tabela = "<table><thead><tr><th>Posição</th><th>Título do Livro</th><th>Autor</th><th>Total de Empréstimos</th></tr></thead><tbody>"
        for i, livro in enumerate(relatorio_livros, 1):
            titulo = livro.get('title', f'ID: {livro.get("book_id", "N/A")}')
            autor = livro.get('author', 'N/A')
            emprestimos_count = livro.get('loan_count', 0)
            tabela += f'<tr><td><span class="position-badge">{i}</span></td>'
            tabela += f'<td><div class="book-info"><div class="book-details"><h4>{_esc(titulo)}</h4><p>Livro técnico</p></div></div></td>'
            tabela += f'<td>{_esc(autor)}</td>'
            tabela += f'<td><span class="loans-count">{emprestimos_count}</span></td></tr>'
        tabela += "</tbody></table>"
    else:
        tabela = '<div class="no-data"><p>Nenhum empréstimo registrado no sistema ainda.</p><p>Os dados aparecerão aqui após a realização dos primeiros empréstimos.</p></div>'
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Análise de Acervo - Sistema de Biblioteca</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Inter,sans-serif;background:#f8fafc;min-height:100vh;color:#1e293b;padding:20px}}
.header{{background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:50px 20px;text-align:center;margin-bottom:40px;box-shadow:0 4px 6px -1px rgba(0,0,0,0.1)}}
.header h1{{font-size:2.5em;font-weight:700;margin-bottom:12px;letter-spacing:-0.025em}}
.header p{{font-size:1.125em;opacity:0.9;font-weight:400}}
.container{{max-width:1200px;margin:0 auto;background:white;border-radius:16px;padding:50px;box-shadow:0 10px 25px -5px rgba(0,0,0,0.1),0 10px 10px -5px rgba(0,0,0,0.04);border:1px solid #e2e8f0}}
.report-title{{text-align:center;margin-bottom:40px}}
.report-title h1{{font-size:2em;font-weight:600;color:#1e293b;margin-bottom:8px;letter-spacing:-0.025em}}
.report-title p{{color:#64748b;font-size:1em;font-weight:400}}
table{{width:100%;border-collapse:collapse;margin:30px 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.05)}}
thead{{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white}}
th,td{{padding:16px 20px;text-align:left;border-bottom:1px solid #e5e7eb}}
tbody tr:hover{{background:#f8fafc}}
tbody tr:nth-child(even){{background:#f9fafb}}
.position-badge{{display:inline-block;width:40px;height:40px;background:linear-gradient(135deg,#f59e0b,#d97706);color:white;border-radius:50%;text-align:center;line-height:40px;font-weight:700;margin-right:16px}}
.book-info{{display:flex;align-items:center}}
.book-details h4{{margin:0 0 4px 0;font-weight:600;color:#1e293b;font-size:1em}}
.book-details p{{margin:0;color:#64748b;font-size:0.875em}}
.loans-count{{font-weight:700;color:#3b82f6;text-align:center;font-size:1.125em}}
.no-data{{text-align:center;color:#64748b;padding:60px 40px;border:2px dashed #e2e8f0;border-radius:12px;margin:40px 0;background:#f8fafc}}
.actions{{text-align:center;margin-top:40px}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:500;transition:all 0.2s;margin:0 8px}}
.btn-primary{{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white;box-shadow:0 1px 3px 0 rgba(59,130,246,0.3)}}
.btn-primary:hover{{background:linear-gradient(135deg,#1d4ed8,#1e40af);transform:translateY(-1px);box-shadow:0 4px 12px rgba(59,130,246,0.4)}}
.btn-secondary{{background:#64748b;color:white}}
.btn-secondary:hover{{background:#475569;transform:translateY(-1px)}}
@media(max-width:768px){{.container{{padding:30px 20px}}.header{{padding:40px 20px}}.header h1{{font-size:2em}}table{{font-size:0.875em}}th,td{{padding:12px 16px}}}}
</style>
</head>
<body>
<div class="header">
<h1>Análise de Acervo</h1>
<p>Relatório de livros mais emprestados</p>
</div>
<div class="container">
<div class="report-title">
<h1>Ranking de Popularidade</h1>
<p>Métricas de demanda por título bibliográfico</p>
</div>
{tabela}
<div class="actions">
<a href="/t2s/relatorios" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Retornar aos Relatórios</a>
<a href="/t2s/menu" class="btn btn-primary"><i class="fas fa-home"></i> Ir para o Portal</a>
</div>
</div>
</body>
</html>"""
    return render_template_string(html)


@app.get("/t2s/relatorios_usuarios")
def t2s_relatorios_usuarios():
    emprestimos = t2s_controller.get_emprestimos()
    usuarios = t2s_controller.get_usuarios()
    relatorio_usuarios = t2s_report_service.get_most_active_users(emprestimos, usuarios)
    
    def _esc(v):
        from html import escape
        return escape("" if v is None else str(v))
    
    tabela = ""
    if relatorio_usuarios:
        tabela = "<table><thead><tr><th>Posição</th><th>Usuário</th><th>Email</th><th>Categoria</th><th>Total de Empréstimos</th></tr></thead><tbody>"
        for i, usuario in enumerate(relatorio_usuarios, 1):
            nome = usuario.get('name', f'ID: {usuario.get("user_id", "N/A")}')
            email = usuario.get('email', 'N/A')
            tipo = usuario.get('type', 'N/A')
            emprestimos_count = usuario.get('loan_count', 0)
            avatar_emoji = "🎓" if tipo == "Estudante" else "👨‍🏫" if tipo == "Professor" else "👔"
            tabela += f'<tr><td><span class="position-badge">{i}</span></td>'
            tabela += f'<td><div class="user-info"><div class="user-avatar">{avatar_emoji}</div><div class="user-details"><h4>{_esc(nome)}</h4><p>ID: {usuario.get("user_id", "N/A")}</p></div></div></td>'
            tabela += f'<td>{_esc(email)}</td>'
            tabela += f'<td><span class="user-type">{_esc(tipo)}</span></td>'
            tabela += f'<td><span class="loans-count">{emprestimos_count}</span></td></tr>'
        tabela += "</tbody></table>"
    else:
        tabela = '<div class="no-data"><p>Nenhum empréstimo registrado no sistema ainda.</p><p>Os dados aparecerão aqui após a realização dos primeiros empréstimos.</p></div>'
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Perfil dos Usuários - Sistema de Biblioteca</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Inter,sans-serif;background:#f8fafc;min-height:100vh;color:#1e293b;padding:20px}}
.header{{background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:50px 20px;text-align:center;margin-bottom:40px;box-shadow:0 4px 6px -1px rgba(0,0,0,0.1)}}
.header h1{{font-size:2.5em;font-weight:700;margin-bottom:12px;letter-spacing:-0.025em}}
.header p{{font-size:1.125em;opacity:0.9;font-weight:400}}
.container{{max-width:1200px;margin:0 auto;background:white;border-radius:16px;padding:50px;box-shadow:0 10px 25px -5px rgba(0,0,0,0.1),0 10px 10px -5px rgba(0,0,0,0.04);border:1px solid #e2e8f0}}
.report-title{{text-align:center;margin-bottom:40px}}
.report-title h1{{font-size:2em;font-weight:600;color:#1e293b;margin-bottom:8px;letter-spacing:-0.025em}}
.report-title p{{color:#64748b;font-size:1em;font-weight:400}}
table{{width:100%;border-collapse:collapse;margin:30px 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.05)}}
thead{{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white}}
th,td{{padding:16px 20px;text-align:left;border-bottom:1px solid #e5e7eb}}
tbody tr:hover{{background:#f8fafc}}
tbody tr:nth-child(even){{background:#f9fafb}}
.position-badge{{display:inline-block;width:40px;height:40px;background:linear-gradient(135deg,#f59e0b,#d97706);color:white;border-radius:50%;text-align:center;line-height:40px;font-weight:700;margin-right:16px}}
.user-info{{display:flex;align-items:center}}
.user-avatar{{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#f1f5f9,#e2e8f0);display:flex;align-items:center;justify-content:center;margin-right:16px;font-size:1.2em;color:#64748b;border:1px solid #cbd5e1}}
.user-details h4{{margin:0 0 4px 0;font-weight:600;color:#1e293b;font-size:1em}}
.user-details p{{margin:0;color:#64748b;font-size:0.875em}}
.user-type{{display:inline-block;padding:4px 12px;background:#dcfce7;color:#166534;border:1px solid #bbf7d0;border-radius:16px;font-size:0.8em;font-weight:600;margin-left:8px}}
.loans-count{{font-weight:700;color:#3b82f6;text-align:center;font-size:1.125em}}
.no-data{{text-align:center;color:#64748b;padding:60px 40px;border:2px dashed #e2e8f0;border-radius:12px;margin:40px 0;background:#f8fafc}}
.actions{{text-align:center;margin-top:40px}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:500;transition:all 0.2s;margin:0 8px}}
.btn-primary{{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white;box-shadow:0 1px 3px 0 rgba(59,130,246,0.3)}}
.btn-primary:hover{{background:linear-gradient(135deg,#1d4ed8,#1e40af);transform:translateY(-1px);box-shadow:0 4px 12px rgba(59,130,246,0.4)}}
.btn-secondary{{background:#64748b;color:white}}
.btn-secondary:hover{{background:#475569;transform:translateY(-1px)}}
@media(max-width:768px){{.container{{padding:30px 20px}}.header{{padding:40px 20px}}.header h1{{font-size:2em}}table{{font-size:0.875em}}th,td{{padding:12px 16px}}}}
</style>
</head>
<body>
<div class="header">
<h1>Perfil dos Usuários</h1>
<p>Relatório de usuários mais ativos</p>
</div>
<div class="container">
<div class="report-title">
<h1>Ranking de Atividade</h1>
<p>Métricas de engajamento e frequência de empréstimos</p>
</div>
{tabela}
<div class="actions">
<a href="/t2s/relatorios" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Retornar aos Relatórios</a>
<a href="/t2s/menu" class="btn btn-primary"><i class="fas fa-home"></i> Ir para o Portal</a>
</div>
</div>
</body>
</html>"""
    return render_template_string(html)


# ===== Seção: Dacio (reuso de HTML e controller existente) =====
comTrole = dacio_controller.Controler() if DACIO_AVAILABLE else None


@app.get("/dacio/menu")
def dacio_menu():
    if not DACIO_AVAILABLE:
        return "Módulo Dacio indisponível nesta execução.", 503
    path = os.path.join(PROJ_DACIO, "View_and_Interface", "menu.html")
    return render_template_string(_read_file(path))


@app.get("/dacio/cadastrar_livro")
def dacio_cadastrar_livro_page():
    if not DACIO_AVAILABLE:
        return "Módulo Dacio indisponível nesta execução.", 503
    path = os.path.join(PROJ_DACIO, "View_and_Interface", "cadastrar_livro.html")
    conteudo = _read_file(path)
    html = conteudo.replace("/cadastrar", "/dacio/cadastrar")
    html = html.replace("/menu", "/dacio/menu")
    return render_template_string(html)


@app.get("/dacio/listar_livros")
def dacio_listar_livros():
    if not DACIO_AVAILABLE or not comTrole:
        return "Módulo Dacio indisponível nesta execução.", 503
    livros = comTrole.Get_Livros()
    path_tpl = os.path.join(PROJ_DACIO, "View_and_Interface", "listar_livros.html")
    conteudo = _read_file(path_tpl)
    
    def _esc(v):
        from html import escape
        return escape("" if v is None else str(v))
    
    cards = []
    for livro in livros:
        autores = ", ".join(livro.autores)
        cards.append(f"""
                <div class="card mb-3 p-4 shadow-sm border-0">
                    <h5 class="card-title text-primary">{_esc(livro.titulo)}</h5>
                    <p class="mb-1"><b>Autores:</b> {_esc(autores)}</p>
                    <p class="mb-1"><b>ISBN:</b> {_esc(livro.ISBN)}</p>
                    <p class="mb-1"><b>Ano:</b> {_esc(livro.ano)}</p>
                    <p class="mb-1"><b>Cópias:</b> {_esc(livro.copiasDisponiveis)}/{_esc(livro.copiasTotal)}</p>
                    <p class="mb-2"><b>Status:</b> {_esc(livro.status)}</p>
                    <div class="d-flex gap-2">
                        <form method="GET" action="/dacio/alterar_livro">
                            <input type="hidden" name="isbn" value="{_esc(livro.ISBN)}">
                            <button class="btn btn-warning btn-sm" type="submit">✏️ Editar</button>
                        </form>
                        <form method="POST" action="/dacio/remover_livro" onsubmit="return confirm('Deseja realmente remover este livro?');">
                            <input type="hidden" name="isbn" value="{_esc(livro.ISBN)}">
                            <button class="btn btn-danger btn-sm" type="submit">🗑️ Remover</button>
                        </form>
                    </div>
                </div>
                """)
    html = conteudo.replace("<!--LIVROS-->", "".join(cards) or "<div>Nenhum livro.</div>")
    html = html.replace("/menu", "/dacio/menu")
    html = html.replace("/cadastrar_livro", "/dacio/cadastrar_livro")
    return render_template_string(html)


@app.post("/dacio/cadastrar")
def dacio_cadastrar_livro_action():
    if not DACIO_AVAILABLE or not comTrole:
        return "Módulo Dacio indisponível nesta execução.", 503
    dados_livro = {
        "titulo": request.form.get("titulo", ""),
        "autores": [a.strip() for a in request.form.get("autores", "").split(",") if a.strip()],
        "isbn": request.form.get("isbn", ""),
        "ano": request.form.get("ano", ""),
        "copiasTotal": request.form.get("copiasTotal", "0"),
        "copiasDisponiveis": request.form.get("copiasDisponiveis", "0"),
    }
    comTrole.Ctr_Adicionar_Livro(dados_livro)
    return redirect("/dacio/listar_livros")


@app.get("/dacio/alterar_livro")
def dacio_alterar_livro_page():
    if not DACIO_AVAILABLE or not comTrole:
        return "Módulo Dacio indisponível nesta execução.", 503
    isbn = request.args.get("isbn", "")
    livros = comTrole.Get_Livros()
    livro = next((l for l in livros if l.ISBN == isbn), None)
    if not livro:
        return "Livro não encontrado", 404
    
    def _esc(v):
        from html import escape
        return escape("" if v is None else str(v))
    
    path = os.path.join(PROJ_DACIO, "View_and_Interface", "alterar_livro.html")
    conteudo = _read_file(path)
    html = (conteudo
            .replace("<!--TITULO-->", _esc(livro.titulo))
            .replace("<!--AUTORES-->", _esc(", ".join(livro.autores)))
            .replace("<!--ISBN-->", _esc(livro.ISBN))
            .replace("<!--ANO-->", _esc(livro.ano))
            .replace("<!--COPIASTOTAL-->", _esc(livro.copiasTotal))
            .replace("/alterar_livro", "/dacio/alterar_livro")
            .replace("/listar_livros", "/dacio/listar_livros"))
    return render_template_string(html)


@app.post("/dacio/alterar_livro")
def dacio_alterar_livro_action():
    if not DACIO_AVAILABLE or not comTrole:
        return "Módulo Dacio indisponível nesta execução.", 503
    isbn = request.form.get("isbn", "")
    novo_titulo = request.form.get("titulo", "")
    novos_autores = [a.strip() for a in request.form.get("autores", "").split(",") if a.strip()]
    novo_ano = int(request.form.get("ano", "0") or "0")
    nova_qtd = int(request.form.get("copiasTotal", "0") or "0")
    comTrole.Alterar_Livro(isbn, novo_titulo, novos_autores, novo_ano, nova_qtd)
    return redirect("/dacio/listar_livros")


@app.post("/dacio/remover_livro")
def dacio_remover_livro_action():
    if not DACIO_AVAILABLE or not comTrole:
        return "Módulo Dacio indisponível nesta execução.", 503
    isbn = request.form.get("isbn", "")
    comTrole.Remover_Livro(isbn)
    return redirect("/dacio/listar_livros")


if __name__ == "__main__":
    # Inicializa banco do Trabalho-2S forçando memória (evitar dependência de MongoDB local)
    try:
        t2s_model.db_manager.using_memory = True
    except Exception:
        pass
    t2s_model.db_manager.connect()
    app.run(host="0.0.0.0", port=5050, debug=True)

