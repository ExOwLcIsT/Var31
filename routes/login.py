from flask import Blueprint, request, jsonify, make_response

from dbconnection.db import db

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if len(password) < 8 or len(password) > 16:
        return jsonify({'error': 'Пароль має бути від 8 до 16 символів'}), 400

    user = db.Keys.find_one({'username': username})
    
    if user and (user['password'] == password):
        response = make_response(jsonify({'message': 'Вхід успішний!'}))
        response.set_cookie('logged_in_user', username)
        return response, 200

    return jsonify({'error': 'Неправильне ім`я користувача або пароль'}), 401

@login_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    access_rights = data.get('access_rights')
    if len(password) < 8 or len(password) > 16:
        return jsonify({'error': 'Пароль має бути від 8 до 16 символів'}), 400
    db.Keys.insert_one(
        {'username': username, 'password': password, 'access_rights': access_rights})

    return jsonify({'message': 'Користувача успішно зареєстровано!'}), 201

@login_bp.route('/logout', methods=['POST'])
def logout():
    # Clear the cookie by setting an empty value and expiration
    response = make_response(jsonify({'message': 'Ви вийшли з системи'}))
    response.set_cookie('logged_in_user', '', expires=0)
    return response, 200

@login_bp.route('/role', methods=['GET'])
def get_role():
    # Отримуємо username з cookies
    username = request.cookies.get('logged_in_user')
    
    if not username:
        return jsonify({'role': 'none'}), 200
    
    # Пошук користувача в базі даних
    user = db.Keys.find_one({'username': username})
    
    if not user:
        return jsonify({'role': 'none'}), 200
    
    # Отримуємо роль користувача
    role = user.get('access_rights')
    
    # Повертаємо роль користувача
    return jsonify({'role': role}), 200

@login_bp.route('/forgot-password/<username>', methods=['GET'])
def get_password(username):    
    if not username:
        return jsonify({'message': 'такого користувача немає'}), 400
    
    user = db.Keys.find_one({'username': username})
    
    if not user:
        return jsonify({'message': 'такого користувача немає'}), 400
    
    password = user.get('password')
    
    return jsonify({'message': password}), 200