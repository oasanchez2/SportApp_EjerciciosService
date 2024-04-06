from flask import Flask, jsonify, request, Blueprint
from ..commands.create_exercise import CreateExercises
from ..commands.get_exercise import GetExercise
from ..commands.reset import Reset

ejercicios_blueprint = Blueprint('ejercicios', __name__)

@ejercicios_blueprint.route('/ejercicios', methods = ['POST'])
def create():
    user = CreateExercises(request.get_json()).execute()
    return jsonify(user), 201

@ejercicios_blueprint.route('/ejercicios/<id>', methods = ['GET'])
def show(id):
    """ Authenticate(auth_token()).execute() """
    ejercicio = GetExercise(id).execute() 
    return jsonify(ejercicio)

@ejercicios_blueprint.route('/', methods = ['GET'])
def ping():
    return 'pong'

@ejercicios_blueprint.route('/ejercicios/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization