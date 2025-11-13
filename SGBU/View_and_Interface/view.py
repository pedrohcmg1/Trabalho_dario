from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class BibliotecaHandler(BaseHTTPRequestHandler):
    usuario_controller = None
    livro_controller = None
    emprestimo_controller = None
    relatorio_controller = None
    
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
    
    def _send_json(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode('utf-8'))
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        try:
            if path == '/usuarios':
                usuarios = self.usuario_controller.listar_usuarios()
                self._send_json([u.to_dict() for u in usuarios])
            
            elif path.startswith('/usuarios/'):
                matricula = path.split('/')[-1]
                usuario = self.usuario_controller.buscar_usuario(matricula)
                if usuario:
                    self._send_json(usuario.to_dict())
                else:
                    self._send_json({'erro': 'Usuário não encontrado'}, 404)
            
            elif path == '/livros':
                livros = self.livro_controller.listar_livros()
                self._send_json([l.to_dict() for l in livros])
            
            elif path.startswith('/livros/'):
                codigo = path.split('/')[-1]
                livro = self.livro_controller.buscar_livro(codigo)
                if livro:
                    self._send_json(livro.to_dict())
                else:
                    self._send_json({'erro': 'Livro não encontrado'}, 404)
            
            elif path == '/emprestimos':
                emprestimos = self.emprestimo_controller.listar_emprestimos()
                self._send_json([e.to_dict() for e in emprestimos])
            
            elif path == '/emprestimos/ativos':
                emprestimos = self.emprestimo_controller.listar_emprestimos_ativos()
                self._send_json([e.to_dict() for e in emprestimos])
            
            elif path.startswith('/emprestimos/usuario/'):
                matricula = path.split('/')[-1]
                emprestimos = self.emprestimo_controller.listar_emprestimos_usuario(matricula)
                self._send_json([e.to_dict() for e in emprestimos])
            
            elif path.startswith('/emprestimos/livro/'):
                codigo = path.split('/')[-1]
                emprestimos = self.emprestimo_controller.listar_emprestimos_livro(codigo)
                self._send_json([e.to_dict() for e in emprestimos])
            
            elif path.startswith('/emprestimos/'):
                id_emp = path.split('/')[-1]
                emprestimo = self.emprestimo_controller.buscar_emprestimo(id_emp)
                if emprestimo:
                    self._send_json(emprestimo.to_dict())
                else:
                    self._send_json({'erro': 'Empréstimo não encontrado'}, 404)
            
            elif path == '/relatorios/livros-mais-emprestados':
                limite = int(query_params.get('limite', [10])[0])
                resultado = self.relatorio_controller.obter_livros_mais_emprestados(limite)
                self._send_json(resultado)
            
            elif path == '/relatorios/usuarios-mais-ativos':
                limite = int(query_params.get('limite', [10])[0])
                resultado = self.relatorio_controller.obter_usuarios_mais_ativos(limite)
                self._send_json(resultado)
            
            elif path == '/relatorios/status-acervo':
                resultado = self.relatorio_controller.obter_status_acervo()
                self._send_json(resultado)
            
            elif path == '/relatorios/status-usuarios':
                resultado = self.relatorio_controller.obter_status_usuarios()
                self._send_json(resultado)
            
            elif path == '/relatorios/emprestimos-ativos':
                resultado = self.relatorio_controller.obter_emprestimos_ativos()
                self._send_json(resultado)
            
            elif path == '/relatorios/completo':
                resultado = self.relatorio_controller.obter_relatorio_completo()
                self._send_json(resultado)
            
            elif path == '/':
                self._send_json({
                    'mensagem': 'Sistema de Gerenciamento de Biblioteca Universitária - TecLearn TABAJARA',
                    'endpoints': {
                        'usuarios': '/usuarios, /usuarios/{matricula}',
                        'livros': '/livros, /livros/{codigo}',
                        'emprestimos': '/emprestimos, /emprestimos/{id}, /emprestimos/usuario/{matricula}, /emprestimos/livro/{codigo}',
                        'relatorios': '/relatorios/livros-mais-emprestados, /relatorios/usuarios-mais-ativos, /relatorios/completo'
                    }
                })
            
            else:
                self._send_json({'erro': 'Rota não encontrada'}, 404)
        
        except Exception as e:
            self._send_json({'erro': str(e)}, 500)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        path = self.path
        
        try:
            if path == '/usuarios':
                usuario = self.usuario_controller.cadastrar_usuario(
                    data['matricula'], data['nome'], data['tipo_usuario']
                )
                self._send_json(usuario.to_dict(), 201)
            
            elif path == '/livros':
                livro = self.livro_controller.cadastrar_livro(
                    data['codigo'], data['titulo'], data['autor'], data['quantidade_total']
                )
                self._send_json(livro.to_dict(), 201)
            
            elif path == '/emprestimos':
                emprestimo = self.emprestimo_controller.realizar_emprestimo(
                    data['matricula_usuario'], data['codigo_livro']
                )
                self._send_json(emprestimo.to_dict(), 201)
            
            elif path == '/emprestimos/devolucao':
                emprestimo = self.emprestimo_controller.realizar_devolucao(data['id_emprestimo'])
                self._send_json(emprestimo.to_dict())
            
            else:
                self._send_json({'erro': 'Rota não encontrada'}, 404)
        
        except ValueError as e:
            self._send_json({'erro': str(e)}, 400)
        except Exception as e:
            self._send_json({'erro': str(e)}, 500)
    
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        data = json.loads(put_data.decode('utf-8'))
        
        path = self.path
        
        try:
            if path.startswith('/usuarios/'):
                matricula = path.split('/')[-1]
                usuario = self.usuario_controller.editar_usuario(
                    matricula,
                    data.get('nome'),
                    data.get('tipo_usuario')
                )
                self._send_json(usuario.to_dict())
            
            elif path.startswith('/livros/'):
                codigo = path.split('/')[-1]
                livro = self.livro_controller.editar_livro(
                    codigo,
                    data.get('titulo'),
                    data.get('autor'),
                    data.get('quantidade_total')
                )
                self._send_json(livro.to_dict())
            
            else:
                self._send_json({'erro': 'Rota não encontrada'}, 404)
        
        except ValueError as e:
            self._send_json({'erro': str(e)}, 400)
        except Exception as e:
            self._send_json({'erro': str(e)}, 500)
    
    def do_DELETE(self):
        path = self.path
        
        try:
            if path.startswith('/usuarios/'):
                matricula = path.split('/')[-1]
                self.usuario_controller.remover_usuario(matricula)
                self._send_json({'mensagem': 'Usuário removido com sucesso'})
            
            elif path.startswith('/livros/'):
                codigo = path.split('/')[-1]
                self.livro_controller.remover_livro(codigo)
                self._send_json({'mensagem': 'Livro removido com sucesso'})
            
            else:
                self._send_json({'erro': 'Rota não encontrada'}, 404)
        
        except ValueError as e:
            self._send_json({'erro': str(e)}, 400)
        except Exception as e:
            self._send_json({'erro': str(e)}, 500)
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")