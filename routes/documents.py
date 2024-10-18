from datetime import datetime
from bson import ObjectId
from flask import Blueprint, jsonify, request

from decorators.role_controls import role_required

from dbconnection.db import db

documents_bp = Blueprint('documents', __name__)


@documents_bp.route('/documents/<collection_name>', methods=['GET'])
def get_documents(collection_name):
    try:
        documents = list(db[collection_name].find())
        formatted_documents = []

        for doc in documents:
            formatted_doc = []
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    value_type = "objectId"
                    value = str(value)
                elif isinstance(value, bool):
                    value_type = "boolean"
                elif isinstance(value, (int, float)):
                    value_type = "number"
                elif isinstance(value, datetime):
                    value_type = "date"
                    value = value.isoformat()
                else:
                    value_type = "string"

                formatted_doc.append({
                    'field_name': key,
                    'field_value': value,
                    'field_type': value_type
                })

            formatted_documents.append(formatted_doc)

        return jsonify({'documents': formatted_documents}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@documents_bp.route('/documents/<collection_name>', methods=['POST'])
@role_required("operator")
def create_document(collection_name):
    try:
        if "_id" in request.json:
            del request.json["_id"]
        doc = {}
        for field_id, field_info in request.json.items():
            field_value = field_info['value']
            field_type = field_info['type']

            # Convert the field value based on its type
            if field_type == 'boolean':
                doc[field_id] = bool(field_value)  # Ensure it's a boolean
            elif field_type == 'number':
                doc[field_id] = float(field_value)  # Convert to float
            elif field_type == 'date':
                doc[field_id] = datetime.fromisoformat(
                    field_value)  # Convert to datetime
            else:  # Assuming all other types are string
                doc[field_id] = str(field_value)
        db[collection_name].insert_one(doc)
        return jsonify({'message': 'Документ додано успішно'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@documents_bp.route('/documents/<collection_name>/<doc_id>', methods=['PUT'])
@role_required("operator")
def update_document(collection_name, doc_id):
    try:
        updated_data = request.json
        updates = {}

        # Перетворюємо типи полів перед оновленням

        field_name = updated_data.get('field_name')
        field_value = updated_data.get('field_value')
        field_type = updated_data.get('field_type')

        if field_type == 'number':
            # Перетворюємо в число
            field_value = float(
                field_value) if '.' in field_value else int(field_value)
        elif field_type == 'boolean':
            # Перетворюємо в булеве значення
            field_value = bool(field_value)
        elif field_type == 'date':
            # Перетворюємо у datetime
            field_value = datetime.fromisoformat(field_value)
        elif field_type == 'objectId':
            # Перетворюємо у ObjectId
            field_value = ObjectId(field_value)
        # В іншому випадку залишаємо як рядок (string)

        # Додаємо перетворене поле до оновлень
        updates[field_name] = field_value

        # Оновлюємо документ у колекції
        result = db[collection_name].update_one(
            {'_id': ObjectId(doc_id)},
            {'$set': updates}
        )

        if result.modified_count == 1:
            return jsonify({'message': 'Документ оновлено успішно'}), 200
        else:
            return jsonify({'message': 'Документ не знайдено або немає змін'}), 404

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


@documents_bp.route('/documents/<collection_name>/<doc_id>', methods=['DELETE'])
@role_required("operator")
def delete_document(collection_name, doc_id):
    try:
        print(collection_name)
        print(doc_id)
        result = db[collection_name].delete_one({'_id': ObjectId(doc_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Документ видалено успішно'}), 200
        else:
            return jsonify({'message': 'Документ не знайдено'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
