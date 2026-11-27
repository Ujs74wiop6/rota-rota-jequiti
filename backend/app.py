from flask import Flask
from flask_cors import CORS

from apps.login.controller.ctlLogin import dp_login
from apps.pasto.controller.ctlPasto import bp_pasto
from apps.piquete.controller.ctlPiquete import bp_piquete
from apps.animal.controller.ctlAnimal import bp_animal
from apps.alocado.controller.ctlAlocado import bp_alocado

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"]) # Permitindo requisições do frontend

app.register_blueprint(dp_login)
app.register_blueprint(bp_pasto)
app.register_blueprint(bp_piquete)
app.register_blueprint(bp_animal)
app.register_blueprint(bp_alocado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)