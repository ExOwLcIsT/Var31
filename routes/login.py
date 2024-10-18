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
        # If login is successful, set a cookie with the username
        response = make_response(jsonify({'message': 'Вхід успішний!'}))
        response.set_cookie('logged_in_user', username)
        return response, 200

    return jsonify({'error': 'Неправильне ім`я користувача або пароль'}), 401


@login_bp.route('/logout', methods=['POST'])
def logout():
    # Clear the cookie by setting an empty value and expiration
    response = make_response(jsonify({'message': 'Ви вийшли з системи'}))
    response.set_cookie('logged_in_user', '', expires=0)
    return response, 200
