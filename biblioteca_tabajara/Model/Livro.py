class Livro:
    def __init__(self, id, titulo, autor, estoque, status="disponível"):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.estoque = estoque
        self.status = status

    def get_id(self):
        return self.id

    def get_titulo(self):
        return self.titulo

    def get_autor(self):
        return self.autor

    def get_estoque(self):
        return self.estoque

    def get_status(self):
        return self.status

    def set_status(self, novo_status):
        self.status = novo_status

    def emprestar(self):
        if self.estoque > 0:
            self.estoque -= 1
            if self.estoque == 0:
                self.status = "emprestado"
        else:
            raise ValueError("Livro indisponível para empréstimo")

    def devolver(self):
        self.estoque += 1
        self.status = "disponível"
