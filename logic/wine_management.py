import sqlite3
from datetime import datetime

def fetch_wines():
    """Busca todos os vinhos na tabela Vinhos."""
    connection = sqlite3.connect("data/database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, marca, preco, regiao, ano, descricao FROM Vinhos")
    wines = [
        {
            "id": row[0],
            "marca": row[1],
            "preco": row[2],
            "regiao": row[3],
            "ano": row[4],
            "descricao": row[5]
        }
        for row in cursor.fetchall()
    ]

    connection.close()
    return wines

def procurar_vinhos():
    """
    Procura todos os vinhos na tabela `Vinhos`.

    Returns:
        list: Lista de dicionários contendo os dados dos vinhos.
    """
    connection = sqlite3.connect("data/database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id, marca, preco, regiao, ano, descricao FROM Vinhos")
    vinhos = [
        {
            "id": row[0],
            "marca": row[1],
            "preco": row[2],
            "regiao": row[3],
            "ano": row[4],
            "descricao": row[5]
        }
        for row in cursor.fetchall()
    ]

    connection.close()
    return vinhos


def eliminar_vinho(vinho_id):
    """
    Elimina um vinho da tabela `Vinhos` com base no ID.

    Args:
        vinho_id (int): ID do vinho a ser eliminado.

    Returns:
        tuple: Um par (bool, str) indicando o sucesso ou falha da operação.
    """
    try:
        connection = sqlite3.connect("data/database.db")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Vinhos WHERE id = ?", (vinho_id,))
        connection.commit()

        return True, "Vinho eliminado com sucesso!"
    except sqlite3.Error as e:
        return False, f"Erro ao eliminar vinho: {e}"
    finally:
        connection.close()


def editar_vinho(vinho_id, marca, preco, regiao, ano, descricao):
    """
    Edita os dados de um vinho na tabela `Vinhos`.

    Args:
        vinho_id (int): ID do vinho a ser editado.
        marca (str): Nova marca do vinho.
        preco (float): Novo preço do vinho.
        regiao (str): Nova região do vinho.
        ano (int): Novo ano do vinho.
        descricao (str): Nova descrição do vinho.

    Returns:
        tuple: Um par (bool, str) indicando o sucesso ou falha da operação.
    """
    try:
        connection = sqlite3.connect("data/database.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Vinhos
            SET marca = ?, preco = ?, regiao = ?, ano = ?, descricao = ?
            WHERE id = ?
        """, (marca, preco, regiao, ano, descricao, vinho_id))
        connection.commit()

        return True, "Vinho editado com sucesso!"
    except sqlite3.Error as e:
        return False, f"Erro ao editar vinho: {e}"
    finally:
        connection.close()


def criar_vinho(marca, preco, regiao, ano, descricao):
    """
    Adiciona um novo vinho à tabela `Vinhos`.

    Args:
        marca (str): Marca do vinho.
        preco (float): Preço do vinho.
        regiao (str): Região do vinho.
        ano (int): Ano do vinho.
        descricao (str): Descrição do vinho.

    Returns:
        tuple: Um par (bool, str) indicando o sucesso ou falha da operação.
    """
    try:
        connection = sqlite3.connect("data/database.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Vinhos (marca, preco, regiao, ano, descricao)
            VALUES (?, ?, ?, ?, ?)
        """, (marca, preco, regiao, ano, descricao))
        connection.commit()

        return True, "Vinho criado com sucesso!"
    except sqlite3.Error as e:
        return False, f"Erro ao criar vinho: {e}"
    finally:
        connection.close()


def processar_compra(carrinho, user_id):
    """
    Processa a compra de itens no carrinho.

    Args:
        carrinho (list): Lista de dicionários representando os itens no carrinho.
        user_id (int): ID do utilizador que está efetuando a compra.

    Returns:
        str: Mensagem indicando o sucesso ou falha da operação.
    """
    if not carrinho:
        return "O carrinho está vazio."

    connection = sqlite3.connect("data/database.db")
    cursor = connection.cursor()

    try:
        for item in carrinho:
            vinho_id = item['id']
            quantidade = 1
            data = datetime.now().strftime('%Y-%m-%d')

            cursor.execute('''
                INSERT INTO Vendas (user_id, vinho_id, data, quantidade)
                VALUES (?, ?, ?, ?)
            ''', (user_id, vinho_id, data, quantidade))
        
        connection.commit()
        return "Compra realizada com sucesso!"
    except Exception as e:
        return f"Erro ao processar a compra: {e}"
    finally:
        connection.close()


def inserir_vinhos_exemplo():
    """
    Insere vinhos de exemplo na tabela `Vinhos`.

    Returns:
        None
    """
    connection = sqlite3.connect("data/database.db")
    cursor = connection.cursor()

    vinhos = [
        ("Vinho Tinto Premium", 15.99, "Douro", 2020, "Um vinho tinto encorpado e com sabor intenso."),
        ("Vinho Branco Clássico", 12.50, "Alentejo", 2021, "Vinho branco refrescante, ideal para dias quentes."),
        ("Espumante Brut Reserva", 18.00, "Bairrada", 2019, "Espumante seco com aromas frutados e ótima acidez."),
        ("Vinho Rosé Suave", 10.50, "Tejo", 2022, "Rosé suave com toques de frutas vermelhas."),
        ("Vinho Verde Fresco", 8.99, "Minho", 2021, "Vinho verde leve e refrescante."),
        ("Reserva Especial Tinto", 25.00, "Douro", 2018, "Tinto encorpado com aromas de especiarias e frutas negras.")
    ]

    cursor.executemany(
        "INSERT INTO Vinhos (marca, preco, regiao, ano, descricao) VALUES (?, ?, ?, ?, ?)", 
        vinhos
    )
    connection.commit()
    connection.close()


def procurar_vinho_por_id(vinho_id):
    """
    Procura os dados de um vinho pelo ID.

    Args:
        vinho_id (int): ID do vinho a ser procurado.

    Returns:
        tuple: Um par (bool, dict ou str).
            - bool: True se o vinho for encontrado, False caso contrário.
            - dict: Dados do vinho se encontrado.
            - str: Mensagem de erro se o vinho não for encontrado.
    """
    try:
        connection = sqlite3.connect("data/database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id, marca, preco, regiao, ano, descricao FROM Vinhos WHERE id = ?", (vinho_id,))
        row = cursor.fetchone()

        if row:
            vinho = {
                "id": row[0],
                "marca": row[1],
                "preco": row[2],
                "regiao": row[3],
                "ano": row[4],
                "descricao": row[5],
            }
            return True, vinho
        else:
            return False, "Vinho não encontrado."
    except sqlite3.Error as e:
        return False, f"Erro ao procurar vinho: {e}"
    finally:
        connection.close()


if __name__ == "__main__":
    inserir_vinhos_exemplo()
    print("Amostra de vinhos inserida com sucesso!")
