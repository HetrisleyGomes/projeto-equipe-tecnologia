from typing import Tuple, Dict, List
from psycopg2.extensions import connection as Connection
import json


class RequisicoesRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn

    def registry_requisition(self, requisition_infos) -> None:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
                INSERT INTO requisicoes
                (id, setor, description, priority, status, data_emissao, nome_requisitante)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                requisition_infos["id"],
                requisition_infos["setor"],
                requisition_infos["description"],
                requisition_infos["priority"],
                requisition_infos["status"],
                requisition_infos["data_emissao"],
                requisition_infos["nome_requisitante"],
            ),
        )
        self.__conn.commit()
        cursor.close()

    def get_all_requisitions(self) -> List[Tuple]:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
                SELECT * FROM requisicoes
            """
        )
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_one_requisition(self, id) -> Dict:
        cursor = self.__conn.cursor()
        cursor.execute(
            """
                SELECT * FROM requisicoes WHERE id = %s
            """,
            (id,),
        )
        data = cursor.fetchone()
        cursor.close()
        return data

    def set_comments_requisition(self, id, comment) -> List:
        cursor = self.__conn.cursor()

        # Recuperar a lista de comentários existente
        cursor.execute("SELECT comments FROM requisicoes WHERE id = %s", (id,))
        result = cursor.fetchone()
        if result:
            comentarios_json = result[0]
            if comentarios_json:
                # Tentar carregar o JSON
                try:
                    comentarios = json.loads(comentarios_json)
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON: {e}")
                    comentarios = (
                        []
                    )  # Inicializar como lista vazia se o JSON estiver corrompido
            else:
                comentarios = []
        else:
            comentarios = []

        # Adicionar o novo comentário à lista
        comentarios.append(comment)

        # Converter a lista de volta para JSON
        comentarios_json = json.dumps(comentarios)

        # Atualizar o registro com os comentários modificados
        cursor.execute(
            "UPDATE requisicoes SET comments = %s WHERE id = %s", (comentarios_json, id)
        )

        self.__conn.commit()
        cursor.close()
        return comentarios

    def edit_requisition(self, id, description, propriety, status) -> None:
        cursor = self.__conn.cursor()

        cursor.execute(
            "UPDATE requisicoes SET description = %s, priority = %s, status = %s WHERE id = %s",
            (   
                description,
                propriety,
                status,
                id,
            ),
        )

        self.__conn.commit()
        cursor.close()

    def finalizar_requisition(self, id, data_atual) -> None:
        cursor = self.__conn.cursor()

        cursor.execute(
            'UPDATE requisicoes SET data_conclusao = %s, status = "Finalizado" WHERE id = %s',
            (
                data_atual,
                id,
            ),
        )

        self.__conn.commit()
        cursor.close()

    def get_custom_query(self, query) -> List:
        cursor = self.__conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    
    def delete_request(self, id) -> None:
        cursor = self.__conn.cursor()

        cursor.execute(
            "DELETE FROM requisicoes WHERE id = %s",
            (id,)
        )

        self.__conn.commit()
        cursor.close()