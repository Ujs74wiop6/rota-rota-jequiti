from datetime import datetime

from flask import Blueprint, jsonify, request

from auth import token_obrigatorio
from apps.alocado.model import mdAlocado
from apps.animal.model import mdAnimal
from apps.piquete.model import mdPiquete

bp_alocado = Blueprint("alocado", __name__)


def validar(dados):
    animalidifk = dados.get("animalidifk")
    piqueteidfk = dados.get("piqueteidfk")
    datainicio = dados.get("datainicio")
    datafinal = dados.get("datafinal")

    if not isinstance(animalidifk, int):
        return None, "Informe o animal."
    if mdAnimal.buscar(animalidifk) is None:
        return None, "O animal informado não existe."

    if not isinstance(piqueteidfk, int):
        return None, "Informe o piquete."
    if mdPiquete.buscar(piqueteidfk) is None:
        return None, "O piquete informado não existe."

    if not datainicio:
        return None, "Informe a data de início."
    try:
        inicio = datetime.strptime(datainicio, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None, "Data de início inválida. Use AAAA-MM-DD."

    if datafinal:
        try:
            final = datetime.strptime(datafinal, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None, "Data final inválida. Use AAAA-MM-DD."
        if final < inicio:
            return None, "A data final não pode ser anterior à data de início."
    else:
        datafinal = None

    return (animalidifk, piqueteidfk, datainicio, datafinal), None


@bp_alocado.get("/alocado")
@token_obrigatorio
def get_all():
    return jsonify(mdAlocado.listar())


@bp_alocado.get("/alocado/<int:alocadoid>")
@token_obrigatorio
def get_by_id(alocadoid):
    alocado = mdAlocado.buscar(alocadoid)
    if alocado is None:
        return jsonify({"erro": "Alocação não encontrada."}), 404
    return jsonify(alocado)


@bp_alocado.post("/alocado")
@token_obrigatorio
def insert():
    valores, erro = validar(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(mdAlocado.inserir(*valores)), 201


@bp_alocado.put("/alocado/<int:alocadoid>")
@token_obrigatorio
def update(alocadoid):
    valores, erro = validar(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"erro": erro}), 400
    alocado = mdAlocado.atualizar(alocadoid, *valores)
    if alocado is None:
        return jsonify({"erro": "Alocação não encontrada."}), 404
    return jsonify(alocado)


@bp_alocado.delete("/alocado/<int:alocadoid>")
@token_obrigatorio
def delete(alocadoid):
    if not mdAlocado.excluir(alocadoid):
        return jsonify({"erro": "Alocação não encontrada."}), 404
    return jsonify({"mensagem": "Alocação excluída."})