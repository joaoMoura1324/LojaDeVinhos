import sqlite3

# Caminho para a base de dados
DATABASE_PATH = "data/database.db"

def login_user(email, password):
    """
    Autentica um utilizador com base no email e password.

    Verifica as credenciais do utilizador na base de dados. Se as credenciais
    forem válidas, retorna os dados do utilizador.

    Args:
        email (str): O email do utilizador.
        password (str): A senha do utilizador.

    Returns:
        tuple: Um par (bool, dict ou str).
            - bool: True se o login for bem-sucedido, False caso contrário.
            - dict: Dados do utilizador se a autenticação for bem-sucedida.
            - str: Mensagem de erro se a autenticação falhar.
    """
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT id, nome, email, tipo FROM Users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            user_data = {
                "id": user[0],
                "nome": user[1],
                "email": user[2],
                "tipo": user[3]
            }
            return True, user_data
        else:
            return False, "Credenciais inválidas."
    except sqlite3.Error as e:
        return False, f"Erro ao autenticar utilizador: {e}"
    finally:
        connection.close()

def register_user(name, email, password, address1, address2, account_type="utilizador"):
    """
    Regista um novo utilizador na base de dados.

    Args:
        name (str): Nome do utilizador.
        email (str): Email do utilizador.
        password (str): Senha do utilizador.
        address1 (str): Endereço principal do utilizador.
        address2 (str): Endereço secundário do utilizador (opcional).
        account_type (str): Tipo de conta (`utilizador` ou `admin`). Padrão: 'utilizador'.

    Returns:
        tuple: Um par (bool, str).
            - bool: True se o registo for bem-sucedido, False caso contrário.
            - str: Mensagem indicando o status do registo.
    """
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Users (nome, email, password, morada1, morada2, tipo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, password, address1, address2, account_type))

        connection.commit()
        return True, "Conta criada com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: Email já está em uso."
    except sqlite3.Error as e:
        return False, f"Erro ao criar conta: {e}"
    finally:
        connection.close()

def fetch_user_data(user_id):
    """
    Obtém os dados de um utilizador com base no ID.

    Args:
        user_id (int): O ID do utilizador.

    Returns:
        tuple: Um par (bool, dict ou str).
            - bool: True se os dados forem encontrados, False caso contrário.
            - dict: Dados do utilizador se encontrados.
            - str: Mensagem de erro se o utilizador não for encontrado.
    """
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT id, nome, email, morada1, morada2, tipo FROM Users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            user_data = {
                "id": user[0],
                "nome": user[1],
                "email": user[2],
                "morada1": user[3],
                "morada2": user[4],
                "tipo": user[5]
            }
            return True, user_data
        else:
            return False, "Utilizador não encontrado."
    except sqlite3.Error as e:
        return False, f"Erro ao obter dados do utilizador: {e}"
    finally:
        connection.close()

def update_user_profile(user_id, name, email, password):
    """
    Atualiza o perfil de um utilizador na base de dados.

    Args:
        user_id (int): ID do utilizador.
        name (str): Novo nome do utilizador.
        email (str): Novo email do utilizador.
        password (str): Nova senha do utilizador.

    Returns:
        tuple: Um par (bool, str).
            - bool: True se a atualização for bem-sucedida, False caso contrário.
            - str: Mensagem indicando o status da operação.
    """
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

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

def delete_user_account(user_id):
    """
    Elimina o utilizador da base de dados com base no ID.

    Args:
        user_id (int): O ID do utilizador.

    Returns:
        tuple: Um par (bool, str).
            - bool: True se a exclusão for bem-sucedida, False caso contrário.
            - str: Mensagem indicando o status da operação.
    """
    try:
        connection = sqlite3.connect("data/database.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
        connection.commit()

        return True, "Conta eliminada com sucesso."
    except sqlite3.Error as e:
        return False, f"Erro ao eliminar conta: {e}"
    finally:
        connection.close()
