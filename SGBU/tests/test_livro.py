import unittest
from Model.livro import Livro, LivroRepository
from Controller.livro_controller import LivroController

class TestLivro(unittest.TestCase):
    
    def setUp(self):
        self.repository = LivroRepository()
        self.controller = LivroController(self.repository)
    
    # [TDD red] Teste para criar livro
    def test_criar_livro_valido(self):
        livro = Livro("L001", "Python para Iniciantes", "João Silva", 5)
        self.assertEqual(livro.codigo, "L001")
        self.assertEqual(livro.titulo, "Python para Iniciantes")
        self.assertEqual(livro.autor, "João Silva")
        self.assertEqual(livro.quantidade_total, 5)
        self.assertEqual(livro.quantidade_disponivel, 5)
    
    # [TDD red] Teste para validar código inválido
    def test_criar_livro_codigo_invalido(self):
        with self.assertRaises(ValueError):
            Livro("", "Python para Iniciantes", "João Silva", 5)
    
    # [TDD red] Teste para validar título inválido
    def test_criar_livro_titulo_invalido(self):
        with self.assertRaises(ValueError):
            Livro("L001", "", "João Silva", 5)
    
    # [TDD red] Teste para validar autor inválido
    def test_criar_livro_autor_invalido(self):
        with self.assertRaises(ValueError):
            Livro("L001", "Python para Iniciantes", "", 5)
    
    # [TDD red] Teste para validar quantidade inválida
    def test_criar_livro_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            Livro("L001", "Python para Iniciantes", "João Silva", -1)
    
    # [TDD red] Teste para cadastrar livro
    def test_cadastrar_livro(self):
        livro = self.controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        self.assertIsNotNone(livro)
        self.assertEqual(livro.codigo, "L001")
    
    # [TDD red] Teste para impedir cadastro duplicado
    def test_cadastrar_livro_duplicado(self):
        self.controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        with self.assertRaises(ValueError):
            self.controller.cadastrar_livro("L001", "Java Avançado", "Maria Santos", 3)
    
    # [TDD red] Teste para buscar livro
    def test_buscar_livro(self):
        self.controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        livro = self.controller.buscar_livro("L001")
        self.assertIsNotNone(livro)
        self.assertEqual(livro.titulo, "Python para Iniciantes")
    
    # [TDD red] Teste para buscar livro inexistente
    def test_buscar_livro_inexistente(self):
        livro = self.controller.buscar_livro("L999")
        self.assertIsNone(livro)
    
    # [TDD red] Teste para listar livros
    def test_listar_livros(self):
        self.controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        self.controller.cadastrar_livro("L002", "Java Avançado", "Maria Santos", 3)
        livros = self.controller.listar_livros()
        self.assertEqual(len(livros), 2)
    
    # [TDD red] Teste para editar livro
    def test_editar_livro(self):
        self.controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        livro = self.controller.editar_livro("L001", titulo="Python Avançado")
        self.assertEqual(livro.titulo, "Python Avançado")
    
    # [TDD red] Teste para remover livro
    def test_remover_livro(self):
        self.controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        resultado = self.controller.remover_livro("L001")
        self.assertTrue(resultado)
        livro = self.controller.buscar_livro("L001")
        self.assertIsNone(livro)
    
    # [TDD red] Teste para verificar disponibilidade
    def test_verificar_disponibilidade(self):
        self.controller.cadastrar_livro("L001", "Python para Iniciantes", "João Silva", 5)
        disponivel = self.controller.verificar_disponibilidade("L001")
        self.assertTrue(disponivel)
    
    # [TDD red] Teste para emprestar livro
    def test_emprestar_livro(self):
        livro = Livro("L001", "Python para Iniciantes", "João Silva", 5)
        livro.emprestar()
        self.assertEqual(livro.quantidade_disponivel, 4)
    
    # [TDD red] Teste para emprestar livro indisponível
    def test_emprestar_livro_indisponivel(self):
        livro = Livro("L001", "Python para Iniciantes", "João Silva", 0)
        with self.assertRaises(ValueError):
            livro.emprestar()
    
    # [TDD red] Teste para devolver livro
    def test_devolver_livro(self):
        livro = Livro("L001", "Python para Iniciantes", "João Silva", 5)
        livro.emprestar()
        livro.devolver()
        self.assertEqual(livro.quantidade_disponivel, 5)

if __name__ == '__main__':
    unittest.main()