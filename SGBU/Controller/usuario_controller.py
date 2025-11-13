from Model.usuario import Usuario

class UsuarioController:
    def __init__(self, usuario_repository):
        self.repository = usuario_repository
    
    def cadastrar_usuario(self, matricula, nome, tipo_usuario):
        try:
            usuario = Usuario(matricula, nome, tipo_usuario)
            return self.repository.cadastrar(usuario)
        except ValueError as e:
            raise e
    
    def buscar_usuario(self, matricula):
        return self.repository.buscar(matricula)
    
    def listar_usuarios(self):
        return self.repository.listar()
    
    def editar_usuario(self, matricula, nome=None, tipo_usuario=None):
        return self.repository.editar(matricula, nome, tipo_usuario)
    
    def remover_usuario(self, matricula):
        return self.repository.remover(matricula)
    
    def desativar_usuario(self, matricula):
        return self.repository.desativar(matricula)