import mysql.connector

def connect_to_database():
    # configurações da conexão
    config = {
        'user': 'root',
        'password': 'Its_Ssv@2025',
        'host': 'localhost',
        'database': 'teste'
    }

    # Estabelece a conexão
    connection = mysql.connector.connect(**config)

    # Cria um cursor para executar comandos SQL
    cursor = connection.cursor()

    # Executa uma consulta simples
    cursor.execute('SELECT * from exemplo')

    # Exibe os resultados
    for row in cursor.fetchall():
        print(row)    

    # Fecha a conexão
    cursor.close()
    connection.close()


if __name__ == '__main__':
    connect_to_database()