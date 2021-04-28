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
sub_category_api = Blueprint('sub_category_api', __name__)
sub_category_api.config = {}
schema = JsonSchema(sub_category_api)


@sub_category_api.route("/api/v1/subcategory", methods=['POST'])
@cross_origin("*")
def create():

    try:
        input_json_data = request.get_json()

        db.create_all()
        db.session.commit()
        if not input_json_data:
            return {"message": "No input data provided"}, 400
        subcategory_1 = input_json_data['subcategory']
        category_1 = input_json_data['category']
        subcategory_results = Subcategory.query.filter(Subcategory.subcategory == subcategory_1)
        # validation subcategory details
        for temp in subcategory_results:
            string_val = temp.serialize()
            if (subcategory_1 == string_val.get('subcategory') and category_1 == string_val.get('category')):
                data = {'Inserting Data': 'Failure', 'Error': "Subcategory and Category have been already exists"}
                resp = jsonify(data), 205
                return resp
        subcategory = Subcategory(subcategory=input_json_data['subcategory'],
                                  subcategory_id=Sequence('user_id_seq').next_value(),
                                  category=input_json_data['category'],
                                  details=input_json_data['details'])
        db.session.add(subcategory)
        db.session.commit()
        data = {'create': 'success', 'subcategory_id': subcategory.subcategory_id}
        resp = jsonify(data), 201
    except Exception as e:
        data = {'create': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp
@sub_category_api.route("/api/v1/location/<location_id>/department/<department_id>/category"
                        "/<category_id>/subcategory", methods=['GET'])
@cross_origin(origin="*")
def subcategory(location_id,department_id,category_id):
    try:


        if (location_id is None) and (department_id is None) and (category_id is None):
            data = {'info': 'location, department and category ids are required parameter'}
            return jsonify(data), 422
        location_all = Location.query.filter(Location.location_id == location_id)
        departments_results = []
        category_results = []
        subcategory_results = []
        results = []
        # Joining of location and department models with department column
        # Joining of department and category models with category column
        # Joining of category and sub category models with subcategory column
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
                subcategory_results.append(string_val.get('subcategory'))
        for query_subcategory in subcategory_results:
            subcategory_all = Subcategory.query.filter(Subcategory.subcategory == query_subcategory)
            for temp in subcategory_all:
                string_val = temp.serialize()
                results.append(string_val)
        data = {"Subcategories": results}
    except Exception as e:
        print("----error---",e)
    if len(data.get("Subcategories")) == 0:
        data["Subcategories"] = ["Category is not available in the database"]
    return current_app.response_class(json.dumps(data), mimetype="application/json")


@sub_category_api.route("/api/v1/location/<location_id>/department/<department_id>"
                        "/category/<category_id>/subcategory/<subcategory_id>", methods=['GET'])
@cross_origin(origin="*")
def subcategoryid(location_id,department_id,category_id,subcategory_id):
    try:

        if (location_id is None) and (department_id is None) \
                and (category_id is None) and (subcategory_id is None):
            data = {'info': 'location , department ,category and subcategory ids are required parameter'}
            return jsonify(data), 422
        location_all = Location.query.filter(Location.location_id == location_id)
        department_results = []
        category_results = []
        subcategory_results = []
        results = []
        # Joining location and department model with column department
        # more drill down level of data with department id condition
        # again more drill down level with category id condition
        # again more drill down level with sub category id condition
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
                subcategory_results.append(string_val.get('subcategory'))

        for subcategory_query in subcategory_results:
            subcategory_all = Subcategory.query.filter(Subcategory.subcategory == subcategory_query,
                                                       Subcategory.subcategory_id == subcategory_id)
            for temp in subcategory_all:
                string_val = temp.serialize()
                results.append(string_val)

        data = {"Subcategory": results}

    except Exception as e:
        print("----error---",e)
    if len(data.get("Subcategory")) == 0:
        data["Subcategory"] = ["Category id is not available in the database"]

    return current_app.response_class(json.dumps(data), mimetype="application/json")


@sub_category_api.route("/api/v1/subcategory", methods=['PUT'])
@cross_origin(origin="*")
def update():
    pdb.set_trace()
    try:
        input_json_data = request.get_json()
        old_subcategory = input_json_data["subcategory"]
        new_subcategory = input_json_data["new_subcategory"]
        if not input_json_data:
            return {"message": "No input data provided"}, 400

        # Getting subcategory details with old subcategory and replacing with new value

        subcategory_model = Subcategory.query.filter(Subcategory.subcategory == old_subcategory).first()
        subcategory_model.subcategory = new_subcategory
        if old_subcategory.upper() == new_subcategory.upper():
            data = {'updating': old_subcategory + "  same as " + new_subcategory}
            resp = jsonify(data), 205
            return resp

        # Getting category details with old subcategory and replacing with new value

        category_model = Category.query.filter(Category.subcategory == old_subcategory).first()
        category_model.subcategory = new_subcategory
        db.session.flush()
        db.session.commit()
        data = {'updated': old_subcategory + "  with  " + new_subcategory + "  in category && subcategory models "}
        resp = jsonify(data), 200

    except Exception as e:
        data = {'update': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp

@sub_category_api.route("/api/v1/subcategory", methods=['DELETE'])
@cross_origin(origin="*")
def delete():
    pdb.set_trace()
    try:
        input_json_data = request.get_json()
        del_subcategory = input_json_data["subcategory"]
        if not input_json_data:
            return {"message": "No input data provided"}, 400

        # Validation of subcategory
        subcategoryFlag = bool(Subcategory.query.filter_by(subcategory=del_subcategory).first())

        if not subcategoryFlag:
            data = {'Delete Object': del_subcategory + " is not available in subcategory model "}
            resp = jsonify(data), 205
            return resp
        #  Getting delete subcategory details and deleting row
        subcategory_model = Subcategory.query.filter(Subcategory.subcategory == del_subcategory).first()
        db.session.delete(subcategory_model)
        db.session.commit()
        data = {'deleted': del_subcategory + " in subcategory model "}
        resp = jsonify(data), 200

    except Exception as e:
        data = {'delete': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp