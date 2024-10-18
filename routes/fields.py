from datetime import datetime
from flask import Blueprint, Response, jsonify, request
from bson import ObjectId, json_util

from decorators.role_controls import role_required

from dbconnection.db import db

fields_bp = Blueprint('fields', __name__)


@fields_bp.route('/fields/<collection_name>', methods=['GET'])
def get_collection_data(collection_name):
    try:
        collection = db[collection_name]
        documents = list(collection.find({}))

        if not documents:
            return jsonify({"error": "Колекція порожня або не існує"}), 404

        # Initialize a list to hold field information
        field_types = []

        # Get field names from the first document
        fields = list(documents[0].keys())

        for field in fields:
            # Determine the type of each field based on the first document
            value = documents[0][field]
            if isinstance(value, ObjectId):
                value_type = "objectId"
            elif isinstance(value, bool):
                value_type = "boolean"
            elif isinstance(value, (int, float)):
                value_type = "number"
            elif isinstance(value, datetime):
                value_type = "date"
            else:
                value_type = "string"
            
            # Append field information to the list
            field_types.append({
                'field_name': field,
                'field_type': value_type
            })

        response = {
            "collection_name": collection_name,
            "fields": field_types  
        }

        return Response(json_util.dumps(response), mimetype='application/json'), 200
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500


@fields_bp.route('/fields/<collection_name>/<field_name>', methods=['PUT'])
@role_required("admin")
def update_column(collection_name, field_name):

    data = request.json
    old_field_name = field_name
    new_field_name = data.get('newFieldName')
    if not old_field_name or not new_field_name:
        return jsonify({"error": "Назва старої та нової колонки є обов'язковими"}), 400

    if old_field_name == "_id":
        return jsonify({"error": "Не можна змінювати колонку _id"}), 400

    try:
        collection = db[collection_name]

        collection.update_many(
            {}, {'$rename': {old_field_name: new_field_name}})

        return jsonify({"message": f"Колонку '{old_field_name}' змінено на '{new_field_name}'"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fields_bp.route('/fields/<collection_name>/<field_name>', methods=['DELETE'])
@role_required("admin")
def delete_column(collection_name, field_name):
    if not field_name:
        return jsonify({"error": "Назва поля є обов'язковою"}), 400

    if field_name == "_id":
        return jsonify({"error": "Не можна видалити поле _id"}), 400
    try:
        collection = db[collection_name]

        collection.update_many({}, {'$unset': {field_name: ""}})

        return jsonify({"message": f"Поле '{field_name}' успішно видалено"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fields_bp.route('/fields/<collectionName>/<field_name>', methods=['POST'])
def add_column(collectionName, field_name):
    try:
        data = request.json
        type = data.get('type')

        if not field_name or not field_name:
            return jsonify({'error': 'Некоректні дані'}), 400

        collection = db[collectionName]
        print(type)
        if type == 'string':
            default_value = ''
        elif type == 'number':
            default_value = 0
        elif type == 'date':
            default_value = datetime.now()
        elif type == 'boolean':
            default_value = False
        elif type == 'objectId':
            default_value = ''
        else:
            return jsonify({'error': 'Невідомий тип даних'}), 400

        collection.update_many({}, {'$set': {field_name: default_value}})

        return jsonify({'message': 'Колонка успішно додана'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
