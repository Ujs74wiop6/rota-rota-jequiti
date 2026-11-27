from datetime import date, datetime

from flask import Blueprint, jsonify, request

from auth import token_obrigatorio
from apps.animal.model import mdAnimal

bp_animal = Blueprint("animal", __name__)


def validar(dados):
    nome = (dados.get("nome") or "").strip()
    datanasc = dados.get("datanasc")

    if not nome:
        return None, "Informe o nome."
    if not datanasc:
        return None, "Informe a data de nascimento."

    try:
        data = datetime.strptime(datanasc, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None, "Data de nascimento inválida. Use AAAA-MM-DD."

    if data > date.today():
        return None, "A data de nascimento não pode ser futura."

    return (nome, datanasc), None


@bp_animal.get("/animal")
@token_obrigatorio
def get_all():
    return jsonify(mdAnimal.listar())


@bp_animal.get("/animal/<int:animalid>")
@token_obrigatorio
def get_by_id(animalid):
    animal = mdAnimal.buscar(animalid)
    if animal is None:
        return jsonify({"erro": "Animal não encontrado."}), 404
    return jsonify(animal)


@bp_animal.post("/animal")
@token_obrigatorio
def insert():
    valores, erro = validar(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"erro": erro}), 400
    return jsonify(mdAnimal.inserir(*valores)), 201


@bp_animal.put("/animal/<int:animalid>")
@token_obrigatorio
def update(animalid):
    valores, erro = validar(request.get_json(silent=True) or {})
    if erro:
        return jsonify({"erro": erro}), 400
    animal = mdAnimal.atualizar(animalid, *valores)
    if animal is None:
        return jsonify({"erro": "Animal não encontrado."}), 404
    return jsonify(animal)


@bp_animal.delete("/animal/<int:animalid>")
@token_obrigatorio
def delete(animalid):
    if not mdAnimal.excluir(animalid):
        return jsonify({"erro": "Animal não encontrado."}), 404
    return jsonify({"mensagem": "Animal excluído."})