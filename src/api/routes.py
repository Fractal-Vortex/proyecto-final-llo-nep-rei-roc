"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, Rutas, Categorias, Eventos, Rutas_eventos, Favorites
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# Obtener todos los eventos
@api.route('/eventos', methods=['GET'])
def get_all_events():
    data = Eventos.query.all()
    data = [user.serialize() for user in data]
    return jsonify({"msg": "Eventos obtenidos correctamente" , "payload": data})

# Obtener un evento
@api.route('/eventos/<int:id>', methods=['GET'])
def get_event(id):
    data = Eventos.query.get(id)
    if not data:
        return jsonify({"msg": "Eventono encontrado"}), 404
    return jsonify({"msg": "Evento obtenido correctamente", "payload": data.serialize()})

# Crear un evento
# Editar un evento
# Eliminar un evento

