"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/member', methods=['POST'])
def create_members():
    request_body = request.get_json() #Primero hay que recibir el cuerpo de la solicitud.
    if 'first_name' not in request_body or 'age' not in request_body or 'lucky_numbers' not in request_body: #Validamos que la respeusta incluya los 3 datos necesarios
        return jsonify({"error":"Missing data"}), 400
    
    new_member = {  #Añadimos la información nueva
        "first_name": request_body["first_name"],
        "age": request_body["age"],
        "lucky_numbers": request_body["lucky_numbers"],
        "id": 3443,
        "last_name": jackson_family.last_name,
    }
    jackson_family.add_member(new_member)
    return jsonify(new_member), 200 #devolvemos el resultado

@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)  # Pasamos el id a la función
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404  # Si no se encuentra el miembro


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    jackson_family.delete_member(id)

    return jsonify({"done": True}), 200
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
