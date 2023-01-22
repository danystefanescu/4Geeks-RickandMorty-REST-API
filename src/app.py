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
from models import db, User, Character, Location, Episode

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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# <------------------- USER GET AND POST -------------------------------------------------------->

@app.route('/user', methods=['POST','GET'])
def handle_users():

     if request.method == 'POST':
        body = request.get_json()
        user = User(
            user_name=body['user_name'],
            first_name=body['first_name'],
            last_name=body['last_name'],
            email= body['email'],
            password=body['password'],
            is_active=True         
        )
        db.session.add(user)
        db.session.commit()
        response_body = {
        "msg": "User added correctly !"
        }
        return jsonify(response_body), 200

     if request.method == 'GET':
        users = User.query.all()
        users_serialized = [x.serialize() for x in users]
        response_body = {
            "msg": "This is your /GET for table 'User' !"
        }
        return jsonify({"Users" : users_serialized}, response_body), 200


# DELETE a USER based on it's ID ---------------------------------------------------------------------->

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user_query = User.query.get(user_id)
    if not user_query:
        response_body = {
            "msg" : "This user doesn't exist, can't be deleted."
        }
        return jsonify(response_body), 200

    db.session.delete(user_query)
    db.session.commit()
    response_body = {
        "msg" : "User deleted correctly !"
    }

    return jsonify(response_body), 200

# GET a USER based on it's ID ------------------------------------------------------------------------->

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user_query = User.query.get(user_id)
    
    if not user_query:
        response_body = {
            "msg" : "The user you are looking for doesn't exist."
        }
        return jsonify(response_body), 200

    user_serialize = user_query.serialize()
    return jsonify({"Result": user_serialize}), 200


# <------------------- CHARACTER GET AND POST -------------------------------------------------------->

@app.route('/character', methods=['POST','GET'])
def handle_characters():
    if request.method == 'POST':
        body = request.get_json()
        character = Character(
            name=body['name'],
            species=body['species'],
            gender=body['gender'],
            is_alive=True   
        )
        db.session.add(character)
        db.session.commit()
        response_body = {
        "msg": "Character added correctly !"
        }
        return jsonify(response_body), 200

    if request.method == 'GET':
        characters = Character.query.all()
        characters_serialized = [x.serialize() for x in characters]
        response_body = {
            "msg": "This is your /GET for table 'Character' !"
        }
        return jsonify({"Characters" : characters_serialized}, response_body), 200


# DELETE a CHARACTER based on it's ID ----------------------------------------------------------------->

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character_by_id(character_id):
    character_query = Character.query.get(character_id)
    if not character_query:
        response_body = {
            "msg" : "This character doesn't exist, can't be deleted."
        }
        return jsonify(response_body), 200

    db.session.delete(character_query)
    db.session.commit()
    response_body = {
        "msg" : "User deleted correctly !"
    }

    return jsonify(response_body), 200

# GET a CHARACTER based on it's ID -------------------------------------------------------------------->

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    character_query = Character.query.get(character_id)
    
    if not character_query:
        response_body = {
            "msg" : "The user you are looking for doesn't exist."
        }
        return jsonify(response_body), 200

    character_serialize = character_query.serialize()
    return jsonify({"Result": character_serialize}), 200


# <------------------- LOCATION GET AND POST -------------------------------------------------------->

@app.route('/location', methods=['POST','GET'])
def handle_locations():
    if request.method == 'POST':
        body = request.get_json()
        location = Location(
            name=body['name'],
            type=body['type'],
            dimension=body['dimension']
        )
        db.session.add(location)
        db.session.commit()
        response_body = {
        "msg": "Location added correctly !"
        }
        return jsonify(response_body), 200

    if request.method == 'GET':
        locations = Location.query.all()
        locations_serialized = [x.serialize() for x in locations]
        response_body = {
            "msg": "This is your /GET for table 'Location' !"
        }
        return jsonify({"Locations" : locations_serialized}, response_body), 200


# DELETE a LOCATION based on it's ID ---------------------------------------------------------------->

@app.route('/location/<int:location_id>', methods=['DELETE'])
def delete_location_by_id(location_id):
    location_query = Location.query.get(location_id)
    if not location_query:
        response_body = {
            "msg" : "This character doesn't exist, can't be deleted."
        }
        return jsonify(response_body), 200

    db.session.delete(location_query)
    db.session.commit()
    response_body = {
        "msg" : "User deleted correctly !"
    }

    return jsonify(response_body), 200

# GET a CHARACTER based on it's ID -------------------------------------------------------------------->

@app.route('/location/<int:location_id>', methods=['GET'])
def get_location_by_id(location_id):
    location_query = Location.query.get(location_id)
    
    if not location_query:
        response_body = {
            "msg" : "The user you are looking for doesn't exist."
        }
        return jsonify(response_body), 200

    location_serialize = location_query.serialize()
    return jsonify({"Result": location_serialize}), 200


# <------------------- EPISODE GET AND POST -------------------------------------------------------->

@app.route('/episode', methods=['POST','GET'])
def handle_episodes():
    if request.method == 'POST':
        body = request.get_json()
        episode = Episode(
            name=body['name'],
            air_date=body['air_date'],
            episode=body['episode']
        )
        db.session.add(episode)
        db.session.commit()
        response_body = {
        "msg": "Episode added correctly !"
        }
        return jsonify(response_body), 200

    if request.method == 'GET':
        episodes = Episode.query.all()
        episodes_serialized = [x.serialize() for x in episodes]
        response_body = {
            "msg": "This is your /GET for table 'Episode' !"
        }
        return jsonify({"Episodes" : episodes_serialized}, response_body), 200


# DELETE a EPISODE based on it's ID ---------------------------------------------------------------->

@app.route('/episode/<int:episode_id>', methods=['DELETE'])
def delete_episode_by_id(episode_id):
    episode_query = Location.query.get(episode_id)
    if not episode_query:
        response_body = {
            "msg" : "This character doesn't exist, can't be deleted."
        }
        return jsonify(response_body), 200

    db.session.delete(episode_query)
    db.session.commit()
    response_body = {
        "msg" : "User deleted correctly !"
    }

    return jsonify(response_body), 200

# GET a EPISODE based on it's ID -------------------------------------------------------------------->

@app.route('/episode/<int:episode_id>', methods=['GET'])
def get_episode_by_id(episode_id):
    episode_query = Episode.query.get(episode_id)
    
    if not episode_query:
        response_body = {
            "msg" : "The user you are looking for doesn't exist."
        }
        return jsonify(response_body), 200

    episode_serialize = episode_query.serialize()
    return jsonify({"Result": episode_serialize}), 200


# <------------------- SERVER RUN ON PORT 3000 -------------------------------------------------------->

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
