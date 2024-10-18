from functools import wraps
from flask import request, jsonify
from pymongo import MongoClient

from dbconnection.db import db


def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user:
                user_access_rights = "user"
            else:
                user_access_rights = user.get('access_rights')

            roles_hierarchy = ['user', 'operator', 'admin', 'owner']
            if roles_hierarchy.index(user_access_rights) < roles_hierarchy.index(required_role):
                return jsonify({'error': 'Недостатньо прав доступу'}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator


def get_current_user():
    username = request.cookies.get('logged_in_user')
    if username:
        return db.Keys.find_one({'username': username})
    return None
