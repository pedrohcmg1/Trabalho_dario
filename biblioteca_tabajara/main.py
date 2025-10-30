from Controller.LivroController import LivroController

def main():
    controller = LivroController()
    controller.cadastrar_livro(1, "1984", "George Orwell", 3)
    controller.cadastrar_livro(2, "Dom Casmurro", "Machado de Assis", 2)
    
    for livro in controller.listar_livros():
        print(f"{livro.get_id()} - {livro.get_titulo()} ({livro.get_autor()}) [{livro.get_status()}]")

if __name__ == "__main__":
    main()
