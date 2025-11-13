import unittest
from Model.usuario import UsuarioRepository
from Model.livro import LivroRepository
from Model.emprestimo import EmprestimoRepository
from Model.relatorio import RelatorioService
from Controller.usuario_controller import UsuarioController
from Controller.livro_controller import LivroController
from Controller.emprestimo_controller import EmprestimoController
from Controller.relatorio_controller import RelatorioController

class TestIntegracao(unittest.TestCase):
    """
    Testes de integração para verificar se todos os módulos funcionam corretamente juntos
    """
    
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
        
        self.usuario_controller = UsuarioController(self.usuario_repository)
        self.livro_controller = LivroController(self.livro_repository)
        self.emprestimo_controller = EmprestimoController(self.emprestimo_repository)
        self.relatorio_controller = RelatorioController(self.relatorio_service)
    
    # [TDD red] Teste de fluxo completo: cadastro até empréstimo
    def test_fluxo_completo_cadastro_ate_emprestimo(self):
        usuario = self.usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.assertIsNotNone(usuario)
        
        livro = self.livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        self.assertIsNotNone(livro)
        
        emprestimo = self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        self.assertIsNotNone(emprestimo)
        self.assertEqual(emprestimo.matricula_usuario, "2024001")
        self.assertEqual(emprestimo.codigo_livro, "L001")
        
        livro_atualizado = self.livro_controller.buscar_livro("L001")
        self.assertEqual(livro_atualizado.quantidade_disponivel, 4)
    
    # [TDD red] Teste de integração: empréstimo e devolução
    def test_fluxo_emprestimo_e_devolucao(self):
        self.usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        
        emprestimo = self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        livro = self.livro_controller.buscar_livro("L001")
        self.assertEqual(livro.quantidade_disponivel, 4)
        
        self.emprestimo_controller.realizar_devolucao(emprestimo.id_emprestimo)
        livro_devolvido = self.livro_controller.buscar_livro("L001")
        self.assertEqual(livro_devolvido.quantidade_disponivel, 5)
    
    # [TDD red] Teste de integração: múltiplos empréstimos e relatório
    def test_multiplos_emprestimos_e_relatorio(self):
        self.usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.usuario_controller.cadastrar_usuario("2024002", "Maria Santos", "professor")
        
        self.livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        self.livro_controller.cadastrar_livro("L002", "Java Avançado", "Maria Santos", 3)
        
        self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        self.emprestimo_controller.realizar_emprestimo("2024001", "L002")
        self.emprestimo_controller.realizar_emprestimo("2024002", "L001")
        
        livros_mais_emprestados = self.relatorio_controller.obter_livros_mais_emprestados()
        self.assertEqual(len(livros_mais_emprestados), 2)
        self.assertEqual(livros_mais_emprestados[0]['codigo'], "L001")
        
        usuarios_mais_ativos = self.relatorio_controller.obter_usuarios_mais_ativos()
        self.assertEqual(len(usuarios_mais_ativos), 2)
        self.assertEqual(usuarios_mais_ativos[0]['matricula'], "2024001")
    
    # [TDD red] Teste de integração: verificação de disponibilidade
    def test_integracao_verificacao_disponibilidade(self):
        self.usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 1)
        
        self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        
        with self.assertRaises(ValueError):
            self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
    
    # [TDD red] Teste de integração: usuário inativo não pode emprestar
    def test_usuario_inativo_nao_pode_emprestar(self):
        self.usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        
        self.usuario_controller.desativar_usuario("2024001")
        
        with self.assertRaises(ValueError):
            self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
    
    # [TDD red] Teste de integração: relatório completo do sistema
    def test_relatorio_completo_sistema(self):
        self.usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.usuario_controller.cadastrar_usuario("2024002", "Maria Santos", "professor")
        self.usuario_controller.cadastrar_usuario("2024003", "Pedro Costa", "funcionario")
        
        self.livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        self.livro_controller.cadastrar_livro("L002", "Java Avançado", "Maria Santos", 3)
        self.livro_controller.cadastrar_livro("L003", "JavaScript Básico", "Pedro Costa", 2)
        
        self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        self.emprestimo_controller.realizar_emprestimo("2024002", "L001")
        self.emprestimo_controller.realizar_emprestimo("2024001", "L002")
        
        relatorio = self.relatorio_controller.obter_relatorio_completo()
        
        self.assertIn('acervo', relatorio)
        self.assertIn('usuarios', relatorio)
        self.assertIn('livros_mais_emprestados', relatorio)
        self.assertIn('usuarios_mais_ativos', relatorio)
        
        self.assertEqual(relatorio['acervo']['total_titulos'], 3)
        self.assertEqual(relatorio['acervo']['exemplares_emprestados'], 3)
        
        self.assertEqual(relatorio['usuarios']['total_usuarios'], 3)
        self.assertEqual(relatorio['usuarios']['por_tipo']['aluno'], 1)
        
        self.assertEqual(relatorio['total_emprestimos'], 3)
        self.assertEqual(relatorio['emprestimos_ativos'], 3)
    
    # [TDD red] Teste de integração: ciclo completo com devolução
    def test_ciclo_completo_com_devolucao(self):
        self.usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 2)
        
        emp1 = self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        self.assertEqual(self.livro_controller.buscar_livro("L001").quantidade_disponivel, 1)
        
        emp2 = self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        self.assertEqual(self.livro_controller.buscar_livro("L001").quantidade_disponivel, 0)
        
        with self.assertRaises(ValueError):
            self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        
        self.emprestimo_controller.realizar_devolucao(emp1.id_emprestimo)
        self.assertEqual(self.livro_controller.buscar_livro("L001").quantidade_disponivel, 1)
        
        emp3 = self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        self.assertIsNotNone(emp3)
        
        emprestimos_ativos = self.relatorio_controller.obter_emprestimos_ativos()
        self.assertEqual(len(emprestimos_ativos), 2)  
    
    # [TDD red] Teste de integração: validação cruzada de dados
    def test_validacao_cruzada_dados(self):
        self.livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        with self.assertRaises(ValueError):
            self.emprestimo_controller.realizar_emprestimo("2024999", "L001")
        
        self.usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        with self.assertRaises(ValueError):
            self.emprestimo_controller.realizar_emprestimo("2024001", "L999")
    
    # [TDD red] Teste de integração: edição não afeta empréstimos ativos
    def test_edicao_nao_afeta_emprestimos_ativos(self):
        self.usuario_controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.livro_controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        
        emp = self.emprestimo_controller.realizar_emprestimo("2024001", "L001")
        
        self.usuario_controller.editar_usuario("2024001", nome="João Pedro Silva")
        
        self.livro_controller.editar_livro("L001", titulo="Python Avançado")
        
        emprestimo_atual = self.emprestimo_controller.buscar_emprestimo(emp.id_emprestimo)
        self.assertEqual(emprestimo_atual.status, "ativo")
        
        self.emprestimo_controller.realizar_devolucao(emp.id_emprestimo)
        self.assertEqual(emprestimo_atual.status, "devolvido")

if __name__ == '__main__':
    unittest.main()