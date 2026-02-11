"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import *

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():
    personajes = PersonajeSimpson.query.all()
    return jsonify([p.serialize() for p in personajes]), 200

@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje = PersonajeSimpson.query.get(personaje_id)
    if personaje is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(personaje.serialize()), 200

@app.route('/personajes', methods=['POST'])
def create_personaje():
    data = request.json
    nuevo = PersonajeSimpson(
        nombre=data.get("nombre"),
        edad=data.get("edad"),
        ocupacion=data.get("ocupacion"),
        frase_iconica=data.get("frase_iconica")
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"msg": "Personaje creado", "personaje": nuevo.serialize()}), 201

@app.route('/personajes/<int:personaje_id>', methods=['PUT'])
def update_personaje(personaje_id):
    personaje = PersonajeSimpson.query.get(personaje_id)
    if personaje is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404

    data = request.json
    personaje.nombre = data.get("nombre", personaje.nombre)
    personaje.edad = data.get("edad", personaje.edad)
    personaje.ocupacion = data.get("ocupacion", personaje.ocupacion)
    personaje.frase_iconica = data.get("frase_iconica", personaje.frase_iconica)

    db.session.commit()
    return jsonify({"msg": "Personaje actualizado", "personaje": personaje.serialize()}), 200

@app.route('/personajes/<int:personaje_id>', methods=['DELETE'])
def delete_personaje(personaje_id):
    personaje = PersonajeSimpson.query.get(personaje_id)
    if personaje is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404

    db.session.delete(personaje)
    db.session.commit()
    return jsonify({"msg": "Personaje eliminado"}), 200

@app.route('/locations', methods=['GET'])
def get_locations():
    lugares = Lugar.query.all()
    return jsonify([l.serialize() for l in lugares]), 200

@app.route('/locations/<int:lugar_id>', methods=['GET'])
def get_location(lugar_id):
    lugar = Lugar.query.get(lugar_id)
    if lugar is None:
        return jsonify({"msg": "Lugar no encontrado"}), 404
    return jsonify(lugar.serialize()), 200

@app.route('/locations', methods=['POST'])
def create_location():
    data = request.json
    nuevo = Lugar(
        nombre=data.get("nombre"),
        tipo=data.get("tipo"),
        direccion=data.get("direccion"),
        descripcion=data.get("descripcion")
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"msg": "Lugar creado", "lugar": nuevo.serialize()}), 201

@app.route('/locations/<int:lugar_id>', methods=['PUT'])
def update_location(lugar_id):
    lugar = Lugar.query.get(lugar_id)
    if lugar is None:
        return jsonify({"msg": "Lugar no encontrado"}), 404

    data = request.json
    lugar.nombre = data.get("nombre", lugar.nombre)
    lugar.tipo = data.get("tipo", lugar.tipo)
    lugar.direccion = data.get("direccion", lugar.direccion)
    lugar.descripcion = data.get("descripcion", lugar.descripcion)

    db.session.commit()
    return jsonify({"msg": "Lugar actualizado", "lugar": lugar.serialize()}), 200

@app.route('/locations/<int:lugar_id>', methods=['DELETE'])
def delete_location(lugar_id):
    lugar = Lugar.query.get(lugar_id)
    if lugar is None:
        return jsonify({"msg": "Lugar no encontrado"}), 404

    db.session.delete(lugar)
    db.session.commit()
    return jsonify({"msg": "Lugar eliminado"}), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1

    personajes = FavoritoPersonaje.query.filter_by(user_id=user_id).all()
    lugares = FavoritoLugar.query.filter_by(user_id=user_id).all()

    return jsonify({
        "personajes_favoritos": [p.serialize() for p in personajes],
        "lugares_favoritos": [l.serialize() for l in lugares]
    }), 200


@app.route('/favorite/location/<int:lugar_id>', methods=['POST'])
def add_favorite_location(lugar_id):
    user_id = 1
    nuevo = FavoritoLugar(user_id=user_id, lugar_id=lugar_id)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"msg": "Lugar añadido a favoritos"}), 201


@app.route('/favorite/personaje/<int:personaje_id>', methods=['POST'])
def add_favorite_personaje(personaje_id):
    user_id = 1
    nuevo = FavoritoPersonaje(user_id=user_id, personaje_id=personaje_id)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"msg": "Personaje añadido a favoritos"}), 201


@app.route('/favorite/location/<int:lugar_id>', methods=['DELETE'])
def delete_favorite_location(lugar_id):
    user_id = 1
    fav = FavoritoLugar.query.filter_by(user_id=user_id, lugar_id=lugar_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Lugar eliminado de favoritos"}), 200


@app.route('/favorite/personaje/<int:personaje_id>', methods=['DELETE'])
def delete_favorite_personaje(personaje_id):
    user_id = 1
    fav = FavoritoPersonaje.query.filter_by(user_id=user_id, personaje_id=personaje_id).first()
    if fav is None:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Personaje eliminado de favoritos"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
