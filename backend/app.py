from flask import Flask, jsonify
from flask_cors import CORS
from db import get_conexao
from apps.login.controller.ctlLogin import dp_login
from apps.pasto.controller.ctlPasto import dp_pasto

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"]) # Permitindo requisições do frontend

app.register_blueprint(dp_login)
app.register_blueprint(dp_pasto)

@app.route("/saude")
def saude():
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as total FROM usuario")
    total = cur.fetchone()["total"]
    conn.close()
    return jsonify({"status": "ok", "total_usuarios": total})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)