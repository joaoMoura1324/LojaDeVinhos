import customtkinter as ctk
from logic.wine_management import fetch_wines
from ui.login_and_register import LoginAndRegister
from logic.user_management import update_user_profile
from datetime import datetime
import sqlite3

class MainPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão e Comercialização de Vinhos")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Centralizar a janela na tela
        self.center_window(800, 600)

        # Navegação superior
        self.nav_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.nav_frame.pack(fill="x", pady=10)

        self.create_nav_button("Catálogo", self.show_catalog)
        self.create_nav_button("Carrinho", self.open_cart)
        self.create_nav_button("Login", self.open_login)

        # Conteúdo principal
        self.content_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Inicializar estado do usuário
        self.user_logged_in = False
        self.cart = []  # Lista para armazenar itens no carrinho

        # Mostrar o catálogo por padrão
        self.show_catalog()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_nav_button(self, text, command):
        btn = ctk.CTkButton(self.nav_frame, text=text, command=command, corner_radius=10)
        btn.pack(side="left", padx=10, pady=5)

    def show_catalog(self):
        self.clear_content()
        ctk.CTkLabel(self.content_frame, text="Catálogo de Vinhos", font=("Arial", 16)).pack(pady=10)

        # Criar um canvas para rolagem vertical
        canvas = ctk.CTkCanvas(self.content_frame, bg="#2a2d2e", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        scroll = ctk.CTkScrollbar(self.content_frame, command=canvas.yview)
        scroll.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scroll.set)

        wines_frame = ctk.CTkFrame(canvas, corner_radius=10)
        canvas.create_window((0, 0), window=wines_frame, anchor="n")

        wines = fetch_wines()

        for wine in wines:
            wine_frame = ctk.CTkFrame(wines_frame, corner_radius=10, fg_color="#3b3b3b", width=500, height=150)
            wine_frame.pack(padx=10, pady=5)
            wine_frame.pack_propagate(False)

            # Container centralizado
            inner_frame = ctk.CTkFrame(wine_frame, fg_color="#3b3b3b")
            inner_frame.pack(expand=True)

            wine_info = f"Nome: {wine['marca']}\nAno: {wine['ano']}\nRegião: {wine['regiao']}\nPreço: {wine['preco']}€\nDescrição: {wine['descricao']}"
            ctk.CTkLabel(inner_frame, text=wine_info, justify="left").pack(pady=5)

            add_button = ctk.CTkButton(inner_frame, text="Adicionar ao Carrinho", command=lambda w=wine: self.add_to_cart(w))
            add_button.pack(pady=5)

        wines_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.update()

        # Centralizar o wines_frame
        canvas_width = canvas.winfo_width()
        wines_frame.update_idletasks()
        wines_frame_width = wines_frame.winfo_width()
        canvas.create_window((canvas_width // 2 - wines_frame_width // 2, 0), window=wines_frame, anchor="n")

    def add_to_cart(self, wine):
        if self.user_logged_in:
            self.cart.append(wine)
            self.show_message(f"{wine['marca']} adicionado ao carrinho!", callback=self.show_catalog)
        else:
            self.show_message("precisas de estar logado para adicionar itens ao carrinho.", success=False)


    def show_login_message(self):
        login_window = ctk.CTkToplevel(self.root)
        login_window.title("Aviso")
        login_window.geometry("300x150")
        login_window.resizable(False, False)
        login_window.attributes('-topmost', True)  # Garante que a mensagem aparece por cima do painel principal

        # Centralizar a janela
        screen_width = login_window.winfo_screenwidth()
        screen_height = login_window.winfo_screenheight()
        x = (screen_width // 2) - (300 // 2)
        y = (screen_height // 2) - (150 // 2)
        login_window.geometry(f"300x150+{x}+{y}")

        ctk.CTkLabel(login_window, text="Tem que estar logado na app!", font=("Arial", 12), wraplength=250).pack(pady=20)

        ctk.CTkButton(login_window, text="Login", command=lambda: self.close_and_open_profile(login_window)).pack(pady=10)

    def close_and_open_profile(self, login_window):
        login_window.destroy()
        self.open_login()

    def update_main_panel_for_user(self, user_name, user_id, user_email):
        self.user_name = user_name
        self.user_id = user_id
        self.user_email = user_email
        # Atualizar a barra de navegação
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        # Adicionar novos botões e informações para o utilizador logado
        self.create_nav_button("Catálogo", self.show_catalog)
        self.create_nav_button("Carrinho", self.open_cart)
        self.create_nav_button("Perfil", self.open_profile)

        # Mostrar o nome do utilizador
        user_label = ctk.CTkLabel(self.nav_frame, text=f"Bem-vindo, {user_name}", font=("Arial", 14))
        user_label.pack(side="right", padx=10)

        # Botão de logout
        ctk.CTkButton(self.nav_frame, text="Logout", command=self.logout_action).pack(side="right", padx=10)

        # Permitir acesso ao carrinho
        self.user_logged_in = True
        self.show_catalog()

    def logout_action(self):
        self.user_logged_in = False
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        self.create_nav_button("Catálogo", self.show_catalog)
        self.create_nav_button("Carrinho", self.show_login_message)  # Carrinho volta a pedir login
        self.create_nav_button("Login", self.open_login)
        self.show_catalog()

    def open_cart(self):
        if not self.user_logged_in:
            self.show_login_message()
        else:
            self.clear_content()
            ctk.CTkLabel(self.content_frame, text="Carrinho de Compras", font=("Arial", 16)).pack(pady=10)

        for item in self.cart:
            ctk.CTkLabel(self.content_frame, text=f"{item['marca']} - {item['preco']}€", font=("Arial", 14)).pack(pady=5)

        # Botão de comprar
        ctk.CTkButton(
            self.content_frame,
            text="Comprar",
            command=self.complete_purchase
        ).pack(pady=20)

    def complete_purchase(self):
        if not self.cart:
            self.show_message("O carrinho está vazio.", success=False)
            return

        from logic.wine_management import process_purchase
        result = process_purchase(self.cart, self.user_id)  # Passa o user_id do logado
        self.show_message(result, success=True if "sucesso" in result else False)

        if "sucesso" in result:
            self.cart.clear()  # Limpa o carrinho após a compra

    def open_login(self):
        # Limpa o conteúdo da interface atual
        self.clear_content()

        # Recria o painel de login
        login_screen = LoginAndRegister(self.content_frame, self)

        # Atualiza os atributos do utilizador para garantir que estão limpos
        self.user_name = None
        self.user_email = None
        self.user_id = None
        self.user_logged_in = False

    def open_profile(self):
        self.clear_content()
        ctk.CTkLabel(
            self.content_frame,
            text="Perfil do Utilizador",
            font=("Arial", 18, "bold"),
        ).pack(pady=20)
        ctk.CTkLabel(
            self.content_frame,
            text=f"Bem-vindo ao seu perfil!",
            font=("Arial", 16),
        ).pack(pady=10)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_message(self, message, success=True, callback=None):
        """Exibe uma mensagem popup e executa uma ação opcional após fechar."""
        popup = ctk.CTkToplevel(self.root)
        popup.title("Aviso")
        popup.geometry("400x200")
        popup.attributes('-topmost', True)

        # Centralizar o popup
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (200 // 2)
        popup.geometry(f"400x200+{x}+{y}")

        ctk.CTkLabel(
            popup,
            text=message,
            font=("Arial", 14),
            wraplength=350,
            justify="center"
        ).pack(pady=40)

        def on_close():
            popup.destroy()
            if callback:
                callback()  # Executa a ação personalizada, se fornecida

        ctk.CTkButton(
            popup,
            text="OK",
            command=on_close
        ).pack(pady=10)

        
    def complete_purchase(self):
        if not self.cart:
            self.show_message("O carrinho está vazio.", success=False)
            return

        from logic.wine_management import process_purchase
        result = process_purchase(self.cart, self.user_id)
        success = "sucesso" in result.lower()

        self.show_message(result, success=success, callback=self.show_catalog if success else None)

        if success:
            self.cart.clear()  # Limpa o carrinho após a compra


    def open_profile(self):
        self.clear_content()

        # Verifica se o utilizador está logado
        if not self.user_logged_in or not self.user_name or not self.user_email:
            self.show_message("Erro: Nenhum utilizador logado.", success=False)
            self.open_login()
            return

        ctk.CTkLabel(
            self.content_frame,
            text="Perfil do Utilizador",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        # Criar o formulário
        form_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        form_frame.pack(pady=10, padx=20, fill="both")

        ctk.CTkLabel(form_frame, text="Nome:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = ctk.CTkEntry(form_frame, font=("Arial", 14))
        name_entry.insert(0, self.user_name if self.user_name else "")  # Usa string vazia como fallback
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Email:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        email_entry = ctk.CTkEntry(form_frame, font=("Arial", 14))
        email_entry.insert(0, self.user_email if self.user_email else "")  # Usa string vazia como fallback
        email_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Password:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        password_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=10)

        # Botão para salvar alterações
        ctk.CTkButton(
            form_frame,
            text="Salvar Alterações",
            command=lambda: self.update_profile(name_entry.get(), email_entry.get(), password_entry.get())
        ).grid(row=3, column=0, columnspan=2, pady=20)

        # Botão para eliminar conta
        ctk.CTkButton(
            form_frame,
            text="Eliminar Conta",
            command=self.delete_account,
            fg_color="red"
        ).grid(row=4, column=0, columnspan=2, pady=20)

        # Botão para voltar ao catálogo
        ctk.CTkButton(
            self.content_frame,
            text="Voltar ao Catálogo",
            command=self.show_catalog
        ).pack(pady=10)
        
    def update_user_profile(user_id, name, email, password):
        try:
            connection = sqlite3.connect("data/database.db")
            cursor = connection.cursor()

            # Atualizar os dados na tabela Users
            cursor.execute("""
                UPDATE Users
                SET nome = ?, email = ?, password = ?
                WHERE id = ?
            """, (name, email, password, user_id))

            connection.commit()
            return True, "Perfil atualizado com sucesso!"
        except sqlite3.Error as e:
            return False, f"Erro ao atualizar perfil: {e}"
        finally:
            connection.close()
            
    def update_profile(self, name, email, password):
        if not name or not email or not password:
            self.show_message("Todos os campos são obrigatórios.", success=False)
            return

        from logic.user_management import update_user_profile

        # Atualizar os dados do utilizador na base de dados
        success, message = update_user_profile(self.user_id, name, email, password)

        if success:
            # Atualiza os atributos do utilizador no MainPanel
            self.user_name = name
            self.user_email = email
            self.show_message(message, success=True)

            # Recria o painel de perfil para refletir as mudanças
            self.open_profile()
        else:
            self.show_message(message, success=False)
            
    def delete_account(self):
        from logic.user_management import delete_user_account

        confirm = ctk.CTkToplevel(self.root)
        confirm.title("Confirmar Eliminação")
        confirm.geometry("400x200")
        confirm.attributes('-topmost', True)

        # Centralizar a mensagem
        screen_width = confirm.winfo_screenwidth()
        screen_height = confirm.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (200 // 2)
        confirm.geometry(f"400x200+{x}+{y}")

        ctk.CTkLabel(confirm, text="Tem certeza que deseja eliminar sua conta?", font=("Arial", 14), wraplength=350).pack(pady=20)
        ctk.CTkButton(confirm, text="Sim", command=lambda: [self.confirm_delete(confirm)]).pack(pady=10)
        ctk.CTkButton(confirm, text="Cancelar", command=confirm.destroy).pack(pady=10)

    def confirm_delete(self, confirm_window):
        from logic.user_management import delete_user_account

        # Eliminar o utilizador da base de dados
        success, message = delete_user_account(self.user_id)
        confirm_window.destroy()

        if success:
            # Limpar os dados do utilizador
            self.user_name = None
            self.user_email = None
            self.user_id = None
            self.user_logged_in = False

            # Limpar a navegação e voltar ao estado inicial
            for widget in self.nav_frame.winfo_children():
                widget.destroy()

            self.create_nav_button("Catálogo", self.show_catalog)
            self.create_nav_button("Carrinho", self.show_login_message)
            self.create_nav_button("Login", self.open_login)

            # Mostrar mensagem de sucesso e voltar ao menu inicial
            self.show_message("Conta eliminada com sucesso. Faça login novamente.", success=True)
            self.open_login()
        else:
            self.show_message(message, success=False)

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainPanel(root)
    root.mainloop()
