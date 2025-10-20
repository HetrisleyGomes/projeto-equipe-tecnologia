from flask import render_template, url_for, request, redirect, Blueprint, jsonify, send_file, g
import json
import csv
import pandas as pd
from io import StringIO, BytesIO
import psycopg2

from routes import get_db_connection

from src.models.repositories.requisicoes_repository import RequisicoesRepository
from src.controllers.requisicao_controller import RequisicaoController

from src.models.settings.db_connection_handler import db_connection_handler
from src.main.server.server import (
    socketio,
    app
)  # Importa socketio do módulo de configuração



rest_bp = Blueprint("rest_bp",__name__)

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