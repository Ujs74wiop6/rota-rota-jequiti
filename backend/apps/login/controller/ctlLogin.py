import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from flask import Blueprint, jsonify, request

from apps.login.model.mdLogin import buscar_usuario

dp_login = Blueprint("login", __name__)


@dp_login.route("/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True) or {}
    login = dados.get("login")
    senha = dados.get("senha")

    if not login or not senha:
        return jsonify({"erro": "Informe login e senha!"}), 400

    usuario = buscar_usuario(login)
    if usuario is None:
        return jsonify({"erro": "Login ou senha inválidos!"}), 401

    if not bcrypt.checkpw(senha.encode("utf-8"), usuario["senha"].encode("utf-8")):
        return jsonify({"erro": "Login ou senha inválidos!"}), 401

    token = jwt.encode(
        {
            "sub": str(usuario["usuarioid"]),
            "login": usuario["login"],
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        },
        os.environ["JWT_SECRET"],
        algorithm="HS256",
    )
    return jsonify({"token": token, "usuario": usuario["login"]})