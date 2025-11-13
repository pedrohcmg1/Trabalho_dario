from collections import Counter

class RelatorioService:
    def __init__(self, usuario_repository, livro_repository, emprestimo_repository):
        self.usuario_repository = usuario_repository
        self.livro_repository = livro_repository
        self.emprestimo_repository = emprestimo_repository
    
    def livros_mais_emprestados(self, limite=10):
        """Retorna os livros mais emprestados"""
        emprestimos = self.emprestimo_repository.listar()
        
        contagem = Counter(e.codigo_livro for e in emprestimos)
        
        resultado = []
        for codigo_livro, quantidade in contagem.most_common(limite):
            livro = self.livro_repository.buscar(codigo_livro)
            if livro:
                resultado.append({
                    'codigo': codigo_livro,
                    'titulo': livro.titulo,
                    'autor': livro.autor,
                    'quantidade_emprestimos': quantidade
                })
        
        return resultado
    
    def usuarios_mais_ativos(self, limite=10):
        """Retorna os usuários com mais empréstimos"""
        emprestimos = self.emprestimo_repository.listar()
        
        contagem = Counter(e.matricula_usuario for e in emprestimos)
        
        resultado = []
        for matricula, quantidade in contagem.most_common(limite):
            usuario = self.usuario_repository.buscar(matricula)
            if usuario:
                resultado.append({
                    'matricula': matricula,
                    'nome': usuario.nome,
                    'tipo_usuario': usuario.tipo_usuario,
                    'quantidade_emprestimos': quantidade
                })
        
        return resultado
    
    def status_acervo(self):
        """Retorna estatísticas gerais do acervo"""
        livros = self.livro_repository.listar()
        
        total_livros = len(livros)
        total_exemplares = sum(l.quantidade_total for l in livros)
        exemplares_disponiveis = sum(l.quantidade_disponivel for l in livros)
        exemplares_emprestados = total_exemplares - exemplares_disponiveis
        
        return {
            'total_titulos': total_livros,
            'total_exemplares': total_exemplares,
            'exemplares_disponiveis': exemplares_disponiveis,
            'exemplares_emprestados': exemplares_emprestados
        }
    
    def status_usuarios(self):
        """Retorna estatísticas de usuários"""
        usuarios = self.usuario_repository.listar()
        
        total_usuarios = len(usuarios)
        usuarios_ativos = sum(1 for u in usuarios if u.ativo)
        usuarios_inativos = total_usuarios - usuarios_ativos
        
        por_tipo = Counter(u.tipo_usuario for u in usuarios)
        
        return {
            'total_usuarios': total_usuarios,
            'usuarios_ativos': usuarios_ativos,
            'usuarios_inativos': usuarios_inativos,
            'por_tipo': dict(por_tipo)
        }
    
    def emprestimos_ativos(self):
        """Retorna lista de empréstimos ativos"""
        emprestimos = self.emprestimo_repository.listar_ativos()
        
        resultado = []
        for emprestimo in emprestimos:
            usuario = self.usuario_repository.buscar(emprestimo.matricula_usuario)
            livro = self.livro_repository.buscar(emprestimo.codigo_livro)
            
            if usuario and livro:
                resultado.append({
                    'id_emprestimo': emprestimo.id_emprestimo,
                    'usuario_nome': usuario.nome,
                    'usuario_matricula': usuario.matricula,
                    'livro_titulo': livro.titulo,
                    'livro_codigo': livro.codigo,
                    'data_emprestimo': emprestimo.data_emprestimo.isoformat(),
                    'data_devolucao_prevista': emprestimo.data_devolucao_prevista.isoformat()
                })
        
        return resultado
    
    def relatorio_completo(self):
        """Retorna relatório completo do sistema"""
        return {
            'acervo': self.status_acervo(),
            'usuarios': self.status_usuarios(),
            'livros_mais_emprestados': self.livros_mais_emprestados(5),
            'usuarios_mais_ativos': self.usuarios_mais_ativos(5),
            'total_emprestimos': len(self.emprestimo_repository.listar()),
            'emprestimos_ativos': len(self.emprestimo_repository.listar_ativos())
        }