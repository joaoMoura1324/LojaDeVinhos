from ui.main_panel import MainPanel
from data.database import initialize_database
import customtkinter as ctk

def main():
    """
    Função principal que inicializa a aplicação de gestão de vinhos.

    Configura a aparência da interface com customtkinter, inicializa a base de dados,
    cria o painel principal da aplicação e executa o loop principal da interface.

    Returns:
        None
    """
    # Configuração inicial do customtkinter
    ctk.set_appearance_mode("dark")  # Define o tema da aplicação (dark ou light)
    ctk.set_default_color_theme("blue")  # Define o tema de cor (blue, green, etc.)

    # Inicializar a base de dados
    initialize_database()
    print("Bem-vindo à aplicação de gestão de vinhos!")

    # Inicializar o painel principal
    root = ctk.CTk()
    app = MainPanel(root)
    root.mainloop()

if __name__ == "__main__":
    main()
