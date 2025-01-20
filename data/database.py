import sqlite3

def initialize_database():
    """
    Inicializa o banco de dados da aplicação, criando as tabelas necessárias.

    Cria as tabelas `Vinhos`, `Users` e `Vendas` se elas ainda não existirem,
    garantindo que a estrutura do banco esteja pronta para uso.

    Tabelas:
        - Vinhos: Armazena informações sobre os vinhos disponíveis.
        - Users: Armazena informações sobre os utilizadores.
        - Vendas: Armazena informações sobre as vendas realizadas.

    Estrutura das tabelas:
        - Vinhos:
            - id: Identificador único do vinho.
            - marca: Nome do vinho.
            - preco: Preço do vinho.
            - regiao: Região de origem do vinho.
            - ano: Ano de produção do vinho.
            - descricao: Descrição do vinho.
        - Users:
            - id: Identificador único do utilizador.
            - nome: Nome do utilizador.
            - email: Email único do utilizador.
            - password: Senha do utilizador.
            - morada1: Endereço principal do utilizador.
            - morada2: Endereço secundário do utilizador (opcional).
            - tipo: Tipo de utilizador (`utilizador` ou `admin`).
        - Vendas:
            - id: Identificador único da venda.
            - user_id: ID do utilizador que realizou a compra.
            - vinho_id: ID do vinho vendido.
            - data: Data da venda.
            - quantidade: Quantidade de vinhos vendidos.

    Returns:
        None
    """
    connection = sqlite3.connect("data/database.db")
    cursor = connection.cursor()

    # Criar tabela de vinhos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vinhos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT NOT NULL,
        preco REAL NOT NULL,
        regiao TEXT NOT NULL,
        ano INTEGER NOT NULL,
        descricao TEXT
    )
    ''')

    # Criar tabela de utilizadores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        morada1 TEXT NOT NULL,
        morada2 TEXT DEFAULT NULL,
        tipo TEXT NOT NULL DEFAULT 'utilizador'  -- Adiciona tipo com valor padrão 'utilizador'
    )
    ''')

    # Criar tabela de vendas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        vinho_id INTEGER NOT NULL,
        data DATE NOT NULL,
        quantidade INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (vinho_id) REFERENCES Vinhos(id)
    )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()
    print("Base de dados inicializada com sucesso!")
