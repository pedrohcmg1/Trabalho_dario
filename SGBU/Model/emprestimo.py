from datetime import datetime, timedelta

class Emprestimo:
    def __init__(self, id_emprestimo, matricula_usuario, codigo_livro, data_emprestimo=None):
        if not id_emprestimo or not isinstance(id_emprestimo, str):
            raise ValueError("ID de empréstimo inválido")
        if not matricula_usuario or not isinstance(matricula_usuario, str):
            raise ValueError("Matrícula inválida")
        if not codigo_livro or not isinstance(codigo_livro, str):
            raise ValueError("Código do livro inválido")
        
        self.id_emprestimo = id_emprestimo
        self.matricula_usuario = matricula_usuario
        self.codigo_livro = codigo_livro
        self.data_emprestimo = data_emprestimo or datetime.now()
        self.data_devolucao_prevista = self.data_emprestimo + timedelta(days=14)
        self.data_devolucao_real = None
        self.status = 'ativo'
    
    def to_dict(self):
        return {
            'id_emprestimo': self.id_emprestimo,
            'matricula_usuario': self.matricula_usuario,
            'codigo_livro': self.codigo_livro,
            'data_emprestimo': self.data_emprestimo.isoformat(),
            'data_devolucao_prevista': self.data_devolucao_prevista.isoformat(),
            'data_devolucao_real': self.data_devolucao_real.isoformat() if self.data_devolucao_real else None,
            'status': self.status
        }
    
    @staticmethod
    def from_dict(data):
        emprestimo = Emprestimo(
            data['id_emprestimo'],
            data['matricula_usuario'],
            data['codigo_livro'],
            datetime.fromisoformat(data['data_emprestimo'])
        )
        emprestimo.data_devolucao_prevista = datetime.fromisoformat(data['data_devolucao_prevista'])
        if data.get('data_devolucao_real'):
            emprestimo.data_devolucao_real = datetime.fromisoformat(data['data_devolucao_real'])
        emprestimo.status = data['status']
        return emprestimo
    
    def devolver(self, data_devolucao=None):
        if self.status == 'devolvido':
            raise ValueError("Empréstimo já devolvido")
        self.data_devolucao_real = data_devolucao or datetime.now()
        self.status = 'devolvido'


class EmprestimoRepository:
    def __init__(self, usuario_repository, livro_repository):
        self.emprestimos = {}
        self.usuario_repository = usuario_repository
        self.livro_repository = livro_repository
        self.contador = 0
    
    def _gerar_id(self):
        self.contador += 1
        return f"EMP{self.contador:05d}"
    
    def registrar_emprestimo(self, matricula_usuario, codigo_livro):
        usuario = self.usuario_repository.buscar(matricula_usuario)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        if not usuario.ativo:
            raise ValueError("Usuário inativo")
        
        livro = self.livro_repository.buscar(codigo_livro)
        if not livro:
            raise ValueError("Livro não encontrado")
        if livro.quantidade_disponivel <= 0:
            raise ValueError("Livro indisponível")
        
        id_emprestimo = self._gerar_id()
        emprestimo = Emprestimo(id_emprestimo, matricula_usuario, codigo_livro)
        
        livro.emprestar()
        
        self.emprestimos[id_emprestimo] = emprestimo
        return emprestimo
    
    def registrar_devolucao(self, id_emprestimo):
        emprestimo = self.buscar(id_emprestimo)
        if not emprestimo:
            raise ValueError("Empréstimo não encontrado")
        
        if emprestimo.status == 'devolvido':
            raise ValueError("Empréstimo já devolvido")
        
        emprestimo.devolver()
        
        livro = self.livro_repository.buscar(emprestimo.codigo_livro)
        if livro:
            livro.devolver()
        
        return emprestimo
    
    def buscar(self, id_emprestimo):
        if id_emprestimo not in self.emprestimos:
            return None
        return self.emprestimos[id_emprestimo]
    
    def listar(self):
        return list(self.emprestimos.values())
    
    def listar_por_usuario(self, matricula_usuario):
        return [e for e in self.emprestimos.values() if e.matricula_usuario == matricula_usuario]
    
    def listar_por_livro(self, codigo_livro):
        return [e for e in self.emprestimos.values() if e.codigo_livro == codigo_livro]
    
    def listar_ativos(self):
        return [e for e in self.emprestimos.values() if e.status == 'ativo']