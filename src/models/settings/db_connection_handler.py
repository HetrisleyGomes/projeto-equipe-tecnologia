import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection as Connection

load_dotenv()

class DbConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = os.getenv("DATABASE_URL")
        self.__conn = None

        if self.__connection_string:
            print("DATABASE_URL carregado.")
        else:
            print("DATABASE_URL NÃO foi carregado.")

    def connect(self) -> None:
        try:
            # Aqui conectamos ao PostgreSQL com psycopg2
            self.__conn = psycopg2.connect(self.__connection_string)
            print("Conexão ao banco PostgreSQL estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar no banco: {e}")
            self.__conn = None

    def get_connection(self) -> Connection:
        return self.__conn


db_connection_handler = DbConnectionHandler()
