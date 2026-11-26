import os
from functools import wraps

import jwt
from flask import jsonify, request

def token_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        cabecalho = request.headers.get("Authorization", "")
        if not cabecalho.startswith("Bearer "):
            return jsonify({"erro": "Token de autenticação ausente ou inválido!"}), 401
        
        token = cabecalho.split(" ", 1)[1]
        try:
            jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado ou inválido!"}), 401
        
        return f(*args, **kwargs)
    return wrapped