import sqlite3
import csv

def fetch_monthly_sales():
    """
    Busca as vendas mensais do banco de dados com informações detalhadas.

    A consulta SQL seleciona as vendas do mês atual, juntando informações 
    das tabelas `Users`, `Vinhos` e `Vendas`.

    Retorna:
        list: Uma lista de tuplas contendo os seguintes dados para cada venda:
            - ID da venda
            - ID do utilizador
            - Nome do utilizador
            - ID do vinho
            - Nome do vinho
            - Preço do vinho
            - Data da venda

        Retorna uma lista vazia se nenhuma venda for encontrada.
    """
    try:
        connection = sqlite3.connect("data/database.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT 
                Vendas.id AS id_venda,
                Vendas.user_id AS id_utilizador,
                Users.nome AS nome_utilizador,
                Vendas.vinho_id AS id_vinho,
                Vinhos.marca AS nome_vinho,
                Vinhos.preco AS preco_vinho,
                Vendas.data AS data_venda
            FROM Vendas
            JOIN Users ON Vendas.user_id = Users.id
            JOIN Vinhos ON Vendas.vinho_id = Vinhos.id
            WHERE strftime('%Y-%m', Vendas.data) = strftime('%Y-%m', 'now')
        """)
        sales = cursor.fetchall()
        return sales if sales else []
    except sqlite3.Error as e:
        print(f"Erro ao buscar vendas: {e}")
        return []
    finally:
        connection.close()

def export_sales_to_csv():
    """
    Exporta as vendas mensais detalhadas para um arquivo CSV.

    Gera um arquivo `sales_report.csv` contendo os seguintes campos:
        - ID Venda
        - ID Utilizador
        - Nome Utilizador
        - ID Vinho
        - Nome Vinho
        - Preço
        - Data

    Retorna:
        tuple: Um par contendo:
            - bool: True se a exportação foi bem-sucedida, False caso contrário.
            - str: Mensagem informando o status da operação.
    """
    sales = fetch_monthly_sales()
    if not sales:
        return False, "Nenhuma venda encontrada para exportar."

    try:
        with open("sales_report.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID Venda", "ID Utilizador", "Nome Utilizador", "ID Vinho", "Nome Vinho", "Preço", "Data"])
            writer.writerows(sales)

        return True, "Relatório exportado com sucesso para 'sales_report.csv'."
    except Exception as e:
        return False, f"Erro ao exportar relatório: {e}"
