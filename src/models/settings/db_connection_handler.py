import os
import sqlite3
from sqlite3 import Connection


class DbConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = os.getenv("DATABASE_URL")
        self.__conn = None
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            print(f"DATABASE_URL carregado: {database_url}")
        else:
            print("DATABASE_URL NÃO foi carregado.")

    def connect(self) -> None:
        conn = sqlite3.connect(self.__connection_string, check_same_thread=False)
        self.__conn = conn

    def get_connection(self) -> Connection:
        return self.__conn


db_connection_handler = DbConnectionHandler()
