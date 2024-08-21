from flask import render_template, url_for, request, redirect, Blueprint, jsonify
import json

from src.models.repositories.requisicoes_repository import RequisicoesRepository
from src.controllers.requisicao_controller import RequisicaoController

from src.models.settings.db_connection_handler import db_connection_handler
from src.main.server.server import socketio  # Importa socketio do módulo de configuração

main_bp = Blueprint('main_bp', __name__, template_folder='templates')

inverter_ordem = False
mostrar_prioridades = False
mostrar_finalizados = False

@main_bp.route("/")
@main_bp.route("/index")
def index():
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    data = controller.get_all()
    return render_template("index.html", data = data, inverter_ordem = inverter_ordem, mostrar_prioridades = mostrar_prioridades, mostrar_finalizados = mostrar_finalizados)

@main_bp.route("/registro")
def registrar():
    return render_template("registrar.html")

@main_bp.route("/registro/salvar", methods=['POST'])
def salvar_registro():
    setor = request.form.get("setor")
    description = request.form.get("description")
    nome_requisitante = request.form.get("nome_requisitante")
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    body ={
        "setor": setor,
        "description": description,
        "nome_requisitante": nome_requisitante
    }
    data = controller.create(body)
    socketio.emit('update')
    return redirect(url_for('main_bp.index'))


@main_bp.route("/ver/<id>")
def find_registro(id):
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)

    data = controller.get_one(id)
    comentarios = []
    try:
        comentarios = json.loads(data['body']['comments'])
    except Exception as e:
        print(e)
    
    return render_template('view.html', data = data, comentarios = comentarios)

@main_bp.route("/adicionar_comentario", methods=['POST'])
def adicionar_comentario():
    # Recebe os dados enviados via POST
    data = request.get_json()

    # Extrai o comentário e dados adicionais
    comment = data.get('comment')
    id = data.get('dados')

    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    response_data = controller.update_comments(id, comment)
    socket_data = {'comment': comment}
    socketio.emit('update', socket_data)
    return jsonify({'comment': comment})

@main_bp.route('/verificar_senha', methods=['POST'])
def verificar_senha():
    senha = request.form.get('senha')
    id = request.form.get('id')

    # Lógica para validar a senha (exemplo simples)
    if senha == '123':  # Substitua 'senha_correta' por sua senha real ou lógica de autenticação
        return jsonify({'redirect': url_for('main_bp.edit_registro', id=id)})
    else:
        return jsonify({'message': 'Senha incorreta!'})

@main_bp.route('/pagina-desejada')
def pagina_desejada():
    return 'Página desejada'

@main_bp.route("/gerenciar/<id>")
def edit_registro(id):
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)

    data = controller.get_one(id)
    comentarios = []
    try:
        comentarios = json.loads(data['body']['comments'])
    except Exception as e:
        print(e)
    
    return render_template('edit.html', data = data, comentarios = comentarios)


@main_bp.route("/edicao/salvar/<id>", methods=['POST'])
def edit_salvar_registro(id):
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)

    priority = request.form.get('priority')
    status = request.form.get('status')

    if priority == "1":
        if status == "A analisar":
            status = "Vizualizado"
    if status == "Finalizado":
        return redirect(url_for("main_bp.finalizar_registro", id=id))
    data = controller.update_infos(id, priority, status)
    socketio.emit('update_edit')
    return redirect(url_for("main_bp.find_registro", id=id))

@main_bp.route("/finalizar/<id>", methods=['GET','POST'])
def finalizar_registro(id):
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)

    data = controller.finalizar(id)
    data = controller.get_one(id)
    socketio.emit('update_edit')
    return redirect(url_for("main_bp.find_registro", id=id))

@main_bp.route('/atualizar_lista', methods=['GET'])
def atualizar_lista():
    repository = RequisicoesRepository(db_connection_handler.get_connection())
    controller = RequisicaoController(repository)
    data = controller.get_all()

    inverter_ordem = request.args.get('inverter_ordem', 'false') == 'true'
    mostrar_prioridades = request.args.get('mostrar_prioridades', 'false') == 'true'
    mostrar_finalizados = request.args.get('mostrar_finalizados', 'false') == 'true'

    # Filtrar dados com base no status
    filtered_data = [item for item in data['body'] if mostrar_finalizados or item[5] != 'Finalizado']
    
    # Filtrar dados com base na prioridade
    filtered_data = [item for item in filtered_data if not mostrar_prioridades or item[4] == 1]
    
    # Ordenar os dados filtrados
    sorted_data = filtered_data
    if inverter_ordem:
        sorted_data.reverse()

    return jsonify({'body': sorted_data})

# Defina suas rotas aqui
@main_bp.route('/update_request/<int:request_id>', methods=['POST'])
def update_request(request_id):
    # Código para atualizar a requisição no banco de dados
    data = {'request_id': request_id, 'new_data': 'updated'}
    socketio.emit('update', data, broadcast=True)
    return 'Update successful'