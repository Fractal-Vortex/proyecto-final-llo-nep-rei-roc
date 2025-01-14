"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Blueprint, request, jsonify, url_for
from api.models import db, Users, Rutas, Categorias, Eventos, Rutas_eventos, Favorites, Comentarios, Valoraciones
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
import re

api = Blueprint('api', __name__)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
MSG_MISSING_DATA = "Todos los datos son necesarios"
MSG_INVALID_DATA = "Datos inválidos"
MSG_EMAIL_EXISTS = "El correo ya existe!"
MSG_SUCCESS = "Usuario registrado exitosamente"

# Allow CORS requests to this API
CORS(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


# Endpoint para registrar un nuevo usuario.
@api.route('/register', methods=['POST'])
def register():
    """
    Endpoint para registrar un nuevo usuario.
    Recibe un JSON con 'user', 'email' y 'password'.
    Retorna un token JWT si el registro es exitoso.
    """
    user = request.json.get('user', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not user or not email or not password:
        return jsonify({"msg": MSG_MISSING_DATA}), 400

    if not isinstance(user, str) or not isinstance(email, str) or not isinstance(password, str) or not EMAIL_REGEX.match(email):
        return jsonify({"msg": MSG_INVALID_DATA}), 400

    exists = Users.query.filter_by(email=email).first()
    if exists:
        return jsonify({"msg": MSG_EMAIL_EXISTS}), 409

    try:
        hashed_password = generate_password_hash(password)
        new_user = Users(
            user=user,  # Ahora se maneja el campo 'user'
            email=email,
            password=hashed_password,
            is_active=True
        )
        db.session.add(new_user)
        db.session.commit()

        token = create_access_token(identity=str(new_user.id))
        return jsonify({"msg": MSG_SUCCESS, "token": token}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500


# Endpoint para obtener todos los usuarios de la base de datos.
@api.route('/users', methods=['GET'])
def get_users():
    """
    Endpoint para obtener todos los usuarios.
    Retorna una lista de usuarios serializados en formato JSON.
    Ejemplo de respuesta:
    {
        "msg": "Usuarios obtenidos correctamente",
        "payload": [
            {
                "id": 1,
                "user": "user1",
                "email": "user1@example.com"
            },
            ...
        ]
    }
    """
    try:
        # Obtener todos los usuarios de la base de datos
        users = Users.query.all()
        
        # Si no hay usuarios, retornar un mensaje adecuado
        if not users:
            return jsonify({"msg": "No users found"}), 404

        # Serializar los usuarios y devolverlos
        users_serialized = [user.serialize() for user in users]
        return jsonify({
            "msg": "Usuarios obtenidos correctamente",
            "payload": users_serialized
        }), 200

    except SQLAlchemyError as e:
        # Manejo de errores específicos de la base de datos
        return jsonify({
            "msg": "Error al obtener los usuarios",
            "error": f"Database query failed: {str(e)}"
        }), 500
    except Exception as e:
        # Manejo de errores generales
        return jsonify({
            "msg": "Unexpected error",
            "error": str(e)
        }), 500

# Endpoint para obtener usuario por id.
@api.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Endpoint para obtener un solo usuario por su ID.
    Retorna el usuario serializado.
    """
    try:
        # Obtener el usuario por ID
        user = Users.query.get(user_id)
        
         # Si no hay usuarios, retornar un mensaje adecuado
        if not user:
            return jsonify({"msg": "User not found"}), 404

        # Serializar el usuario y devolverlo
        return jsonify({
            "msg": "Usuario obtenido correctamente",
            "payload": user.serialize()
        }), 200

    except SQLAlchemyError as e:
        # Manejo de errores específicos de la base de datos
        return jsonify({
            "msg": "Error al obtener el usuario",
            "error": f"Database query failed: {str(e)}"
        }), 500
    except Exception as e:
        # Manejo de errores generales
        return jsonify({
            "msg": "Unexpected error",
            "error": str(e)
        }), 500
    
# Endpoint para obtener usuario por usuario o email.
@api.route('/users/search', methods=['GET'])
def search_user():
    """
    Endpoint para buscar un usuario por nombre de usuario o correo electrónico.
    Recibe parámetros de consulta 'user' o 'email'.
    """
    # Obtener el usuario por nombre de usuario o email
    user = request.args.get('user', None)
    email = request.args.get('email', None)

    # Si no hay parámetros de búsqueda, retorna mensaje
    if not user and not email:
        return jsonify({"msg": "Debe proporcionar un nombre de usuario o un correo electrónico para la búsqueda."}), 400

    try:
        if user:
            user_found = Users.query.filter_by(user=user).first()
        elif email:
            user_found = Users.query.filter_by(email=email).first()

        if user_found:
            return jsonify({
                "msg": "Usuario encontrado",
                "payload": user_found.serialize()
            }), 200
        else:
            return jsonify({"msg": "Usuario no encontrado"}), 404

    except SQLAlchemyError as e:
        # Manejo de errores específicos de la base de datos
        return jsonify({
            "msg": "Error al buscar el usuario",
            "error": f"Database query failed: {str(e)}"
        }), 500
    except Exception as e:
        # Manejo de errores generales
        return jsonify({
            "msg": "Unexpected error",
            "error": str(e)
        }), 500


# Endpoint para editar los datos de usuario.
@api.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Endpoint para actualizar los datos de un usuario existente.
    """
    # Buscar el usuario en la base de datos por su ID
    user = Users.query.get(user_id)
    
    if user is None:
        # Retornar error si el usuario no existe
        return jsonify({"error": "User not found"}), 404

    # Obtener los datos enviados en el cuerpo de la solicitud
    data = request.get_json()

    if not data:
        # Retornar error si no se envían datos
        return jsonify({"error": "No data provided"}), 400

    # Validar y actualizar el correo electrónico si está presente
    if "email" in data:
        if not EMAIL_REGEX.match(data["email"]):
            # Retornar error si el formato del correo es inválido
            return jsonify({"error": "Invalid email format"}), 400
        user.email = data["email"]

    # Validar y actualizar la contraseña si está presente
    if "password" in data:
        if not isinstance(data["password"], str) or len(data["password"]) < 8:
            # Retornar error si la contraseña no cumple con los requisitos mínimos
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        user.password = generate_password_hash(data["password"])  # Hashear la nueva contraseña

    # Validar y actualizar el estado de actividad si está presente
    if "is_active" in data:
        if not isinstance(data["is_active"], bool):
            # Retornar error si el valor de 'is_active' no es un booleano
            return jsonify({"error": "Invalid value for 'is_active'. Must be a boolean"}), 400
        user.is_active = data["is_active"]

    # Guardar los cambios en la base de datos
    try:
        db.session.commit()
        # Retornar mensaje de éxito con los datos actualizados del usuario
        return jsonify({
            "message": f"User {user.email} updated successfully",
            "user": user.serialize()
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores relacionados con la base de datos
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "details": str(e)
        }), 500
    except Exception as e:
        # Manejo de errores generales no previstos
        db.session.rollback()
        return jsonify({
            "error": "Unexpected error",
            "details": str(e)
        }), 500

# Endpoint para eliminar usuario por id.
@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Endpoint para eliminar un usuario por su ID.
    """
    try:
        # Obtener el usuario por ID
        user = Users.query.get(user_id)
        
        # Si no se encuentra el usuario, retornar un mensaje adecuado
        if not user:
            return jsonify({"msg": "User not found"}), 404

        # Eliminar el usuario
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            "msg": f"User {user_id} deleted successfully"
        }), 200

    except SQLAlchemyError as e:
        # Manejo de errores específicos de la base de datos
        db.session.rollback()
        return jsonify({
            "msg": "Error al eliminar el usuario",
            "error": f"Database query failed: {str(e)}"
        }), 500
    except Exception as e:
        # Manejo de errores generales
        db.session.rollback()
        return jsonify({
            "msg": "Unexpected error",
            "error": str(e)
        }), 500


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

@api.route('/categorias', methods=['POST'])
def create_categoria():
    categoria = request.json.get('categoria', None)

    if not categoria:
        return jsonify({"msg": "El campo 'categoria' es obligatorio"}), 400

    if Categorias.query.filter_by(categoria=categoria).first():
        return jsonify({"msg": "La categoría ya existe"}), 400

    try:
        nueva_categoria = Categorias(categoria=categoria)
        db.session.add(nueva_categoria)
        db.session.commit()
        return jsonify(nueva_categoria.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500


@api.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        categorias = Categorias.query.all()
        return jsonify([categoria.serialize() for categoria in categorias]), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@api.route('/categorias/<int:categoria_id>', methods=['GET'])
def get_categoria_by_id(categoria_id):
    categoria = Categorias.query.get(categoria_id)
    if not categoria:
        return jsonify({"msg": "Categoría no encontrada"}), 404
    return jsonify(categoria.serialize()), 200

@api.route('/categorias/<int:categoria_id>', methods=['PUT'])
def update_categoria(categoria_id):
    categoria = Categorias.query.get(categoria_id)
    if not categoria:
        return jsonify({"msg": "Categoría no encontrada"}), 404

    nuevo_nombre = request.json.get('categoria', None)

    if not nuevo_nombre:
        return jsonify({"msg": "El campo 'categoria' es obligatorio"}), 400

    if Categorias.query.filter(Categorias.categoria == nuevo_nombre, Categorias.id != categoria_id).first():
        return jsonify({"msg": "La nueva categoría ya existe"}), 400

    try:
        categoria.categoria = nuevo_nombre
        db.session.commit()
        return jsonify(categoria.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500
    
@api.route('/categorias/<int:categoria_id>', methods=['DELETE'])
def delete_categoria(categoria_id):
    categoria = Categorias.query.get(categoria_id)
    if not categoria:
        return jsonify({"msg": "Categoría no encontrada"}), 404

    try:
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({"msg": "Categoría eliminada"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

# Endpoint para añadir ruta o evento a favoritos
@api.route('/favorites', methods=['POST'])
def add_to_favorites():
    data = request.json

    user_id = data.get('user_id')
    rutas_id = data.get('rutas_id')
    eventos_id = data.get('eventos_id')

    # Validar entrada
    if not user_id or (not rutas_id and not eventos_id):
        return jsonify({"error": "user_id y al menos uno de rutas_id o eventos_id son requeridos"}), 400

    # Crear favorito
    favorito = Favorites(user_id=user_id, rutas_id=rutas_id, eventos_id=eventos_id)
    db.session.add(favorito)
    db.session.commit()

    return jsonify(favorito.serialize()), 201


# Endpoint para obtener todos los favoritos de un usuario
@api.route('/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    favoritos = Favorites.query.filter_by(user_id=user_id).all()

    if not favoritos:
        return jsonify({"error": "No se encontraron favoritos para este usuario"}), 404

    return jsonify([favorito.serialize() for favorito in favoritos]), 200


# Endpoint para eliminar un favorito
@api.route('/favorites/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    favorito = Favorites.query.get(id)

    if not favorito:
        return jsonify({"error": "El favorito no existe"}), 404

    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"message": f"Favorito con ID {id} eliminado exitosamente"}), 200

@api.route('/comentarios', methods=['POST'])
def crear_comentario():
    """
    Permitir que un usuario cree un comentario sobre una ruta o evento.
    """
    data = request.get_json()

    if not data or 'comentario' not in data or 'tipo' not in data or 'to_id' not in data or 'from_id' not in data:
        return jsonify({"error": "Datos insuficientes. Se requieren 'comentario', 'tipo', 'to_id' y 'from_id'."}), 400

    if data['tipo'] not in ['ruta', 'evento']:
        return jsonify({"error": "El tipo debe ser 'ruta' o 'evento'."}), 400

    nuevo_comentario = Comentarios(
        comentario=data['comentario'],
        tipo=data['tipo'],
        to_id=data['to_id'],
        from_id=data['from_id']
    )

    db.session.add(nuevo_comentario)
    db.session.commit()

    return jsonify(nuevo_comentario.serialize()), 201


@api.route('/comentarios/<int:id>', methods=['GET'])
def obtener_comentarios(id):
    """
    Recuperar comentarios de una ruta o evento específico.
    """
    # Validar si es ruta o evento
    tipo = request.args.get('tipo')
    if not tipo or tipo not in ['ruta', 'evento']:
        return jsonify({"error": "Debe especificar el tipo como 'ruta' o 'evento'."}), 400

    # Filtrar comentarios según el tipo y el ID
    comentarios = Comentarios.query.filter_by(tipo=tipo, to_id=id).all()

    if not comentarios:
        return jsonify({"message": f"No se encontraron comentarios para el {tipo} con ID {id}."}), 404

    return jsonify([comentario.serialize() for comentario in comentarios]), 200


@api.route('/comentarios/<int:id>', methods=['DELETE'])
def eliminar_comentario(id):
    """
    Eliminar un comentario.
    """
    comentario = Comentarios.query.get(id)

    if not comentario:
        return jsonify({"error": f"No se encontró ningún comentario con ID {id}."}), 404

    db.session.delete(comentario)
    db.session.commit()

    return jsonify({"message": f"Comentario con ID {id} eliminado exitosamente."}), 200

@api.route('/valoraciones', methods=['POST'])
def añadir_valoracion():
    """
    Permitir añadir una valoración a una ruta.
    """
    data = request.get_json()

    # Validación de datos obligatorios
    if not data or 'valoracion' not in data or 'tipo' not in data or 'to_id' not in data or 'from_id' not in data:
        return jsonify({"error": "Datos insuficientes. Se requieren 'valoracion', 'tipo', 'to_id' y 'from_id'."}), 400

    # Validar tipo ('ruta')
    if data['tipo'] != 'ruta':
        return jsonify({"error": "El tipo debe ser 'ruta'."}), 400

    # Crear una nueva valoración
    nueva_valoracion = Valoraciones(
        valoracion=data['valoracion'],
        tipo=data['tipo'],
        to_id=data['to_id'],
        from_id=data['from_id']
    )

    db.session.add(nueva_valoracion)
    db.session.commit()

    return jsonify(nueva_valoracion.serialize()), 201


@api.route('/valoraciones/<int:ruta_id>', methods=['GET'])
def obtener_valoraciones(ruta_id):
    """
    Recuperar todas las valoraciones de una ruta específica.
    """
    # Obtener todas las valoraciones asociadas a una ruta
    valoraciones = Valoraciones.query.filter_by(to_id=ruta_id).all()

    if not valoraciones:
        return jsonify({"message": f"No se encontraron valoraciones para la ruta con ID {ruta_id}."}), 404

    return jsonify([valoracion.serialize() for valoracion in valoraciones]), 200


@api.route('/valoraciones/<int:id>', methods=['DELETE'])
def eliminar_valoracion(id):
    """
    Eliminar una valoración de una ruta.
    """
    valoracion = Valoraciones.query.get(id)

    if not valoracion:
        return jsonify({"error": f"No se encontró ninguna valoración con ID {id}."}), 404

    db.session.delete(valoracion)
    db.session.commit()

    return jsonify({"message": f"Valoración con ID {id} eliminada exitosamente."}), 200