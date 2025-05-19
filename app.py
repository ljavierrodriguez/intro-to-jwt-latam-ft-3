import os
import datetime
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from models import db, User
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)

db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
jwt = JWTManager(app)
CORS(app)


@app.route('/')
def main():
    return jsonify({ "status": "Server running successfully!"}), 200

@app.route('/login', methods=['POST'])
def user_login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username:
        return jsonify({"msg": "Username is required!"}), 400
    
    if not password:
        return jsonify({"msg": "Password is required!"}), 400
    
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({ "msg": "Username/password are incorrects!"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({ "msg": "Username/password are incorrects!"}), 401

    expire = datetime.timedelta(hours=1)
    token = create_access_token(identity=str(user.id), expires_delta=expire)

    #token = create_access_token(identity=str(user.id))

    datos = {
        "token": token,
        "user": user.serialize()
    }

    return jsonify(datos), 200
    

@app.route('/register', methods=['POST'])
def user_register():
    
    username = request.json.get('username')
    password = request.json.get('password')

    if not username:
        return jsonify({"msg": "Username is required!"}), 400
    
    if not password:
        return jsonify({"msg": "Password is required!"}), 400
    
    found = User.query.filter_by(username=username).first()

    if found:
        return jsonify({"msg": "Username is already used!"}), 400
    
    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.save()

    if user:
        return jsonify({ "status": "success", "message": "Regiter successfully!"}), 200
    
    return jsonify({"status": "error", "message": "Register Error, please try later"}), 200

@app.route('/profile', methods=['GET'])
@jwt_required() # indicamos que la ruta es privada
def profile():

    id = get_jwt_identity()

    user = User.query.get(id)

    if not user:
        return jsonify({ "msg": "User not found"}), 404

    return jsonify(user.serialize()), 200

if __name__ == '__main__':
    app.run()
