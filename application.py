from flask import Flask, jsonify
from src.session import Session, engine
from src.models.model import Base
from src.blueprints.ejercicio import ejercicios_blueprint
from src.errors.errors import ApiError
from flask_cors import CORS

application = Flask(__name__)
application.register_blueprint(ejercicios_blueprint)
CORS(application)
Base.metadata.create_all(engine)
## add comment
@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code
##
if __name__ == "__main__":
    application.run(host="0.0.0.0", port = 5000, debug = True)