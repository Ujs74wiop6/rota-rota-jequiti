from flask import Blueprint, jsonify, request

from auth import token_obrigatorio
from apps.pasto.model import mdPasto
from apps.piquete.model import mdPiquete

bp_piquete = Blueprint("piquete", __name__)


def eh_numero(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validar(dados):
    descricao = (dados.get("descricao") or "").strip()
    latitude = dados.get("latitude")
    longitude = dados.get("longitude")
    pastoidfk = dados.get("pastoidfk")

    if not descricao:
        return None, "Informe a descrição."
    if not eh_numero(latitude) or not -90 <= latitude <= 90:
        return None, "A latitude deve ser um número entre -90 e 90."
    if not eh_numero(longitude) or not -180 <= longitude <= 180:
        return None, "A longitude deve ser um número entre -180 e 180."
    if not isinstance(pastoidfk, int) or isinstance(pastoidfk, bool):
        return None, "Informe o pasto."
    if mdPasto.buscar(pastoidfk) is None:
        return None, "O pasto informado não existe."
    return (descricao, latitude, longitude, pastoidfk), None


@bp_piquete.get("/piquete")
@token_obrigatorio
def get_all():
    return jsonify(mdPiquete.listar())


@bp_piquete.get("/piquete/<int:piqueteid>")
@token_obrigatorio
def get_by_id(piqueteid):
    piquete = mdPiquete.buscar(piqueteid)
    if piquete is None:
        return jsonify({"erro": "Piquete não encontrado."}), 404
    return jsonify(piquete)


@bp_piquete.post("/piquete")
@token_obrigatorio
def insert():
    valores, erro = validar(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(mdPiquete.inserir(*valores)), 201


@bp_piquete.put("/piquete/<int:piqueteid>")
@token_obrigatorio
def update(piqueteid):
    valores, erro = validar(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"erro": erro}), 400
    piquete = mdPiquete.atualizar(piqueteid, *valores)
    if piquete is None:
        return jsonify({"erro": "Piquete não encontrado."}), 404
    return jsonify(piquete)


@bp_piquete.delete("/piquete/<int:piqueteid>")
@token_obrigatorio
def delete(piqueteid):
    if not mdPiquete.excluir(piqueteid):
        return jsonify({"erro": "Piquete não encontrado."}), 404
    return jsonify({"mensagem": "Piquete excluído."})