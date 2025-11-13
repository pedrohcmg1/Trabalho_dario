from Model.usuario import UsuarioRepository
from Model.livro import LivroRepository
from Model.emprestimo import EmprestimoRepository
from Model.relatorio import RelatorioService
from Controller.usuario_controller import UsuarioController
from Controller.livro_controller import LivroController
from Controller.emprestimo_controller import EmprestimoController
from Controller.relatorio_controller import RelatorioController
from View_and_Interface.view import BibliotecaHandler
from http.server import HTTPServer

def main():
    print("Starting Service...\n")
    print("Sistema de Gerenciamento de Biblioteca Universitária - TecLearn TABAJARA")
    print("=" * 70)
    
    usuario_repository = UsuarioRepository()
    livro_repository = LivroRepository()
    emprestimo_repository = EmprestimoRepository(usuario_repository, livro_repository)
    relatorio_service = RelatorioService(usuario_repository, livro_repository, emprestimo_repository)
    
    usuario_controller = UsuarioController(usuario_repository)
    livro_controller = LivroController(livro_repository)
    emprestimo_controller = EmprestimoController(emprestimo_repository)
    relatorio_controller = RelatorioController(relatorio_service)
    
    BibliotecaHandler.usuario_controller = usuario_controller
    BibliotecaHandler.livro_controller = livro_controller
    BibliotecaHandler.emprestimo_controller = emprestimo_controller
    BibliotecaHandler.relatorio_controller = relatorio_controller
    
    print("\nCarregando dados de exemplo...")
    try:
        usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        usuario_controller.cadastrar_usuario("2024002", "Maria Santos", "professor")
        usuario_controller.cadastrar_usuario("2024003", "Pedro Costa", "funcionario")
        print("✓ 3 usuários cadastrados")
        
        livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        livro_controller.cadastrar_livro("L002", "Java Avançado", "Maria Santos", 3)
        livro_controller.cadastrar_livro("L003", "JavaScript Básico", "Pedro Costa", 2)
        livro_controller.cadastrar_livro("L004", "Banco de Dados", "Ana Lima", 4)
        print("✓ 4 livros cadastrados")
        
        emprestimo_controller.realizar_emprestimo("2024001", "L001")
        emprestimo_controller.realizar_emprestimo("2024002", "L002")
        print("✓ 2 empréstimos realizados")
        
    except Exception as e:
        print(f"Erro ao carregar dados de exemplo: {e}")
    
    print("\n" + "=" * 70)
    print("Servidor rodando em http://localhost:8000")
    print("\nEndpoints disponíveis:")
    print("  Usuários:")
    print("    GET    /usuarios")
    print("    GET    /usuarios/{matricula}")
    print("    POST   /usuarios")
    print("    PUT    /usuarios/{matricula}")
    print("    DELETE /usuarios/{matricula}")
    print("\n  Livros:")
    print("    GET    /livros")
    print("    GET    /livros/{codigo}")
    print("    POST   /livros")
    print("    PUT    /livros/{codigo}")
    print("    DELETE /livros/{codigo}")
    print("\n  Empréstimos:")
    print("    GET    /emprestimos")
    print("    GET    /emprestimos/ativos")
    print("    GET    /emprestimos/{id}")
    print("    GET    /emprestimos/usuario/{matricula}")
    print("    GET    /emprestimos/livro/{codigo}")
    print("    POST   /emprestimos")
    print("    POST   /emprestimos/devolucao")
    print("\n  Relatórios:")
    print("    GET    /relatorios/livros-mais-emprestados")
    print("    GET    /relatorios/usuarios-mais-ativos")
    print("    GET    /relatorios/status-acervo")
    print("    GET    /relatorios/status-usuarios")
    print("    GET    /relatorios/emprestimos-ativos")
    print("    GET    /relatorios/completo")
    print("=" * 70)
    print("\nPressione Ctrl+C para encerrar o servidor\n")
    
    servidor = HTTPServer(("localhost", 8000), BibliotecaHandler)
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n\nEncerrando servidor...")
        servidor.shutdown()
        print("Servidor encerrado com sucesso!")

if __name__ == "__main__":
    main()