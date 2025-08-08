import os
import psycopg2
from psycopg2.extensions import connection as Connection

class DbConnectionHandler:
    def __init__(self) -> None:
        # Pega a string de conexão do ambiente (Render → Environment Variable)
        self.__connection_string = os.getenv("DATABASE_URL")
        self.__conn = None

    def connect(self) -> None:
        try:
            self.__conn = psycopg2.connect(self.__connection_string)
        except Exception as e:
            print(f"Erro ao conectar no PostgreSQL: {e}")

    def get_connection(self) -> Connection:
        return self.__conn


db_connection_handler = DbConnectionHandler()