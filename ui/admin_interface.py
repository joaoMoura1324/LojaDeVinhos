import customtkinter as ctk

class AdminInterface:
    """
    Interface administrativa para gestão de vinhos e análise de vendas.

    Permite:
        - Gerir vinhos: listar, criar, editar e eliminar.
        - Visualizar vendas: exibir uma tabela de vendas mensais e exportar para CSV.
        - Encerrar a aplicação.
    """

    def __init__(self, root):
        """
        Inicializa a interface administrativa.

        Args:
            root: A janela principal onde a interface será exibida.
        """
        self.root = root
        self.root.title("Painel do Administrador")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Centralizar a janela na tela
        self.center_window(800, 600)

        # Painel de navegação
        nav_frame = ctk.CTkFrame(self.root, corner_radius=10)
        nav_frame.pack(fill="x", pady=10)

        # Botões de navegação
        ctk.CTkButton(nav_frame, text="Gestão de Vinhos", command=self.manage_wines).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Análise de Vendas", command=self.view_sales).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text="Sair", command=self.exit_application).pack(side="right", padx=10)

        # Conteúdo principal
        self.content_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.content_frame, text="Bem-vindo, Administrador!", font=("Arial", 24)).pack(pady=20)

    def center_window(self, width, height):
        """
        Centraliza a janela na tela.

        Args:
            width (int): Largura da janela.
            height (int): Altura da janela.
        """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def manage_wines(self):
        """
        Exibe a interface para gestão de vinhos.

        Permite listar, criar, editar e eliminar vinhos.
        """
        from logic.wine_management import fetch_wines  # Função para obter vinhos da base de dados

        # Limpar conteúdo anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.content_frame, text="Gestão de Vinhos", font=("Arial", 18, "bold")).pack(pady=10)

        # Criar tabela para exibir vinhos
        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        wine_list = fetch_wines()  # Obter vinhos do banco de dados

        if wine_list:
            # Cabeçalhos da tabela
            headers = ["ID", "Marca", "Preço", "Região", "Ano", "Descrição"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(
                    table_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    anchor="center",
                    fg_color="#3b3b3b"
                ).grid(row=0, column=col, padx=5, pady=5)

            # Configurar proporções das colunas
            for col in range(len(headers)):
                table_frame.grid_columnconfigure(col, weight=1)

            # Preencher tabela com vinhos
            for row, wine in enumerate(wine_list, start=1):
                for col, value in enumerate(wine.values()):
                    ctk.CTkLabel(
                        table_frame,
                        text=value,
                        font=("Arial", 12),
                        anchor="center",
                    ).grid(row=row, column=col, padx=5, pady=2)
        else:
            ctk.CTkLabel(self.content_frame, text="Nenhum vinho encontrado.", font=("Arial", 14)).pack(pady=10)

        # Área de ações
        action_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        action_frame.pack(pady=20)

        ctk.CTkButton(action_frame, text="Eliminar", command=self.delete_selected_wine).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Editar", command=self.edit_selected_wine).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Criar Novo Vinho", command=self.create_new_wine).pack(side="left", padx=10)

    def view_sales(self):
        """
        Exibe a interface de análise de vendas.

        Mostra uma tabela de vendas mensais e permite exportar os dados como CSV.
        """
        from logic.sales_management import fetch_monthly_sales, export_sales_to_csv

        # Limpar conteúdo anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.content_frame, text="Análise de Vendas", font=("Arial", 18, "bold")).pack(pady=10)

        # Criar tabela para exibir vendas
        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        sales = fetch_monthly_sales()  # Obter vendas do banco de dados

        if sales:
            headers = ["ID Venda", "ID Utilizador", "ID Vinho", "Data", "Quantidade"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(
                    table_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    anchor="center",
                    fg_color="#3b3b3b"
                ).grid(row=0, column=col, padx=5, pady=5)

            # Preencher tabela com vendas
            for row, sale in enumerate(sales, start=1):
                for col, value in enumerate(sale):
                    ctk.CTkLabel(
                        table_frame,
                        text=value,
                        font=("Arial", 12),
                        anchor="center",
                    ).grid(row=row, column=col, padx=5, pady=2)
        else:
            ctk.CTkLabel(self.content_frame, text="Nenhuma venda encontrada.", font=("Arial", 14)).pack(pady=10)

        # Botão para exportar como CSV
        export_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        export_frame.pack(pady=20)

        def export_csv():
            success, message = export_sales_to_csv()
            self.show_message(message, success=success)

        ctk.CTkButton(export_frame, text="Exportar para CSV", command=export_csv).pack(pady=10)

    def exit_application(self):
        """
        Encerra a aplicação.
        """
        self.root.destroy()

    def manage_wines(self):
        """
        Exibe a interface para gestão de vinhos.

        Permite listar todos os vinhos da base de dados, bem como realizar ações como
        eliminar, editar e criar novos vinhos.
        """
        from logic.wine_management import fetch_wines  # Importa a função para buscar vinhos do banco de dados

        # Limpa o conteúdo anterior da área principal para exibir os novos elementos
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Adiciona o título da seção
        ctk.CTkLabel(self.content_frame, text="Gestão de Vinhos", font=("Arial", 18, "bold")).pack(pady=10)

        # Cria um frame para conter a tabela que exibirá os vinhos
        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Obtém a lista de vinhos do banco de dados
        wine_list = fetch_wines()

        if wine_list:
            # Cria os cabeçalhos da tabela
            headers = ["ID", "Marca", "Preço", "Região", "Ano", "Descrição"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(
                    table_frame,
                    text=header,
                    font=("Arial", 12, "bold"),
                    width=15,
                    anchor="center",
                    fg_color="#3b3b3b",  # Fundo escuro para destaque
                ).grid(row=0, column=col, padx=5, pady=5)

            # Preenche a tabela com os dados de cada vinho
            for row, wine in enumerate(wine_list, start=1):  # Começa na linha 1, pois a linha 0 é para os cabeçalhos
                for col, value in enumerate(wine.values()):
                    ctk.CTkLabel(
                        table_frame,
                        text=value,  # Dados do vinho
                        font=("Arial", 12),
                        width=15,
                        anchor="center",
                    ).grid(row=row, column=col, padx=5, pady=2)
        else:
            # Caso nenhum vinho seja encontrado, exibe uma mensagem
            ctk.CTkLabel(self.content_frame, text="Nenhum vinho encontrado.", font=("Arial", 14)).pack(pady=10)

        # Cria a área para os botões de ação
        action_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        action_frame.pack(pady=20)

        # Botão para eliminar vinhos
        ctk.CTkButton(action_frame, text="Eliminar", command=self.delete_selected_wine).pack(side="left", padx=10)

        # Botão para editar vinhos
        ctk.CTkButton(action_frame, text="Editar", command=self.edit_selected_wine).pack(side="left", padx=10)

        # Botão para criar novos vinhos
        ctk.CTkButton(action_frame, text="Criar Novo Vinho", command=self.create_new_wine).pack(side="left", padx=10)


    def delete_selected_wine(self):
        """
        Abre um popup para eliminar um vinho da base de dados.

        Solicita ao utilizador que insira o ID do vinho que deseja eliminar. Após
        validar o ID, remove o vinho correspondente do banco de dados e atualiza
        a tabela de vinhos exibida.
        """
        # Criar uma janela popup para entrada do ID
        popup = ctk.CTkToplevel(self.root)
        popup.title("Eliminar Vinho")
        popup.geometry("400x200")
        popup.attributes('-topmost', True)  # Garante que o popup fique no topo da janela principal

        # Centralizar o popup na tela
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (200 // 2)
        popup.geometry(f"400x200+{x}+{y}")

        # Adicionar um rótulo explicativo e um campo de entrada para o ID
        ctk.CTkLabel(
            popup, 
            text="Digite o ID do vinho que deseja eliminar:", 
            font=("Arial", 14)
        ).pack(pady=10)

        wine_id_entry = ctk.CTkEntry(popup, font=("Arial", 14), width=300)
        wine_id_entry.pack(pady=10)

        # Função para confirmar e realizar a eliminação do vinho
        def confirm_delete():
            wine_id = wine_id_entry.get()

            # Validar se o ID é um número
            if not wine_id.isdigit():
                self.show_message("Por favor, insira um ID válido.", success=False)
            else:
                from logic.wine_management import delete_wine
                success, message = delete_wine(int(wine_id))  # Tentar eliminar o vinho com o ID fornecido
                self.show_message(message, success=success)
                if success:
                    self.manage_wines()  # Recarregar a tabela de vinhos atualizada
                popup.destroy()

        # Botão para confirmar a eliminação
        ctk.CTkButton(popup, text="Eliminar", command=confirm_delete).pack(pady=10)

        # Botão para cancelar a ação e fechar o popup
        ctk.CTkButton(popup, text="Cancelar", command=popup.destroy).pack(pady=10)

    def edit_selected_wine(self):
        """
        Seleciona um vinho para edição.

        Verifica se há um vinho selecionado na tabela. Caso contrário, exibe uma
        mensagem de erro. Se houver, exibe o ID do vinho a ser editado.
        """
        # Obter o vinho atualmente selecionado
        selected_wine = self.get_selected_wine()

        # Verificar se algum vinho foi selecionado
        if not selected_wine:
            self.show_message("Nenhum vinho selecionado para editar.", success=False)
            return

        # Exibir mensagem temporária indicando o ID do vinho selecionado
        self.show_message(f"Editar vinho com ID: {selected_wine['id']}", success=True)

    def create_new_wine(self):
        """
        Abre um popup para criar um novo vinho.

        Permite ao utilizador inserir as informações necessárias para criar um novo vinho
        na base de dados. Exibe uma mensagem de confirmação após a criação.
        """
        # Exibe uma mensagem indicando que a funcionalidade de criação foi ativada
        self.show_message("Criar um novo vinho", success=True)


    def get_selected_wine(self):
        """
        Obtém o vinho selecionado na tabela.

        Lógica que deve retornar os dados do vinho atualmente selecionado na tabela
        de vinhos. Se nenhum vinho for selecionado, retorna `None`.

        Returns:
            dict | None: Um dicionário com os dados do vinho selecionado, ou `None`
            se nenhum vinho estiver selecionado.
        """
        # Retorna os dados do vinho selecionado na tabela
        # Exemplo: Implementar a lógica de seleção na tabela futuramente
        return None

    def show_message(self, message, success):
        """
        Exibe uma mensagem popup na tela.

        O popup aparece no topo da interface principal e exibe uma mensagem de aviso ou
        sucesso. O botão "OK" fecha o popup.

        Args:
            message (str): A mensagem a ser exibida.
            success (bool): Indica se a operação foi bem-sucedida (True) ou falhou (False).
        """
        # Criação do popup
        popup = ctk.CTkToplevel(self.root)
        popup.title("Aviso")
        popup.geometry("400x150")
        popup.attributes('-topmost', True)  # Garante que o popup fique no topo

        # Centralizar o popup no topo da tela
        screen_width = popup.winfo_screenwidth()
        x = (screen_width // 2) - (400 // 2)  # Centraliza horizontalmente
        popup.geometry(f"400x150+{x}+50")  # Ajusta para ficar 50px do topo

        # Rótulo para exibir a mensagem
        ctk.CTkLabel(
            popup,
            text=message,
            font=("Arial", 14),
            justify="center",  # Centraliza o texto
            wraplength=350,    # Limita a largura do texto para quebrar linhas
        ).pack(pady=20)

        # Botão para fechar o popup
        ctk.CTkButton(
            popup,
            text="OK",
            command=popup.destroy,  # Fecha o popup ao clicar
        ).pack(pady=10)
        
    def create_new_wine(self):
        """
        Abre um painel para criar um novo vinho.

        Permite ao utilizador inserir informações como marca, preço, região, ano e descrição
        de um vinho. Após validar os dados, o vinho é adicionado ao banco de dados e a tabela
        de vinhos é recarregada.
        """
        # Criar um popup para o formulário
        popup = ctk.CTkToplevel(self.root)
        popup.title("Criar Novo Vinho")
        popup.geometry("500x500")
        popup.attributes('-topmost', True)  # Garante que o popup esteja no topo da janela principal

        # Centralizar o popup na tela
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (400 // 2)
        popup.geometry(f"500x500+{x}+{y}")

        # Título do formulário
        ctk.CTkLabel(popup, text="Criar Novo Vinho", font=("Arial", 18, "bold")).pack(pady=10)

        # Frame para organizar os campos do formulário
        form_frame = ctk.CTkFrame(popup)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Campos do formulário
        ctk.CTkLabel(form_frame, text="Marca:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        marca_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        marca_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Preço:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        preco_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        preco_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Região:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        regiao_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        regiao_entry.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Ano:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        ano_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        ano_entry.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Descrição:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        descricao_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        descricao_entry.grid(row=4, column=1, padx=10, pady=10)

        # Função para processar a criação do novo vinho
        def process_create():
            """
            Processa os dados do formulário e cria um novo vinho na base de dados.

            Valida os campos obrigatórios e verifica os tipos de dados (como preço e ano).
            Se a criação for bem-sucedida, recarrega a tabela de vinhos e fecha o popup.
            """
            # Obter os valores dos campos do formulário
            marca = marca_entry.get()
            preco = preco_entry.get()
            regiao = regiao_entry.get()
            ano = ano_entry.get()
            descricao = descricao_entry.get()

            # Validar se todos os campos foram preenchidos
            if not all([marca, preco, regiao, ano, descricao]):
                self.show_message("Todos os campos são obrigatórios.", success=False)
                return

            # Validar os tipos dos campos (preço e ano devem ser numéricos)
            try:
                preco = float(preco)
                ano = int(ano)
            except ValueError:
                self.show_message("Preço deve ser um número e ano um inteiro.", success=False)
                return

            # Criar o vinho no banco de dados
            from logic.wine_management import create_wine
            success, message = create_wine(marca, preco, regiao, ano, descricao)
            self.show_message(message, success=success)

            if success:
                self.manage_wines()  # Recarregar a tabela de vinhos
                popup.destroy()  # Fechar o popup

        # Botões de ação
        ctk.CTkButton(popup, text="Criar", command=process_create).pack(pady=10)
        ctk.CTkButton(popup, text="Cancelar", command=popup.destroy).pack(pady=10)

        
    def edit_selected_wine(self):
        """
        Solicita o ID do vinho a ser editado e exibe o painel de edição.

        Abre um popup onde o utilizador pode inserir o ID do vinho. Após validar o ID,
        os dados do vinho são carregados e enviados para o painel de edição.
        """
        # Criar um popup para solicitar o ID do vinho
        popup = ctk.CTkToplevel(self.root)
        popup.title("Editar Vinho")
        popup.geometry("400x200")
        popup.attributes('-topmost', True)  # Garante que o popup fique no topo da interface principal

        # Centralizar o popup na tela
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (200 // 2)
        popup.geometry(f"400x200+{x}+{y}")

        # Rótulo e entrada para o ID
        ctk.CTkLabel(popup, text="Digite o ID do vinho que deseja editar:", font=("Arial", 14)).pack(pady=10)
        wine_id_entry = ctk.CTkEntry(popup, font=("Arial", 14), width=300)
        wine_id_entry.pack(pady=10)

        # Função para carregar os dados do vinho com base no ID
        def load_wine():
            wine_id = wine_id_entry.get()
            if not wine_id.isdigit():
                self.show_message("Por favor, insira um ID válido.", success=False)
                return

            # Buscar os dados do vinho na base de dados
            from logic.wine_management import fetch_wine_by_id
            success, wine = fetch_wine_by_id(int(wine_id))

            if success:
                popup.destroy()  # Fechar o popup de entrada do ID
                self.show_edit_panel(wine)  # Mostrar o painel de edição com os dados carregados
            else:
                self.show_message(wine, success=False)  # Exibir mensagem de erro caso o ID seja inválido

        # Botões para carregar o vinho ou cancelar a ação
        ctk.CTkButton(popup, text="Carregar", command=load_wine).pack(pady=10)
        ctk.CTkButton(popup, text="Cancelar", command=popup.destroy).pack(pady=10)



    def show_edit_panel(self, wine):
        """
        Exibe o painel de edição com os dados do vinho selecionado.

        Permite ao utilizador modificar os campos de um vinho já existente. Após a
        edição, os dados são validados e atualizados no banco de dados.

        Args:
            wine (dict): Dados do vinho selecionado para edição.
        """
        # Criar o popup para o formulário de edição
        popup = ctk.CTkToplevel(self.root)
        popup.title("Editar Vinho")
        popup.geometry("500x400")
        popup.attributes('-topmost', True)  # Garante que o popup fique no topo da interface principal

        # Centralizar o popup na tela
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (400 // 2)
        popup.geometry(f"500x400+{x}+{y}")

        # Título do formulário
        ctk.CTkLabel(popup, text="Editar Vinho", font=("Arial", 18, "bold")).pack(pady=10)

        # Frame para organizar os campos do formulário
        form_frame = ctk.CTkFrame(popup)
        form_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Campos do formulário preenchidos com os dados existentes
        ctk.CTkLabel(form_frame, text="Marca:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        marca_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        marca_entry.insert(0, wine["marca"])
        marca_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Preço:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        preco_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        preco_entry.insert(0, wine["preco"])
        preco_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Região:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        regiao_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        regiao_entry.insert(0, wine["regiao"])
        regiao_entry.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Ano:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        ano_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        ano_entry.insert(0, wine["ano"])
        ano_entry.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Descrição:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        descricao_entry = ctk.CTkEntry(form_frame, font=("Arial", 14), width=300)
        descricao_entry.insert(0, wine["descricao"])
        descricao_entry.grid(row=4, column=1, padx=10, pady=10)

        # Função para salvar as alterações
        def save_changes():
            """
            Salva as alterações feitas no vinho e atualiza os dados no banco.

            Valida os dados do formulário antes de atualizar a base de dados.
            """
            marca = marca_entry.get()
            preco = preco_entry.get()
            regiao = regiao_entry.get()
            ano = ano_entry.get()
            descricao = descricao_entry.get()

            # Validar se todos os campos foram preenchidos
            if not all([marca, preco, regiao, ano, descricao]):
                self.show_message("Todos os campos são obrigatórios.", success=False)
                return

            # Validar os tipos dos campos
            try:
                preco = float(preco)
                ano = int(ano)
            except ValueError:
                self.show_message("Preço deve ser um número e ano um inteiro.", success=False)
                return

            # Atualizar o vinho no banco de dados
            from logic.wine_management import edit_wine
            success, message = edit_wine(wine["id"], marca, preco, regiao, ano, descricao)
            self.show_message(message, success=success)

            if success:
                self.manage_wines()  # Recarrega a tabela de vinhos
                popup.destroy()

        # Botões para salvar alterações ou cancelar a ação
        ctk.CTkButton(popup, text="Salvar Alterações", command=save_changes).pack(pady=10)
        ctk.CTkButton(popup, text="Cancelar", command=popup.destroy).pack(pady=10)

    def view_sales(self):
        """
        Exibe uma tabela de vendas mensais detalhadas e permite exportar os dados como CSV.

        A tabela inclui informações como ID da venda, ID e nome do utilizador, ID e nome do vinho,
        preço e data da venda. Utiliza um canvas com barra de rolagem para exibir grandes volumes
        de dados e permite a exportação para CSV.
        """
        from logic.sales_management import fetch_monthly_sales, export_sales_to_csv

        # Limpar o conteúdo anterior na área principal
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Adicionar título da seção
        ctk.CTkLabel(self.content_frame, text="Análise de Vendas", font=("Arial", 18, "bold")).pack(pady=10)

        # Criar um container para a tabela com rolagem
        table_container = ctk.CTkFrame(self.content_frame, corner_radius=10)
        table_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas para possibilitar a rolagem
        canvas = ctk.CTkCanvas(table_container, bg="#2a2d2e", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        # Barra de rolagem vertical
        scrollbar = ctk.CTkScrollbar(table_container, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno onde a tabela será desenhada
        table_frame = ctk.CTkFrame(canvas, corner_radius=10)
        canvas.create_window((0, 0), window=table_frame, anchor="nw")

        # Buscar as vendas do banco de dados
        sales = fetch_monthly_sales()

        # Verificar se há dados de vendas disponíveis
        if not sales:
            ctk.CTkLabel(table_frame, text="Nenhuma venda encontrada.", font=("Arial", 14)).pack(pady=10)
            return

        # Criar os cabeçalhos da tabela
        headers = ["ID Venda", "ID Utilizador", "Nome Utilizador", "ID Vinho", "Nome Vinho", "Preço", "Data"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                anchor="center",
                fg_color="#3b3b3b"  # Cor de fundo escura para destaque
            )
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        # Configurar proporções das colunas para ajustarem ao espaço disponível
        for col in range(len(headers)):
            table_frame.grid_columnconfigure(col, weight=1)

        # Preencher a tabela com os dados das vendas
        for row, sale in enumerate(sales, start=1):  # Dados começam na linha 1 (linha 0 é para os cabeçalhos)
            for col, value in enumerate(sale):
                data_label = ctk.CTkLabel(
                    table_frame,
                    text=value,  # Dados individuais da venda
                    font=("Arial", 12),
                    anchor="center",
                )
                data_label.grid(row=row, column=col, padx=5, pady=2, sticky="ew")

        # Ajustar o tamanho do canvas para o conteúdo
        table_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Frame para o botão de exportação
        export_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        export_frame.pack(pady=20)

        # Função para exportar os dados para um arquivo CSV
        def export_csv():
            """
            Exporta os dados de vendas mensais para um arquivo CSV.

            Exibe uma mensagem de sucesso ou erro após a operação.
            """
            success, message = export_sales_to_csv()
            self.show_message(message, success=success)

        # Botão para exportar os dados
        ctk.CTkButton(export_frame, text="Exportar para CSV", command=export_csv).pack(pady=10)

