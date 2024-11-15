from datetime import datetime
from flask import Blueprint, Response, jsonify, request
from bson import json_util

from decorators.role_controls import get_current_user, role_required

from dbconnection.db import db
collections_bp = Blueprint('collections', __name__)


@collections_bp.route('/collections', methods=['GET'])
def get_all_collections():
    try:
        collections = db.list_collection_names()

        user = get_current_user()
        if user != None and user["access_rights"] != "owner":
            print(collections)
            collections.remove("Keys")
        return jsonify(collections), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@collections_bp.route('/collections/<collection_name>', methods=['DELETE'])
@role_required("owner")
def delete_collection(collection_name):
    try:
        db.drop_collection(collection_name)
        return jsonify({'message': f'Колекція {collection_name} видалена успішно'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@collections_bp.route('/collections/<collection_name>', methods=['POST'])
@role_required("owner")
def create_collection(collection_name):
    try:
        db[collection_name].insert_one({"Void": "void"})
        return jsonify({'message': f'Колекція {collection_name} створена успішно'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
