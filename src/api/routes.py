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
    try:
        events = Eventos.query.all()
        events_serialized = [event.serialize() for event in events]
        return jsonify({
            "msg": "Eventos obtenidos correctamente", 
            "payload": events_serialized
        }), 200
    except Exception as e:
        return jsonify({
            "msg": "Error al obtener eventos",
            "error": str(e)
        }), 500

# Obtener un evento por ID
@api.route('/eventos/<int:id>', methods=['GET'])
def get_event(id):
    try:
        event = Eventos.query.get(id)
        if not event:
            return jsonify({
                "msg": "Evento no encontrado"
                }), 404
        return jsonify({
            "msg": "Evento obtenido correctamente", 
            "payload": event.serialize()
            }), 200
    except Exception as e:
        return jsonify({
            "msg": "Error al obtener el evento",
            "error": str(e)
        }), 500
    
# Crear un evento
@api.route('/eventos', methods=['POST'])
def add_event():
    try:
        data = request.get_json()
        
        titulo = data.get("titulo")
        detalles = data.get("detalles")
        tipo = data.get("tipo")
        fecha = data.get("fecha")
        category_id = data.get("category_id")
        rutas_id = data.get("rutas_id")

        if not all([titulo, detalles, tipo, fecha, category_id, rutas_id]):
            return jsonify({"msg": "Faltan campos obligatorios"}), 400

        new_event = Eventos(
            titulo=titulo, 
            detalles=data.get("detalles"), 
            tipo=tipo, 
            fecha=fecha, 
            category_id=category_id, 
            rutas_id=rutas_id
        )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({
            "msg": "Evento creado correctamente",
            "payload": new_event.serialize()
        }), 201

    except Exception as e:
        return jsonify({
            "msg": "Error al crear el evento", 
            "error": str(e)
        }), 500

# Eliminar un evento
@api.route('/eventos/<int:id>', methods=['DELETE'])
def delete_event(id):
    try:
        event = Eventos.query.get(id)
        if not event:
            return jsonify({"msg": "Evento no encontrado"}), 404

        db.session.delete(event)
        db.session.commit()

        return jsonify({"msg": "Evento eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({
            "msg": "Error al eliminar el evento", 
            "error": str(e)
        }), 500

# Editar un evento
@api.route('/eventos/<int:id>', methods=['PUT'])
def update_event(id):
    try:
        data = request.get_json()

        event = Eventos.query.get(id)
        if not event:
            return jsonify({"msg": "Evento no encontrado"}), 404
        
        event.titulo = data.get("titulo", event.titulo)
        event.detalles = data.get("detalles", event.detalles)
        event.tipo = data.get("tipo", event.tipo)
        event.fecha = data.get("fecha", event.fecha)
        event.category_id = data.get("category_id", event.category_id)
        event.rutas_id = data.get("rutas_id", event.rutas_id)

        db.session.commit()

        return jsonify({
            "msg": "Evento actualizado correctamente",
            "payload": event.serialize()
        }), 200

    except Exception as e:
        return jsonify({
            "msg": "Error al actualizar el evento", 
            "error": str(e)
        }), 500

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

