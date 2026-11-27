import os
from functools import wraps

import jwt
from flask import jsonify, request


def token_obrigatorio(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        cabecalho = request.headers.get("Authorization", "")
        if not cabecalho.startswith("Bearer "):
            return jsonify({"erro": "Token ausente."}), 401

        token = cabecalho.split(" ", 1)[1]
        try:
            jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido ou expirado."}), 401

        return f(*args, **kwargs)
    return wrapper