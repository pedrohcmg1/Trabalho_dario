import unittest
from Model.usuario import Usuario, UsuarioRepository
from Model.livro import Livro, LivroRepository
from Model.emprestimo import EmprestimoRepository
from Model.relatorio import RelatorioService
from Controller.relatorio_controller import RelatorioController

class TestRelatorio(unittest.TestCase):
    
    def setUp(self):
        self.usuario_repository = UsuarioRepository()
        self.livro_repository = LivroRepository()
        self.emprestimo_repository = EmprestimoRepository(
            self.usuario_repository,
            self.livro_repository
        )
        self.relatorio_service = RelatorioService(
            self.usuario_repository,
            self.livro_repository,
            self.emprestimo_repository
        )
        self.controller = RelatorioController(self.relatorio_service)
        
        usuario1 = Usuario("2024001", "João Silva", "aluno")
        usuario2 = Usuario("2024002", "Maria Santos", "professor")
        self.usuario_repository.cadastrar(usuario1)
        self.usuario_repository.cadastrar(usuario2)
        
        livro1 = Livro("L001", "Python para Iniciantes", "João Silva", 5)
        livro2 = Livro("L002", "Java Avançado", "Maria Santos", 3)
        livro3 = Livro("L003", "JavaScript Básico", "Pedro Costa", 2)
        self.livro_repository.cadastrar(livro1)
        self.livro_repository.cadastrar(livro2)
        self.livro_repository.cadastrar(livro3)
    
    # [TDD red] Teste para obter status do acervo
    def test_status_acervo(self):
        status = self.controller.obter_status_acervo()
        
        self.assertEqual(status['total_titulos'], 3)
        self.assertEqual(status['total_exemplares'], 10)
        self.assertEqual(status['exemplares_disponiveis'], 10)
        self.assertEqual(status['exemplares_emprestados'], 0)
    
    # [TDD red] Teste para status do acervo com empréstimos
    def test_status_acervo_com_emprestimos(self):
        self.emprestimo_repository.registrar_emprestimo("2024001", "L001")
        self.emprestimo_repository.registrar_emprestimo("2024001", "L002")
        
        status = self.controller.obter_status_acervo()
        
        self.assertEqual(status['exemplares_disponiveis'], 8)
        self.assertEqual(status['exemplares_emprestados'], 2)
    
    # [TDD red] Teste para status de usuários
    def test_status_usuarios(self):
        status = self.controller.obter_status_usuarios()
        
        self.assertEqual(status['total_usuarios'], 2)
        self.assertEqual(status['usuarios_ativos'], 2)
        self.assertEqual(status['usuarios_inativos'], 0)
        self.assertEqual(status['por_tipo']['aluno'], 1)
        self.assertEqual(status['por_tipo']['professor'], 1)
    
    # [TDD red] Teste para livros mais emprestados
    def test_livros_mais_emprestados(self):
        self.emprestimo_repository.registrar_emprestimo("2024001", "L001")
        self.emprestimo_repository.registrar_emprestimo("2024002", "L001")
        self.emprestimo_repository.registrar_emprestimo("2024001", "L002")
        
        resultado = self.controller.obter_livros_mais_emprestados(2)
        
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['codigo'], "L001")
        self.assertEqual(resultado[0]['quantidade_emprestimos'], 2)
        self.assertEqual(resultado[1]['codigo'], "L002")
        self.assertEqual(resultado[1]['quantidade_emprestimos'], 1)
    
    # [TDD red] Teste para usuários mais ativos
    def test_usuarios_mais_ativos(self):
        self.emprestimo_repository.registrar_emprestimo("2024001", "L001")
        self.emprestimo_repository.registrar_emprestimo("2024001", "L002")
        self.emprestimo_repository.registrar_emprestimo("2024001", "L003")
        self.emprestimo_repository.registrar_emprestimo("2024002", "L001")
        
        resultado = self.controller.obter_usuarios_mais_ativos(2)
        
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['matricula'], "2024001")
        self.assertEqual(resultado[0]['quantidade_emprestimos'], 3)
        self.assertEqual(resultado[1]['matricula'], "2024002")
        self.assertEqual(resultado[1]['quantidade_emprestimos'], 1)
    
    # [TDD red] Teste para empréstimos ativos
    def test_emprestimos_ativos(self):
        emp1 = self.emprestimo_repository.registrar_emprestimo("2024001", "L001")
        emp2 = self.emprestimo_repository.registrar_emprestimo("2024002", "L002")
        
        self.emprestimo_repository.registrar_devolucao(emp1.id_emprestimo)
        
        resultado = self.controller.obter_emprestimos_ativos()
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['id_emprestimo'], emp2.id_emprestimo)
        self.assertEqual(resultado[0]['usuario_nome'], "Maria Santos")
        self.assertEqual(resultado[0]['livro_titulo'], "Java Avançado")
    
    # [TDD red] Teste para relatório completo
    def test_relatorio_completo(self):
        self.emprestimo_repository.registrar_emprestimo("2024001", "L001")
        self.emprestimo_repository.registrar_emprestimo("2024002", "L001")
        
        resultado = self.controller.obter_relatorio_completo()
        
        self.assertIn('acervo', resultado)
        self.assertIn('usuarios', resultado)
        self.assertIn('livros_mais_emprestados', resultado)
        self.assertIn('usuarios_mais_ativos', resultado)
        self.assertEqual(resultado['total_emprestimos'], 2)
        self.assertEqual(resultado['emprestimos_ativos'], 2)
    
    # [TDD red] Teste para limitar resultados
    def test_livros_mais_emprestados_com_limite(self):
        for i in range(3):
            self.emprestimo_repository.registrar_emprestimo("2024001", "L001")
        for i in range(2):
            self.emprestimo_repository.registrar_emprestimo("2024001", "L002")
        self.emprestimo_repository.registrar_emprestimo("2024001", "L003")
        
        resultado = self.controller.obter_livros_mais_emprestados(2)
        
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['codigo'], "L001")
        self.assertEqual(resultado[1]['codigo'], "L002")

if __name__ == '__main__':
    unittest.main()