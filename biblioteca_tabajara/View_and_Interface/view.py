from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from Controller.LivroController import LivroController
import json

class LivroView(BaseHTTPRequestHandler):
    controller = LivroController()

    def do_GET(self):
        if self.path == "/livros":
            livros = self.controller.listar_livros()
            lista = []

            for livro in livros:
                lista.append({
                    "id": livro.get_id(),
                    "titulo": livro.get_titulo(),
                    "autor": livro.get_autor(),
                    "estoque": livro.get_estoque(),
                    "status": livro.get_status()
                })

            self._send_json(lista)

        elif self.path.startswith("/livros/"):
            try:
                livro_id = int(self.path.split("/")[-1])
                livro = self.controller.buscar_livro(livro_id)
                if livro:
                    self._send_json({
                        "id": livro.get_id(),
                        "titulo": livro.get_titulo(),
                        "autor": livro.get_autor(),
                        "estoque": livro.get_estoque(),
                        "status": livro.get_status()
                    })
                else:
                    self._send_json({"erro": "Livro não encontrado"}, status=404)
            except:
                self._send_json({"erro": "ID inválido"}, status=400)
        else:
            self._send_json({"erro": "Rota não encontrada"}, status=404)

    def do_POST(self):
        if self.path == "/livros":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            dados = parse_qs(body)

            try:
                id = int(dados.get("id", [0])[0])
                titulo = dados.get("titulo", [""])[0]
                autor = dados.get("autor", [""])[0]
                estoque = int(dados.get("estoque", [0])[0])

                novo_livro = self.controller.cadastrar_livro(id, titulo, autor, estoque)
                self._send_json({
                    "mensagem": "Livro cadastrado com sucesso",
                    "livro": {
                        "id": novo_livro.get_id(),
                        "titulo": novo_livro.get_titulo(),
                        "autor": novo_livro.get_autor(),
                        "estoque": novo_livro.get_estoque(),
                        "status": novo_livro.get_status()
                    }
                }, status=201)
            except Exception as e:
                self._send_json({"erro": str(e)}, status=400)
        else:
            self._send_json({"erro": "Rota não encontrada"}, status=404)

    def do_DELETE(self):
        if self.path.startswith("/livros/"):
            try:
                livro_id = int(self.path.split("/")[-1])
                livro = self.controller.buscar_livro(livro_id)
                if livro:
                    self.controller.remover_livro(livro_id)
                    self._send_json({"mensagem": "Livro removido com sucesso"})
                else:
                    self._send_json({"erro": "Livro não encontrado"}, status=404)
            except:
                self._send_json({"erro": "ID inválido"}, status=400)
        else:
            self._send_json({"erro": "Rota não encontrada"}, status=404)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
