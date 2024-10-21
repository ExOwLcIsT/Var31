
from datetime import datetime, timedelta
import random
from bson import ObjectId
from flask import Blueprint, json, jsonify, render_template, request

from dbconnection.db import db

requests_bp = Blueprint('requests', __name__)

# 1


@requests_bp.route('/request1', methods=['GET'])
def get_request1_page():
    return render_template(
        "requests/request1.html"
    )


@requests_bp.route('/request2', methods=['GET'])
def get_request2_page():
    return render_template(
        "requests/request2.html"
    )


@requests_bp.route('/request3', methods=['GET'])
def get_request3_page():
    return render_template(
        "requests/request3.html"
    )


@requests_bp.route('/request4', methods=['GET'])
def get_request4_page():
    return render_template(
        "requests/request4.html"
    )


@requests_bp.route('/request5', methods=['GET'])
def get_request5_page():
    return render_template(
        "requests/request5.html"
    )


@requests_bp.route('/request6', methods=['GET'])
def get_request6_page():
    return render_template(
        "requests/request6.html"
    )


@requests_bp.route('/request7', methods=['GET'])
def get_request7_page():
    return render_template(
        "requests/request7.html"
    )


@requests_bp.route('/request8', methods=['GET'])
def get_request8_page():
    return render_template(
        "requests/request8.html"
    )


@requests_bp.route('/request9', methods=['GET'])
def get_request9_page():
    return render_template(
        "requests/request9.html"
    )


@requests_bp.route('/request10', methods=['GET'])
def get_request10_page():
    return render_template(
        "requests/request10.html"
    )


@requests_bp.route('/api/services', methods=['GET'])
def get_services():
    services = list(db.TaxiServices.find({}))
    service_names = []
    for doc in services:
        service_names.append({"name": doc["name"], "_id": str(doc["_id"])})
    return jsonify(service_names)


@requests_bp.route('/api/rides', methods=['GET'])
def get_rides_by_service():
    service_id = request.args.get('service')

    try:
        # Перетворюємо service_id у ObjectId
        service_id = ObjectId(service_id)

        # Запит до колекції rides
        rides = db.Rides.aggregate([
            {
                # Поєднуємо колекцію rides з Employees через driver_id
                '$lookup': {
                    'from': 'Employees',
                    'localField': 'driver_id',
                    'foreignField': '_id',
                    'as': 'driver_info'
                }
            },
            {
                '$unwind': {
                    'path': '$driver_info',
                    'preserveNullAndEmptyArrays': True  # Зберігаємо виїзди без водія
                }
            },
            {
                # Фільтруємо виїзди за service_id, який є в колекції Employees
                '$match': {
                    'driver_info.service_id': service_id  # Порівнюємо service_id з Employees
                }
            },
            {
                # Поєднуємо колекцію rides з Cars через car_id
                '$lookup': {
                    'from': 'Cars',
                    'localField': 'car_id',
                    'foreignField': '_id',
                    'as': 'car_info'
                }
            },
            {
                '$unwind': {
                    'path': '$car_info',
                    'preserveNullAndEmptyArrays': True  # Зберігаємо виїзди без автомобіля
                }
            },
            {
                # Поєднуємо колекцію rides з TaxiServices через service_id
                '$lookup': {
                    'from': 'TaxiServices',
                    'localField': 'driver_info.service_id',
                    'foreignField': '_id',
                    'as': 'service_info'
                }
            },
            {
                '$unwind': {
                    'path': '$service_info',
                    'preserveNullAndEmptyArrays': True  # Зберігаємо виїзди без служби
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'car_name': {
                        '$concat': [
                            '$car_info.brand',
                            ' ',
                            '$car_info.license_plate'
                        ]
                    },
                    'driver_name': {
                        '$concat': [
                            '$driver_info.first_name',
                            ' ',
                            '$driver_info.last_name'
                        ]
                    },
                    'service_name': '$service_info.name',  # Назва служби
                    'start_time': 1,                 # Час початку
                    'end_time': 1,                   # Час закінчення
                    'distance_km': 1,                # Відстань в км
                    'status': 1                       # Статус
                }
            }
        ])

        results = list(rides)

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": "Виникла помилка при отриманні поїздок"}), 500


