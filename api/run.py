from flask import Flask
from loguru import logger
from .routes.get_loads import loads_bp


# Crear la app de Flask
app = Flask(__name__)

# Registrar los blueprints
app.register_blueprint(loads_bp, url_prefix='/loads')

logger.info('################ API Iniciada ################')

# Iniciar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)