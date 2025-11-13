import unittest
from Model.usuario import Usuario, UsuarioRepository
from Controller.usuario_controller import UsuarioController

class TestUsuario(unittest.TestCase):
    
    def setUp(self):
        self.repository = UsuarioRepository()
        self.controller = UsuarioController(self.repository)
    
    # [TDD red] Teste para criar usuário
    def test_criar_usuario_valido(self):
        usuario = Usuario("2024001", "João Silva", "aluno")
        self.assertEqual(usuario.matricula, "2024001")
        self.assertEqual(usuario.nome, "João Silva")
        self.assertEqual(usuario.tipo_usuario, "aluno")
        self.assertTrue(usuario.ativo)
    
    # [TDD red] Teste para validar matrícula inválida
    def test_criar_usuario_matricula_invalida(self):
        with self.assertRaises(ValueError):
            Usuario("", "João Silva", "aluno")
    
    # [TDD red] Teste para validar nome inválido
    def test_criar_usuario_nome_invalido(self):
        with self.assertRaises(ValueError):
            Usuario("2024001", "", "aluno")
    
    # [TDD red] Teste para validar tipo de usuário inválido
    def test_criar_usuario_tipo_invalido(self):
        with self.assertRaises(ValueError):
            Usuario("2024001", "João Silva", "invalido")
    
    # [TDD red] Teste para cadastrar usuário
    def test_cadastrar_usuario(self):
        usuario = self.controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.matricula, "2024001")
    
    # [TDD red] Teste para impedir cadastro duplicado
    def test_cadastrar_usuario_duplicado(self):
        self.controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        with self.assertRaises(ValueError):
            self.controller.cadastrar_usuario("2024001", "Maria Santos", "professor")
    
    # [TDD red] Teste para buscar usuário
    def test_buscar_usuario(self):
        self.controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        usuario = self.controller.buscar_usuario("2024001")
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nome, "João Silva")
    
    # [TDD red] Teste para buscar usuário inexistente
    def test_buscar_usuario_inexistente(self):
        usuario = self.controller.buscar_usuario("9999999")
        self.assertIsNone(usuario)
    
    # [TDD red] Teste para listar usuários
    def test_listar_usuarios(self):
        self.controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        self.controller.cadastrar_usuario("2024002", "Maria Santos", "professor")
        usuarios = self.controller.listar_usuarios()
        self.assertEqual(len(usuarios), 2)
    
    # [TDD red] Teste para editar usuário
    def test_editar_usuario(self):
        self.controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        usuario = self.controller.editar_usuario("2024001", nome="João Pedro Silva")
        self.assertEqual(usuario.nome, "João Pedro Silva")
    
    # [TDD red] Teste para remover usuário
    def test_remover_usuario(self):
        self.controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        resultado = self.controller.remover_usuario("2024001")
        self.assertTrue(resultado)
        usuario = self.controller.buscar_usuario("2024001")
        self.assertIsNone(usuario)
    
    # [TDD red] Teste para desativar usuário
    def test_desativar_usuario(self):
        self.controller.cadastrar_usuario("2024001", "João Silva", "aluno")
        usuario = self.controller.desativar_usuario("2024001")
        self.assertFalse(usuario.ativo)

if __name__ == '__main__':
    unittest.main()