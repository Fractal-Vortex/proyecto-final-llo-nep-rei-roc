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

@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User {user.email} deleted successfully"}), 200

@api.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Users.query.get(user_id)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = data["password"]
    if "is_active" in data:
        user.is_active = data["is_active"]

    db.session.commit()

    return jsonify({
        "message": f"User {user.email} updated successfully",
        "user": user.serialize()
    }), 200


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