import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import login_required, current_user
meal = Blueprint('meals', 'meal')

@meal.route('/', methods=["GET"])
# @login_required
def get_all_meals():
    try:
        meals = [model_to_dict(meal) for meal in models.Meal.select()]
        # print(meals)
        return jsonify(data=meals, status={'code': 200, 'message': 'Success'})
    except:
        return jsonify(data={}, status={'code': 500, 'message': 'Error getting resources'})


@meal.route('/', methods=["POST"])
def create_meals():
    body = request.get_json()
    print(body)
    new_meal = models.Meal.create(**body)
    # same exact thing as:
    # new_meal = models.meal.create(id=body['id'], meal=body['meal'], restlink=body['restlink'], pic=body['pic'])
    meal_data = model_to_dict(new_meal)
    return jsonify(data=meal_data, status={'code': 200, 'message': 'Success'})

##ind show route
    @meal.route('/<id>, methods=["GET"])')
    def get_one_meal(id):
        meal + models.Meal.get_by_id(id)
        print(meal.__dict__)
        return jsonify(data=model_to_dict(meal), status={"code": 200, "message":"Success"})

#update meal
@meal.route('/<id>', methods=["PUT"])
def update_meal(id):
      payload = request.get_json()
      query = models.Meal.update(**payload).where(models.Meal.id == id)
      query.execute()
      return jsonify(data=model_to_dict(models.Meal.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})

#delete
@meal.route('/<id>', methods=["Delete"])
def delete_meal(id):
    query = models.Meal.delete().where(models.Meal.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})