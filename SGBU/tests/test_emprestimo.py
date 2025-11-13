import unittest
from datetime import datetime, timedelta
from Model.usuario import Usuario, UsuarioRepository
from Model.livro import Livro, LivroRepository
from Model.emprestimo import Emprestimo, EmprestimoRepository
from Controller.emprestimo_controller import EmprestimoController

class TestEmprestimo(unittest.TestCase):
    
    def setUp(self):
        self.usuario_repository = UsuarioRepository()
        self.livro_repository = LivroRepository()
        self.emprestimo_repository = EmprestimoRepository(
            self.usuario_repository, 
            self.livro_repository
        )
        self.controller = EmprestimoController(self.emprestimo_repository)
        
        usuario = Usuario("2024001", "João Silva", "aluno")
        self.usuario_repository.cadastrar(usuario)
        
        livro = Livro("L001", "Python para Iniciantes", "João Silva", 5)
        self.livro_repository.cadastrar(livro)
    
    # [TDD red] Teste para criar empréstimo
    def test_criar_emprestimo_valido(self):
        emprestimo = Emprestimo("EMP001", "2024001", "L001")
        self.assertEqual(emprestimo.id_emprestimo, "EMP001")
        self.assertEqual(emprestimo.matricula_usuario, "2024001")
        self.assertEqual(emprestimo.codigo_livro, "L001")
        self.assertEqual(emprestimo.status, "ativo")
    
    # [TDD red] Teste para validar ID inválido
    def test_criar_emprestimo_id_invalido(self):
        with self.assertRaises(ValueError):
            Emprestimo("", "2024001", "L001")
    
    # [TDD red] Teste para validar matrícula inválida
    def test_criar_emprestimo_matricula_invalida(self):
        with self.assertRaises(ValueError):
            Emprestimo("EMP001", "", "L001")
    
    # [TDD red] Teste para validar código do livro inválido
    def test_criar_emprestimo_codigo_livro_invalido(self):
        with self.assertRaises(ValueError):
            Emprestimo("EMP001", "2024001", "")
    
    # [TDD red] Teste para registrar empréstimo
    def test_registrar_emprestimo(self):
        emprestimo = self.controller.realizar_emprestimo("2024001", "L001")
        self.assertIsNotNone(emprestimo)
        self.assertEqual(emprestimo.status, "ativo")
    
    # [TDD red] Teste para verificar decremento de disponibilidade
    def test_registrar_emprestimo_decrementa_disponibilidade(self):
        livro = self.livro_repository.buscar("L001")
        quantidade_inicial = livro.quantidade_disponivel
        
        self.controller.realizar_emprestimo("2024001", "L001")
        
        self.assertEqual(livro.quantidade_disponivel, quantidade_inicial - 1)
    
    # [TDD red] Teste para impedir empréstimo de usuário inexistente
    def test_registrar_emprestimo_usuario_inexistente(self):
        with self.assertRaises(ValueError):
            self.controller.realizar_emprestimo("9999999", "L001")
    
    # [TDD red] Teste para impedir empréstimo de livro inexistente
    def test_registrar_emprestimo_livro_inexistente(self):
        with self.assertRaises(ValueError):
            self.controller.realizar_emprestimo("2024001", "L999")
    
    # [TDD red] Teste para impedir empréstimo de livro indisponível
    def test_registrar_emprestimo_livro_indisponivel(self):
        livro = Livro("L002", "Livro Esgotado", "Autor", 0)
        self.livro_repository.cadastrar(livro)
        
        with self.assertRaises(ValueError):
            self.controller.realizar_emprestimo("2024001", "L002")
    
    # [TDD red] Teste para impedir empréstimo de usuário inativo
    def test_registrar_emprestimo_usuario_inativo(self):
        usuario = Usuario("2024002", "Maria Inativa", "aluno")
        usuario.ativo = False
        self.usuario_repository.cadastrar(usuario)
        
        with self.assertRaises(ValueError):
            self.controller.realizar_emprestimo("2024002", "L001")
    
    # [TDD red] Teste para registrar devolução
    def test_registrar_devolucao(self):
        emprestimo = self.controller.realizar_emprestimo("2024001", "L001")
        emprestimo_devolvido = self.controller.realizar_devolucao(emprestimo.id_emprestimo)
        
        self.assertEqual(emprestimo_devolvido.status, "devolvido")
        self.assertIsNotNone(emprestimo_devolvido.data_devolucao_real)
    
    # [TDD red] Teste para verificar incremento de disponibilidade na devolução
    def test_registrar_devolucao_incrementa_disponibilidade(self):
        emprestimo = self.controller.realizar_emprestimo("2024001", "L001")
        livro = self.livro_repository.buscar("L001")
        quantidade_antes = livro.quantidade_disponivel
        
        self.controller.realizar_devolucao(emprestimo.id_emprestimo)
        
        self.assertEqual(livro.quantidade_disponivel, quantidade_antes + 1)
    
    # [TDD red] Teste para impedir devolução duplicada
    def test_registrar_devolucao_duplicada(self):
        emprestimo = self.controller.realizar_emprestimo("2024001", "L001")
        self.controller.realizar_devolucao(emprestimo.id_emprestimo)
        
        with self.assertRaises(ValueError):
            self.controller.realizar_devolucao(emprestimo.id_emprestimo)
    
    # [TDD red] Teste para listar empréstimos por usuário
    def test_listar_emprestimos_por_usuario(self):
        self.controller.realizar_emprestimo("2024001", "L001")
        emprestimos = self.controller.listar_emprestimos_usuario("2024001")
        self.assertEqual(len(emprestimos), 1)
    
    # [TDD red] Teste para listar empréstimos por livro
    def test_listar_emprestimos_por_livro(self):
        self.controller.realizar_emprestimo("2024001", "L001")
        emprestimos = self.controller.listar_emprestimos_livro("L001")
        self.assertEqual(len(emprestimos), 1)
    
    # [TDD red] Teste para listar empréstimos ativos
    def test_listar_emprestimos_ativos(self):
        emp1 = self.controller.realizar_emprestimo("2024001", "L001")
        
        livro2 = Livro("L002", "Outro Livro", "Autor", 3)
        self.livro_repository.cadastrar(livro2)
        emp2 = self.controller.realizar_emprestimo("2024001", "L002")
        
        self.controller.realizar_devolucao(emp1.id_emprestimo)
        
        ativos = self.controller.listar_emprestimos_ativos()
        self.assertEqual(len(ativos), 1)
        self.assertEqual(ativos[0].id_emprestimo, emp2.id_emprestimo)

if __name__ == '__main__':
    unittest.main()