class Livro:
    def __init__(self, codigo, titulo, autor, quantidade_total):
        if not codigo or not isinstance(codigo, str):
            raise ValueError("Código inválido")
        if not titulo or not isinstance(titulo, str):
            raise ValueError("Título inválido")
        if not autor or not isinstance(autor, str):
            raise ValueError("Autor inválido")
        if not isinstance(quantidade_total, int) or quantidade_total < 0:
            raise ValueError("Quantidade inválida")
        
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.quantidade_total = quantidade_total
        self.quantidade_disponivel = quantidade_total
    
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'titulo': self.titulo,
            'autor': self.autor,
            'quantidade_total': self.quantidade_total,
            'quantidade_disponivel': self.quantidade_disponivel,
            'status': 'disponível' if self.quantidade_disponivel > 0 else 'indisponível'
        }
    
    @staticmethod
    def from_dict(data):
        livro = Livro(data['codigo'], data['titulo'], data['autor'], data['quantidade_total'])
        livro.quantidade_disponivel = data.get('quantidade_disponivel', data['quantidade_total'])
        return livro
    
    def emprestar(self):
        if self.quantidade_disponivel <= 0:
            raise ValueError("Livro indisponível")
        self.quantidade_disponivel -= 1
    
    def devolver(self):
        if self.quantidade_disponivel >= self.quantidade_total:
            raise ValueError("Todas as cópias já foram devolvidas")
        self.quantidade_disponivel += 1


class LivroRepository:
    def __init__(self):
        self.livros = {}
    
    def cadastrar(self, livro):
        if livro.codigo in self.livros:
            raise ValueError("Livro já cadastrado")
        self.livros[livro.codigo] = livro
        return livro
    
    def buscar(self, codigo):
        if codigo not in self.livros:
            return None
        return self.livros[codigo]
    
    def listar(self):
        return list(self.livros.values())
    
    def editar(self, codigo, titulo=None, autor=None, quantidade_total=None):
        livro = self.buscar(codigo)
        if not livro:
            raise ValueError("Livro não encontrado")
        
        if titulo:
            livro.titulo = titulo
        if autor:
            livro.autor = autor
        if quantidade_total is not None:
            if not isinstance(quantidade_total, int) or quantidade_total < 0:
                raise ValueError("Quantidade inválida")
            diferenca = quantidade_total - livro.quantidade_total
            livro.quantidade_total = quantidade_total
            livro.quantidade_disponivel += diferenca
            if livro.quantidade_disponivel < 0:
                livro.quantidade_disponivel = 0
        
        return livro
    
    def remover(self, codigo):
        if codigo not in self.livros:
            raise ValueError("Livro não encontrado")
        del self.livros[codigo]
        return True
    
    def verificar_disponibilidade(self, codigo):
        livro = self.buscar(codigo)
        if not livro:
            return False
        return livro.quantidade_disponivel > 0