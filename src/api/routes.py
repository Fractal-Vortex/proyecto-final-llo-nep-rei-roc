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

# Endpoints de las rutas --->

@api.route('/rutas', methods=['POST'])
def crear_ruta():
    data = request.get_json()
    try:
        nueva_ruta = Rutas(
            titulo=data['titulo'],
            detalles=data.get('detalles'),
            usuario_id=data.get('usuario_id'),
            category_id=data.get('category_id'),
            fecha_creada=data['fecha_creada'],
            fecha_inicio=data['fecha_inicio']
        )
        db.session.add(nueva_ruta)
        db.session.commit()
        return jsonify(nueva_ruta.serialize()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api.route('/rutas', methods=['GET'])
def obtener_rutas():
    rutas = Rutas.query.all()
    return jsonify([ruta.serialize() for ruta in rutas]), 200

@api.route('/rutas/<int:ruta_id>', methods=['GET'])
def obtener_ruta(ruta_id):
    ruta = Rutas.query.get(ruta_id)
    if not ruta:
        return jsonify({"error": "Ruta no encontrada"}), 404
    return jsonify(ruta.serialize()), 200

@api.route('/rutas/<int:ruta_id>', methods=['PUT'])
def actualizar_ruta(ruta_id):
    ruta = Rutas.query.get(ruta_id)
    if not ruta:
        return jsonify({"error": "Ruta no encontrada"}), 404
    data = request.get_json()
    try:
        ruta.titulo = data.get('titulo', ruta.titulo)
        ruta.detalles = data.get('detalles', ruta.detalles)
        ruta.usuario_id = data.get('usuario_id', ruta.usuario_id)
        ruta.category_id = data.get('category_id', ruta.category_id)
        ruta.fecha_creada = data.get('fecha_creada', ruta.fecha_creada)
        ruta.fecha_inicio = data.get('fecha_inicio', ruta.fecha_inicio)
        db.session.commit()
        return jsonify(ruta.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api.route('/rutas/<int:ruta_id>', methods=['DELETE'])
def eliminar_ruta(ruta_id):
    ruta = Rutas.query.get(ruta_id)
    if not ruta:
        return jsonify({"error": "Ruta no encontrada"}), 404
    try:
        db.session.delete(ruta)
        db.session.commit()
        return jsonify({"message": "Ruta eliminada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
