import json

from flask import jsonify, Blueprint, request, current_app
from db.postgres import db
from flask_cors import cross_origin
from sqlalchemy import Sequence
from flask_json_schema import JsonSchema
from models.department import Department
from models.location import Location
from models.category import Category
from models.sub_category import Subcategory
import pdb
category_api = Blueprint('category_api', __name__)
category_api.config = {}
schema = JsonSchema(category_api)


@category_api.route("/api/v1/category", methods=['POST'])
@cross_origin("*")
def create():

    try:
        input_json_data = request.get_json()
        db.create_all()
        db.session.commit()
        if not input_json_data:
            return {"message": "No input data provided"}, 400
        new_category = input_json_data['category']
        new_subcategory = input_json_data['subcategory']
        category_results = Category.query.filter(Category.category == new_category)
        # validation of category details
        for temp in category_results:
            string_val = temp.serialize()
            if (new_subcategory == string_val.get('sub_category')) and (new_category == string_val.get('category')):
                data = {'Inserting Data': 'Failure', 'Error': "Category and Sub category have been already exists"}
                resp = jsonify(data), 205
                return resp
        category = Category(category=input_json_data['category'],
                            category_id=Sequence('user_id_seq').next_value(),
                            subcategory=input_json_data['subcategory'],
                            details=input_json_data['details'])
        db.session.add(category)
        db.session.commit()
        data = {'create': 'success', 'category_id': category.category_id}
        resp = jsonify(data), 201
    except Exception as e:
        data = {'create': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp


@category_api.route("/api/v1/location/<location_id>/department/<department_id>/category", methods=['GET'])
@cross_origin(origin="*")
def category(location_id,department_id):
    try:

        if (location_id is None) and (department_id is None):
            data = {'info': 'location and department ids are required parameter'}
            return jsonify(data), 422
        location_all = Location.query.filter(Location.location_id == location_id)
        departments_results = []
        category_results = []
        results = []
        # Joining of location and department models with department column
        # Joining of department and category models with category column
        for temp in location_all:
            string_val = temp.serialize()
            departments_results.append(string_val.get('department'))
        for query_depart in departments_results:
            department_all = Department.query.filter(Department.department == query_depart)
            for temp in department_all:
                string_val = temp.serialize()
                category_results.append(string_val.get('category'))
        for query_category in category_results:
            category_all = Category.query.filter(Category.category == query_category)
            for temp in category_all:
                string_val = temp.serialize()
                results.append(string_val)
        data = {"Categories": results}
    except Exception as e:
        print("----error---",e)
    if len(data.get("Categories")) == 0:
        data["Categories"] = ["Category is not available in the database"]
    return current_app.response_class(json.dumps(data), mimetype="application/json")


@category_api.route("/api/v1/location/<location_id>/department/<department_id>"
                    "/category/<category_id>", methods=['GET'])
@cross_origin(origin="*")
def categoryid(location_id,department_id,category_id):
    try:

        if (location_id is None) and (department_id is None) and (category_id is None):
            data = {'info': 'location , department and category  ids are required parameter'}
            return jsonify(data), 422
        location_all = Location.query.filter(Location.location_id == location_id)
        department_results = []
        category_results = []
        results = []
        # Joining location and department model with column department
        # more drill down level of data with department id condition
        # again more drill down level with category id condition
        for temp in location_all:
            string_val = temp.serialize()
            department_results.append(string_val.get('department'))

        for depart_query in department_results:
            department_all = Department.query.filter(Department.department == depart_query,
                                                     Department.department_id == department_id)
            for temp in department_all:
                string_val = temp.serialize()
                category_results.append(string_val.get('category'))

        for category_query in category_results:
            category_all = Category.query.filter(Category.category == category_query,
                                                 Category.category_id == category_id)
            for temp in category_all:
                string_val = temp.serialize()
                results.append(string_val)

        data = {"Category": results}

    except Exception as e:
        print("----error---",e)
    if len(data.get("Category")) == 0:
        data["Category"] = ["Category id is not available in the database"]

    return current_app.response_class(json.dumps(data), mimetype="application/json")

@category_api.route("/api/v1/category", methods=['PUT'])
@cross_origin(origin="*")
def update():
    pdb.set_trace()
    try:
        input_json_data = request.get_json()
        old_category = input_json_data["category"]
        new_category = input_json_data["new_category"]
        if not input_json_data:
            return {"message": "No input data provided"}, 400

        # Getting category details with old category and replacing with new value

        category_model = Category.query.filter(Category.category == old_category).first()
        category_model.category = new_category
        if old_category.upper() == new_category.upper():
            data = {'updating': old_category + "  same as " + new_category}
            resp = jsonify(data), 205
            return resp

        # Getting category details with old category and replacing with new value

        subcategory_model = Subcategory.query.filter(Subcategory.category == old_category).first()
        subcategory_model.category = new_category

        # Getting category details with old category and replacing with new value

        department_model = Department.query.filter(Department.category == old_category).first()
        department_model.category = new_category

        db.session.flush()
        db.session.commit()
        data = {'updated': old_category + "  with  " + new_category + "  in category,department && subcategory models "}
        resp = jsonify(data), 200

    except Exception as e:
        data = {'update': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp

@category_api.route("/api/v1/category", methods=['DELETE'])
@cross_origin(origin="*")
def delete():
    pdb.set_trace()
    try:
        input_json_data = request.get_json()
        del_category = input_json_data["category"]

        if not input_json_data:
            return {"message": "No input data provided"}, 400

        # Getting category details with old category and replacing with new value

        categoryFlag = bool(Category.query.filter(Category.category == del_category).first())
        if not categoryFlag:
            data = {'deleting': del_category + "  is not available in category model"}
            resp = jsonify(data), 205
            return resp

        category_model = Category.query.filter(Category.category == del_category).first()
        del_subcategory = category_model.subcategory
        subcategoryFlag = bool(Subcategory.query.filter(Subcategory.subcategory == del_subcategory).first())

        results=[]
        if subcategoryFlag:
            subcategory_all = Subcategory.query.filter(Subcategory.subcategory == del_subcategory)
            for temp in subcategory_all:
                string_val = temp.serialize()
                results.append(string_val.get('subcategory'))
            data = {"Please delete child subcategories ": results}
            resp = jsonify(data),205
            return resp
        else:
            db.session.delete(category_model)
        db.session.flush()
        db.session.commit()
        data = {'Deleted': del_category + "  in category model "}
        resp = jsonify(data), 200

    except Exception as e:
        data = {'delete': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp