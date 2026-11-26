from flask import Blueprint, jsonify, request

from auth import token_obrigatorio
from apps.pasto.model import mdPasto

bp_pasto = Blueprint("pasto", __name__)


def validar(dados):
    descricao = (dados.get("descricao") or "").strip()
    areatotal = dados.get("areatotal")
    if not descricao:
        return None, "Informe a descrição."
    if isinstance(areatotal, bool) or not isinstance(areatotal, (int, float)) or areatotal <= 0:
        return None, "A área total deve ser um número maior que zero."
    return (descricao, areatotal), None


@bp_pasto.get("/pasto")
@token_obrigatorio
def get_all():
    return jsonify(mdPasto.listar())


@bp_pasto.get("/pasto/<int:pastoid>")
@token_obrigatorio
def get_by_id(pastoid):
    pasto = mdPasto.buscar(pastoid)
    if pasto is None:
        return jsonify({"erro": "Pasto não encontrado."}), 404
    return jsonify(pasto)


@bp_pasto.post("/pasto")
@token_obrigatorio
def insert():
    valores, erro = validar(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(mdPasto.inserir(*valores)), 201


@bp_pasto.put("/pasto/<int:pastoid>")
@token_obrigatorio
def update(pastoid):
    valores, erro = validar(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"erro": erro}), 400
    pasto = mdPasto.atualizar(pastoid, *valores)
    if pasto is None:
        return jsonify({"erro": "Pasto não encontrado."}), 404
    return jsonify(pasto)


@bp_pasto.delete("/pasto/<int:pastoid>")
@token_obrigatorio
def delete(pastoid):
    if not mdPasto.excluir(pastoid):
        return jsonify({"erro": "Pasto não encontrado."}), 404
    return jsonify({"mensagem": "Pasto excluído."})