# 2
@requests_bp.route('/api/vehicles/not_passed_inspection', methods=['GET'])
def get_vehicles_not_passed_inspection():
    try:
        # Запит до колекції автомобілів
        vehicles = db.Cars.find({
            'year_of_manufacture': {'$lt': 2015},
            'inspection_expiry': {'$lt':  datetime(2024, 12, 31)}
        })
        # Форматування результатів у список
        vehicle_list = []
        for vehicle in vehicles:
            vehicle_list.append({
                'id': str(vehicle['_id']),
                'brand': vehicle.get('brand'),
                'year': vehicle.get('year_of_manufacture')
            })
        return jsonify(vehicle_list), 200

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

# 3


@requests_bp.route('/api/drivers/by_car_brand', methods=['GET'])
def get_drivers_by_car_brand():
    brand = request.args.get('brand')

    # Запит для отримання унікальних водіїв, які їздять на автомобілях заданої марки
    drivers = db.Rides.aggregate([
        {
            '$lookup': {
                'from': 'Cars',
                'localField': 'car_id',
                'foreignField': '_id',
                'as': 'car_info'
            }
        },
        {
            '$unwind': '$car_info'
        },
        {
            '$match': {
                'car_info.brand': brand  # Фільтрація по марці автомобіля
            }
        },
        {
            '$lookup': {
                'from': 'Employees',
                'localField': 'driver_id',
                'foreignField': '_id',
                'as': 'driver_info'
            }
        },
        {
            '$unwind': '$driver_info'
        },
        {
            '$group': {
                '_id': {
                    'first_name': '$driver_info.first_name',
                    'last_name': '$driver_info.last_name'
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'first_name': '$_id.first_name',
                'last_name': '$_id.last_name',
            }
        }
    ])
    
    result = json.dumps(list(drivers))
    return result

# 4


@requests_bp.route('/api/drivers/no_orders_today', methods=['GET'])
def get_drivers_without_orders():
    # Отримання поточної дати
    today = datetime.now().date()

    # Знайдемо всіх водіїв, які не мають жодного замовлення за поточний день
    drivers = db.Employees.aggregate([
        {
            '$lookup': {
                'from': 'Rides',  # Колекція замовлень
                'localField': '_id',
                'foreignField': 'driver_id',
                'as': 'rides'
            }
        },
        {
            '$addFields': {
                'today_rides': {
                    '$filter': {
                        'input': '$rides',
                        'as': 'ride',
                        'cond': {
                            '$eq': [
                                {'$dateToString': {
                                    'format': '%Y-%m-%d', 'date': '$$ride.date'}},
                                today.strftime('%Y-%m-%d')
                            ]
                        }
                    }
                }
            }
        },
        {
            '$match': {
                # Відфільтруємо водіїв без замовлень за сьогодні
                'today_rides': {'$size': 0}
            }
        },
        {
            '$project': {
                '_id': 0,
                'first_name': 1,
                'last_name': 1
            }
        }
    ])
    return jsonify(list(drivers)), 200


# 5
@requests_bp.route('/api/clients/by_address', methods=['GET'])
def get_clients_by_address():
    address = request.args.get('address')
    rides = db.Orders.aggregate([
        {
            '$match': {
                'pickup_address': address  # Фільтруємо замовлення за адресою
            }
        },
        {
            '$lookup': {
                'from': 'Clients',  # Колекція клієнтів
                'localField': 'client_id',
                'foreignField': '_id',
                'as': 'client_info'
            }
        },
        {
            '$unwind': '$client_info'  # Розпаковуємо масив client_info
        },
        {
            '$project': {
                '_id': 0,
                'first_name': '$client_info.first_name',  # Ім'я клієнта
                'last_name': '$client_info.last_name',    # Прізвище клієнта
                'phone': '$client_info.phone',            # Телефон клієнта
                'address': '$client_info.address',        # Адреса клієнта
            }
        }
    ])

    # Повертаємо список клієнтів, які замовляли таксі за вказаною адресою
    return jsonify(list(rides)), 200


# 6
@requests_bp.route('/api/dispatcher/calls_per_day', methods=['GET'])
def get_calls_per_dispatcher_per_day():
    today = datetime.now()

    # Початок і кінець дня
    start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
    end_of_day = start_of_day + timedelta(days=1)

    dispatcher_calls = db.Orders.aggregate([
        {
            '$match': {'order_date': {
                '$gte': start_of_day,
                '$lt': end_of_day
            }}
        },
        {
            '$group': {
                '_id': '$dispatcher_id',  # Групуємо за диспетчером
                'total_calls': {'$sum': 1}  # Підраховуємо кількість викликів
            }
        },
        {
            '$lookup': {
                'from': 'Employees',  # Приєднуємо дані про диспетчерів
                'localField': '_id',
                'foreignField': '_id',
                'as': 'dispatcher_info'
            }
        },
        {
            '$unwind': '$dispatcher_info'  # Розпаковуємо масив dispatcher_info
        },
        {
            '$project': {
                '_id': 0,
                'dispatcher_name': '$dispatcher_info.first_name',  # Виводимо ім'я диспетчера
                'total_calls': 1  # Кількість викликів
            }
        }
    ])
    result = json.dumps(list(dispatcher_calls))
    return result, 200

# Маршрут для отримання кількості викликів, виконаних таксистами служб таксі щодня


@requests_bp.route('/api/taxi_service/rides_per_day', methods=['GET'])
def get_rides_per_service_per_day():
    pipeline = [
        {
            # Додавання поля для дати без часу (для групування по дням)
            "$addFields": {
                "order_day": {
                    "$dateToString": {
                        # формат тільки дати (рік-місяць-день)
                        "format": "%Y-%m-%d",
                        "date": "$order_date"
                    }
                }
            }
        },
        {
            # З'єднуємо з колекцією Employees, щоб отримати водія для кожного замовлення
            "$lookup": {
                "from": "Employees",  # Колекція співробітників
                "localField": "driver_id",  # Поле з колекції Orders
                "foreignField": "_id",  # Поле з колекції Employees
                "as": "driver_info"  # Назва для збереження результату
            }
        },
        {
            # Розпаковуємо масив driver_info
            "$unwind": "$driver_info"
        },
        {
            # З'єднуємо з колекцією TaxiServices, щоб отримати інформацію про сервіс
            "$lookup": {
                "from": "TaxiServices",  # Колекція таксі-сервісів
                "localField": "driver_info.service_id",  # Поле в водіях
                "foreignField": "_id",  # Поле в TaxiServices
                "as": "taxi_service_info"  # Назва для збереження результату
            }
        },
        {
            # Розпаковуємо масив taxi_service_info
            "$unwind": "$taxi_service_info"
        },
        {
            # Групування по фірмі (taxi_service) і дню
            "$group": {
                "_id": {
                    "taxi_service": "$taxi_service_info.name",  # групування за назвою сервісу
                    "order_day": "$order_day"  # групування по дню
                },
                # кількість викликів за день для сервісу
                "total_orders": {"$sum": 1}
            }
        },
        {
            # Форматування результату для виведення без _id
            "$project": {
                "_id": 0,  # виключити поле _id з результату
                "taxi_service": "$_id.taxi_service",  # взяти значення з _id
                "order_day": "$_id.order_day",  # взяти значення з _id
                "total_orders": 1  # залишити кількість викликів
            }
        },
        {
            # Сортування за датою і кількістю викликів (опціонально)
            "$sort": {
                "order_day": 1  # сортування по датах
            }
        }
    ]

    result = list(db.Orders.aggregate(pipeline))

    return jsonify(result), 200


# 7
@requests_bp.route('/api/taxi_services/max_orders', methods=['GET'])
def get_max_orders_taxi_service():
    start_date = request.args.get('start_date')  # Дата початку
    end_date = request.args.get('end_date')      # Дата закінчення

    pipeline = [
        {
            # Додавання поля для дати без часу (для групування по дням)
            "$addFields": {
                "order_day": {
                    "$dateToString": {
                        # формат тільки дати (рік-місяць-день)
                        "format": "%Y-%m-%d",
                        "date": "$order_date"
                    }
                }
            }
        },
        {
            # З'єднуємо з колекцією Employees, щоб отримати водія для кожного замовлення
            "$lookup": {
                "from": "Employees",
                "localField": "driver_id",
                "foreignField": "_id",
                "as": "driver_info"
            }
        },
        {
            "$unwind": "$driver_info"  # Розпаковуємо масив driver_info
        },
        {
            # З'єднуємо з колекцією TaxiServices, щоб отримати інформацію про сервіс
            "$lookup": {
                "from": "TaxiServices",
                "localField": "driver_info.service_id",
                "foreignField": "_id",
                "as": "taxi_service_info"
            }
        },
        {
            "$unwind": "$taxi_service_info"  # Розпаковуємо масив taxi_service_info
        },
        {
            # Фільтруємо за датами
            "$match": {
                "order_date": {
                    "$gte": datetime.fromisoformat(start_date),  # Дата початку
                    # Дата закінчення
                    "$lt": datetime.fromisoformat(end_date)
                }
            }
        },
        {
            # Групування по службі таксі та дню
            "$group": {
                "_id": {
                    "service_id": "$taxi_service_info._id",  # айді служби
                    "service_name": "$taxi_service_info.name"  # назва служби
                },
                "total_orders": {"$sum": 1}  # підрахунок замовлень
            }
        },
        {
            # Групування по службі, щоб підрахувати загальну кількість замовлень
            "$group": {
                "_id": "$_id.service_id",
                "service_name": {"$first": "$_id.service_name"},
                "total_orders": {"$sum": "$total_orders"}
            }
        },
        {
            # Сортування за кількістю замовлень
            "$sort": {
                "total_orders": -1  # Сортування за спаданням
            }
        },
        {
            # Обмежуємо результати до 1, щоб отримати тільки службу з максимальною кількістю замовлень
            "$limit": 1
        },
        {
            # Форматування результату для виведення без _id
            "$project": {
                "_id": 0,  # Виключити _id з результату
                "service_name": 1,
                "total_orders": 1
            }
        }
    ]

    max_orders_service = list(db.Orders.aggregate(pipeline))

    return jsonify(max_orders_service), 200


@requests_bp.route('/api/taxi_services/more_than_100_orders', methods=['GET'])
def get_taxi_services_more_than_100_orders():

    pipeline = [
        {
            # Додавання поля для дати без часу (для групування по дням)
            "$addFields": {
                "order_day": {
                    "$dateToString": {
                        # формат тільки дати (рік-місяць-день)
                        "format": "%Y-%m-%d",
                        "date": "$order_date"
                    }
                }
            }
        },
        {
            # З'єднуємо з колекцією Employees, щоб отримати водія для кожного замовлення
            "$lookup": {
                "from": "Employees",
                "localField": "driver_id",
                "foreignField": "_id",
                "as": "driver_info"
            }
        },
        {
            "$unwind": "$driver_info"  # Розпаковуємо масив driver_info
        },
        {
            # З'єднуємо з колекцією TaxiServices, щоб отримати інформацію про сервіс
            "$lookup": {
                "from": "TaxiServices",
                "localField": "driver_info.service_id",
                "foreignField": "_id",
                "as": "taxi_service_info"
            }
        },
        {
            "$unwind": "$taxi_service_info"  # Розпаковуємо масив taxi_service_info
        },
        {
            # Групування по службі таксі та дню
            "$group": {
                "_id": {
                    "service_id": "$taxi_service_info._id",
                    "service_name": "$taxi_service_info.name",
                    "order_day": "$order_day"
                },
                "total_orders": {"$sum": 1}  # підрахунок замовлень
            }
        },
        {
            # Фільтрація для служб, які виконують більше 100 викликів на день
            "$match": {
                "total_orders": {"$gt": 100}
            }
        },
        {
            # Сортування
            "$sort": {
                "total_orders": -1  # Сортування за спаданням
            }
        },
        {
            # Форматування результату для виведення без _id
            "$project": {
                "_id": 0,
                "service_name": "$_id.service_name",
                "order_day": "$_id.order_day",
                "total_orders": 1
            }
        }
    ]

    services_with_many_orders = list(db.Orders.aggregate(pipeline))

    return jsonify(services_with_many_orders), 200


# 8
@requests_bp.route('/api/cars/mileage', methods=['GET'])
def get_car_mileage_by_day():
    license_plate = request.args.get('license_plate')  # Номер машини
    date = request.args.get('date')               # Дата у форматі YYYY-MM-DD

    # Використовуємо агрегаційний запит для обчислення загальної довжини пробігу
    pipeline = [
        {
            # З'єднуємо з колекцією Cars
            "$lookup": {
                "from": "Cars",
                "localField": "car_id",
                "foreignField": "_id",
                "as": "car_info"
            }
        },
        {
            # Розпаковуємо масив car_info
            "$unwind": "$car_info"
        },
        {
            # Фільтруємо за номером автомобіля
            "$match": {
                "car_info.license_plate": license_plate
            }
        },
        {
            # Групуємо за license_plate і підсумовуємо distance_km
            "$group": {
                "_id": None,  # Не групуємо за конкретним полем
                "total_distance_km": {"$sum": "$distance_km"}
            }
        },
        {
            # Форматування результату
            "$project": {
                "_id": 0,              # Виключити _id з результату
                "total_distance_km": 1  # Загальна відстань
            }
        }
    ]

    result = list(db.Rides.aggregate(pipeline))

    # Перевірка наявності результату
    if result:
        total_distance = result[0].get('total_distance_km', 0)
    else:
        total_distance = 0

    return jsonify(total_distance), 200


# 9
@requests_bp.route('/api/clients/multiple_services', methods=['GET'])
def get_clients_multiple_services():
    pipeline = [
        {
            '$lookup': {
                'from': 'Orders',
                'localField': '_id',
                'foreignField': 'client_id',
                'as': 'orders'
            }
        },
        {
            '$match': {
                # Переконайтеся, що у клієнта є замовлення
                'orders': {'$ne': []}
            }
        },
        {
            '$unwind': {
                'path': '$orders',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$lookup': {
                'from': 'Employees',
                'localField': 'orders.driver_id',
                'foreignField': '_id',
                'as': 'employee_info'
            }
        },
        {
            '$match': {
                # Переконайтеся, що водій знайдений
                'employee_info': {'$ne': []}
            }
        },
        {
            '$lookup': {
                'from': 'Clients',  # Назва колекції клієнтів
                'localField': '_id',  # Можливо, тут потрібно використовувати orders.client_id
                'foreignField': '_id',  # Переконайтеся, що це правильне поле
                'as': 'client_info'  # Додати дані про клієнтів
            }
        },
        {
            '$unwind': {
                'path': '$client_info',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$group': {
                '_id': '$_id',  # Групуємо по id клієнта
                # Витягуємо id клієнта
                'client_id': {'$first': '$client_info._id'},
                # Зміна поля на правильне
                'client_first_name': {'$first': '$client_info.first_name'},
                # Зміна поля на правильне
                'client_last_name': {'$first': '$client_info.last_name'},
                # Унікальні service_id
                'services': {'$addToSet': '$employee_info.service_id'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'client_first_name': 1,  # Включаємо ім'я
                'client_last_name': 1,   # Включаємо прізвище
                'services': 1,
                'num_services': {'$size': '$services'}  # Кількість служб
            }
        },
        {
            '$match': {
                'num_services': {'$gt': 1}  # Фільтруємо за кількістю служб
            }
        }
    ]
    clients_with_multiple_services = []

    result = list(db.Clients.aggregate(pipeline))
    for item in result:
        if item['num_services'] > 1:
            clients_with_multiple_services.append(
                item['client_first_name'] + " " + item['client_last_name'])
    print(clients_with_multiple_services)
    return jsonify(clients_with_multiple_services), 200


# 10
@requests_bp.route('/api/client/<client_id>/trips/weekly', methods=['GET'])
def get_weekly_trips(client_id):
    c_id = ObjectId(client_id)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    trips = db.Orders.find({
        'client_id': c_id,
        'order_date': {'$gte': start_date, '$lt': end_date}
    }, {'_id': 0, 'destination_address': 1, 'order_date': 1})

    trips_list = list(trips)
    return jsonify(trips_list)


@requests_bp.route('/api/client/<client_id>/calls/monthly', methods=['GET'])
def get_monthly_calls(client_id):
    c_id = ObjectId(client_id)
    start_date = datetime.now() - timedelta(days=30)

    calls_count = db.Orders.find({
        'client_id': c_id,
        'order_date': {'$gte': start_date}
    })
    l = list(calls_count).__len__()
    return jsonify(l)
