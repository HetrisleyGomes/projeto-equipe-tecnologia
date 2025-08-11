from flask import render_template, url_for, request, redirect, Blueprint, jsonify, send_file
import json
import csv
from io import StringIO, BytesIO

from src.models.repositories.requisicoes_repository import RequisicoesRepository
from src.controllers.requisicao_controller import RequisicaoController

from src.models.settings.db_connection_handler import db_connection_handler
from src.main.server.server import (
    socketio,
)  # Importa socketio do módulo de configuração

main_bp = Blueprint("main_bp", __name__, template_folder="templates")

inverter_ordem = False
mostrar_prioridades = True
mostrar_finalizados = False


@main_bp.route("/")
@main_bp.route("/index")
def index():
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    data = controller.get_all()
    return render_template(
        "index.html",
        data=data,
        inverter_ordem=inverter_ordem,
        mostrar_prioridades=mostrar_prioridades,
        mostrar_finalizados=mostrar_finalizados,
    )


@main_bp.route("/registro")
def registrar():
    return render_template("registrar.html")


@main_bp.route("/registro/salvar", methods=["POST"])
def salvar_registro():
    setor = request.form.get("setor")
    description = request.form.get("description")
    nome_requisitante = request.form.get("nome_requisitante")
    prioridade = request.form.get("prioridade")
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    body = {
        "setor": setor,
        "description": description,
        "nome_requisitante": nome_requisitante,
        "prioridade": prioridade,
    }
    data = controller.create(body)
    socketio.emit("update")
    return redirect(url_for("main_bp.index"))


@main_bp.route("/ver/<id>")
def find_registro(id):
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)

    data = controller.get_one(id)
    comentarios = []
    try:
        comentarios = json.loads(data["body"]["comments"])
    except Exception as e:
        print(e)

    return render_template("view.html", data=data, comentarios=comentarios)


@main_bp.route("/adicionar_comentario", methods=["POST"])
def adicionar_comentario():
    # Recebe os dados enviados via POST
    data = request.get_json()

    # Extrai o comentário e dados adicionais
    comment = data.get("comment")
    id = data.get("dados")

    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    response_data = controller.update_comments(id, comment)
    socket_data = {"comment": comment}
    socketio.emit("update", socket_data)
    return jsonify({"comment": comment})

@main_bp.route("/relatorio")
def relatorio():
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    data = controller.get_all()
    return render_template(
        "relatorio.html",
        data=data
    )

@main_bp.route('/download', methods=['GET'])
def download():
    # Aqui você pode aplicar os mesmos filtros da consulta que você aplicou na rota principal
    casos_encerrados = request.args.get('casos_encerrados', 'false') == 'true'
    casos_abertos = request.args.get('casos_abertos', 'false') == 'true'
    desse_mes = request.args.get('desse_mes', 'false') == 'true'

    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)

    query_args = [0, 0, 0]
    if casos_encerrados:
        query_args[0] = 1
    if casos_abertos:
        query_args[1] = 1
    if desse_mes:
        query_args[2] = 1

    dados = controller.get_by_query(query_args)

    # Gerar CSV
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(['Nome', 'Descrição', 'Comentários', 'Prioridade', 'Status', 'Data de Emissão', 'Data de Finalização', 'Requerente'])

    for row in dados['body']:
        writer.writerow([row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
    
    mem = BytesIO()
    mem.write(csv_buffer.getvalue().encode('utf-8'))
    mem.seek(0)

    return send_file(mem, as_attachment=True, download_name='relatorio_requisicoes.csv', mimetype='text/csv')


@main_bp.route("/gerenciar/<id>")
def edit_registro(id):
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)

    data = controller.get_one(id)
    comentarios = []
    try:
        comentarios = json.loads(data["body"]["comments"])
    except Exception as e:
        print(e)

    return render_template("edit.html", data=data, comentarios=comentarios)


@main_bp.route("/edicao/salvar/<id>", methods=["POST"])
def edit_salvar_registro(id):
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)

    description = request.form.get("description")
    priority = request.form.get("priority")
    status = request.form.get("status")

    if priority == "1":
        if status == "A analisar":
            status = "Vizualizado"

    data = controller.update_infos(id, description, priority, status)


    if status == "Finalizado":
        return redirect(url_for("main_bp.finalizar_registro", id=id))
    
    socketio.emit("update")
    return redirect(url_for("main_bp.find_registro", id=id))


@main_bp.route("/finalizar/<id>", methods=["GET", "POST"])
def finalizar_registro(id):
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)

    data = controller.finalizar(id)
    socketio.emit("update")
    return redirect(url_for("main_bp.index"))


@main_bp.route("/atualizar_lista", methods=["GET"])
def atualizar_lista():
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    data = controller.get_all()

    inverter_ordem = request.args.get("inverter_ordem", "false") == "true"
    mostrar_prioridades = request.args.get("mostrar_prioridades", "false") == "true"
    mostrar_finalizados = request.args.get("mostrar_finalizados", "false") == "true"

    # Filtrar dados com base no status
    filtered_data = [
        item for item in data["body"] if mostrar_finalizados or item['status'] != "Finalizado"
    ]

    # Filtrar dados com base na prioridade, ordena com prioridade 1 primeiro
    if mostrar_prioridades:
        filtered_data.sort(key=lambda x: 0 if x['priority'] == 1 else 1)

    # Ordenar os dados filtrados
    sorted_data = filtered_data
    if inverter_ordem:
        sorted_data.reverse()

    return jsonify({"body": sorted_data})

@main_bp.route("/delete/<id>", methods=["GET"])
def delete_registro(id):
    print(f"Tentando deletar ID: {id}")
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    controller.delete_by_id(id)
    socketio.emit("update")
    return redirect(url_for("main_bp.index"))

@main_bp.route("/update_request/<int:request_id>", methods=["POST"])
def update_request(request_id):
    # Código para atualizar a requisição no banco de dados
    data = {"request_id": request_id, "new_data": "updated"}
    socketio.emit("update", data)
    return "Update successful"