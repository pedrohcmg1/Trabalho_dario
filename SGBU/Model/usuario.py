class Usuario:
    def __init__(self, matricula, nome, tipo_usuario):
        if not matricula or not isinstance(matricula, str):
            raise ValueError("Matrícula inválida")
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome inválido")
        if tipo_usuario not in ['aluno', 'professor', 'funcionario']:
            raise ValueError("Tipo de usuário inválido")
        
        self.matricula = matricula
        self.nome = nome
        self.tipo_usuario = tipo_usuario
        self.ativo = True
    
    def to_dict(self):
        return {
            'matricula': self.matricula,
            'nome': self.nome,
            'tipo_usuario': self.tipo_usuario,
            'ativo': self.ativo
        }
    
    @staticmethod
    def from_dict(data):
        usuario = Usuario(data['matricula'], data['nome'], data['tipo_usuario'])
        usuario.ativo = data.get('ativo', True)
        return usuario


class UsuarioRepository:
    def __init__(self):
        self.usuarios = {}
    
    def cadastrar(self, usuario):
        if usuario.matricula in self.usuarios:
            raise ValueError("Usuário já cadastrado")
        self.usuarios[usuario.matricula] = usuario
        return usuario
    
    def buscar(self, matricula):
        if matricula not in self.usuarios:
            return None
        return self.usuarios[matricula]
    
    def listar(self):
        return list(self.usuarios.values())
    
    def editar(self, matricula, nome=None, tipo_usuario=None):
        usuario = self.buscar(matricula)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        
        if nome:
            usuario.nome = nome
        if tipo_usuario:
            if tipo_usuario not in ['aluno', 'professor', 'funcionario']:
                raise ValueError("Tipo de usuário inválido")
            usuario.tipo_usuario = tipo_usuario
        
        return usuario
    
    def remover(self, matricula):
        if matricula not in self.usuarios:
            raise ValueError("Usuário não encontrado")
        del self.usuarios[matricula]
        return True
    
    def desativar(self, matricula):
        usuario = self.buscar(matricula)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        usuario.ativo = False
        return usuario