from flask import render_template, url_for, request, redirect, Blueprint, jsonify, send_file, g
import psycopg2

from src.models.repositories.requisicoes_repository import RequisicoesRepository
from src.controllers.requisicao_controller import RequisicaoController

from src.models.settings.db_connection_handler import db_connection_handler
from src.main.server.server import (
    socketio,
    app
)  # Importa socketio do módulo de configuração



rest_bp = Blueprint("rest_bp",__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    if 'db_conn' not in g:
        try:
            conn_string = db_connection_handler.get_connection_string()
            g.db_conn = psycopg2.connect(conn_string)
            print("Conexão ao banco PostgreSQL estabelecida para a requisição.")
        except Exception as e:
            print(f"Erro ao conectar no banco: {e}")
            g.db_conn = None
    return g.db_conn

# Função para fechar a conexão no final de cada requisição
@app.teardown_appcontext
def close_db_connection(e=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()
        print("Conexão com o banco fechada.")

@rest_bp.route("/get", methods=["GET"])
def get_all():
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = RequisicoesRepository(connection)
    controller = RequisicaoController(repository)
    data = controller.get_all()

    return data

@rest_bp.route("/get/<id>", methods=["GET"])
def find_registro(id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = RequisicoesRepository(connection)
    controller = RequisicaoController(repository)

    data = controller.get_one(id)
    return data