import uuid
import datetime
from typing import Dict


class RequisicaoController:
    def __init__(self, repository) -> None:
        self.__repository = repository

    def create(self, body) -> Dict:
        try:
            id = str(uuid.uuid4())
            data_atual = datetime.datetime.today().strftime("%d-%m-%Y")
            requisition_infos = {
                "id": id,
                "setor": body["setor"],
                "description": body["description"],
                "priority": 0,
                "status": "A analisar",
                "data_emissao": data_atual,
                "nome_requisitante": body["nome_requisitante"],
            }

            self.__repository.registry_requisition(requisition_infos)

            return {
                "body": {
                    "id": id,
                },
                "status": 200,
            }
        except Exception as e:
            return {"body": {"error": e}, "status": 400}

    def get_all(self) -> Dict:
        try:
            data = self.__repository.get_all_requisitions()

            return {"body": data, "status": 200}
        except Exception as e:
            return {"body": {"error": e}, "status": 400}

    def get_one(self, id) -> Dict:
        try:
            data = self.__repository.get_one_requisition(id)
            data_formatada = {
                "id": data[0],
                "setor": data[1],
                "description": data[2],
                "comments": data[3],
                "priority": data[4],
                "status": data[5],
                "data_emissao": data[6],
                "data_conclusao": data[7],
                "nome_requisitante": data[8],
            }
            return {"body": data_formatada, "status": 200}
        except Exception as e:
            return {"body": {"error": e}, "status": 400}

    def update_comments(self, id, comment) -> Dict:
        try:
            data = self.__repository.set_comments_requisition(id, comment)
            return {"body": data, "status": 200}
        except Exception as e:
            return {"body": {"error": e}, "status": 400}

    def update_infos(self, id, propriety, status) -> Dict:
        try:
            self.__repository.edit_requisition(id, propriety, status)
            data = id
            return {"body": data, "status": 200}
        except Exception as e:
            return {"body": {"error": e}, "status": 400}

    def finalizar(self, id) -> Dict:
        try:
            data_atual = datetime.datetime.today().strftime("%d-%m-%Y")
            self.__repository.finalizar_requisition(id, data_atual)
            data = id
            return {"body": data, "status": 200}
        except Exception as e:
            return {"body": {"error": e}, "status": 400}
