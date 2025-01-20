import customtkinter as ctk
from logic.user_management import login_user, register_user
from logic.user_auth import validate_user_data

class LoginAndRegister:
    """
    Classe responsável pelo sistema de login e registo de utilizadores.

    Permite que os utilizadores façam login, criem uma conta e alternem entre
    as telas de login e registo.
    """

    def __init__(self, parent, main_panel):
        """
        Inicializa o sistema de login e registo.

        Args:
            parent (object): O elemento pai onde o frame será renderizado.
            main_panel (object): Referência ao painel principal para troca de estado.
        """
        self.parent = parent
        self.main_panel = main_panel
        self.frame = ctk.CTkFrame(self.parent, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(self.frame, text="Bem-vindo", font=("Arial", 24, "bold")).pack(pady=40)

        # Área de login
        login_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        login_frame.pack(padx=50, pady=20)

        ctk.CTkLabel(login_frame, text="Email:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = ctk.CTkEntry(login_frame, font=("Arial", 14), width=300)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(login_frame, text="Password:", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(login_frame, show="*", font=("Arial", 14), width=300)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkButton(login_frame, text="Entrar", command=self.login_action).grid(row=2, column=0, columnspan=2, pady=20)

        # Linha de separação
        ctk.CTkLabel(self.frame, text="Ainda não tem conta?", font=("Arial", 14)).pack(pady=10)

        # Botão para registo
        ctk.CTkButton(self.frame, text="Registar", command=self.show_register).pack(pady=10)

    def show_register(self):
        """
        Exibe a interface de registo de utilizadores.
        """
        for widget in self.frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame, text="Criar Conta", font=("Arial", 24, "bold")).pack(pady=40)

        register_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        register_frame.pack(padx=30, pady=10)

        ctk.CTkLabel(register_frame, text="Nome:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = ctk.CTkEntry(register_frame, font=("Arial", 14), width=300)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(register_frame, text="Email:", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.register_email_entry = ctk.CTkEntry(register_frame, font=("Arial", 14), width=300)
        self.register_email_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(register_frame, text="Password:", font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.register_password_entry = ctk.CTkEntry(register_frame, show="*", font=("Arial", 14), width=300)
        self.register_password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(register_frame, text="Morada 1:", font=("Arial", 16)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.address1_entry = ctk.CTkEntry(register_frame, font=("Arial", 14), width=300)
        self.address1_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(register_frame, text="Morada 2 (opcional):", font=("Arial", 16)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.address2_entry = ctk.CTkEntry(register_frame, font=("Arial", 14), width=300)
        self.address2_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(register_frame, text="Tipo de Conta:", font=("Arial", 16)).grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.account_type = ctk.CTkComboBox(register_frame, values=["utilizador", "admin"], font=("Arial", 14))
        self.account_type.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.account_type.set("utilizador")

        ctk.CTkButton(register_frame, text="Registar", command=self.validate_and_register).grid(row=6, column=0, columnspan=2, pady=30)

    def login_action(self):
        """
        Processa o login do utilizador.

        Obtém as credenciais inseridas pelo utilizador, valida no banco de dados e
        redireciona para a interface correta dependendo do tipo de conta.

        Returns:
            None
        """
        email = self.email_entry.get()
        password = self.password_entry.get()

        success, user_data = login_user(email, password)

        if success:
            user_name = user_data['nome']
            user_id = user_data['id']
            user_type = user_data['tipo']

            if user_type == "admin":
                new_window = ctk.CTk()
                from ui.admin_interface import AdminInterface
                AdminInterface(new_window)
                new_window.mainloop()
            elif user_type == "utilizador":
                self.main_panel.update_main_panel_for_user(user_name, user_id, user_data['email'])
        else:
            self.show_message("Login falhou. Verifique suas credenciais.", success=False)

    def validate_and_register(self):
        """
        Valida os dados inseridos no registo e cria uma nova conta.

        Returns:
            None
        """
        name = self.name_entry.get()
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        address1 = self.address1_entry.get()
        address2 = self.address2_entry.get()
        account_type = self.account_type.get()

        errors = validate_user_data(name, name, email, password, address1)

        if errors:
            self.show_message("\n".join(errors), success=False)
            return

        success, message = register_user(name, email, password, address1, address2, account_type)

        if success:
            self.show_message("Conta criada com sucesso!", success=True)
        else:
            self.show_message(message, success=False)

    def show_message(self, message, success):
        """
        Exibe uma mensagem em uma janela popup.

        Args:
            message (str): O texto da mensagem a ser exibida.
            success (bool): Indica se a operação foi bem-sucedida.

        Returns:
            None
        """
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Aviso")
        popup.geometry("400x200")
        popup.attributes('-topmost', True)

        popup.update_idletasks()
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (200 // 2)
        popup.geometry(f"400x200+{x}+{y}")

        ctk.CTkLabel(popup, text=message, font=("Arial", 14), wraplength=350).pack(pady=40)
        ctk.CTkButton(
            popup,
            text="OK",
            command=lambda: [popup.destroy(), self.show_login() if success else None]
        ).pack(pady=10)

    def show_login(self):
        """
        Exibe a interface de login.

        Returns:
            None
        """
        for widget in self.frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.frame, text="Bem-vindo", font=("Arial", 24, "bold")).pack(pady=40)

        login_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        login_frame.pack(padx=50, pady=20)

        ctk.CTkLabel(login_frame, text="Email:", font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = ctk.CTkEntry(login_frame, font=("Arial", 14), width=300)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(login_frame, text="Password:", font=("Arial", 16)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(login_frame, show="*", font=("Arial", 14), width=300)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        ctk.CTkButton(login_frame, text="Entrar", command=self.login_action).grid(row=2, column=0, columnspan=2, pady=20)

        ctk.CTkLabel(self.frame, text="Ainda não tem conta?", font=("Arial", 14)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Registar", command=self.show_register).pack(pady=10)
