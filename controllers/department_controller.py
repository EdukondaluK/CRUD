import json

from flask import jsonify, Blueprint, request, current_app
from db.postgres import db
from flask_cors import cross_origin
from sqlalchemy import Sequence
from flask_json_schema import JsonSchema
from models.department import Department
from models.location import Location
from models.category import Category
import pdb
department_api = Blueprint('department_api', __name__)
department_api.config = {}
schema = JsonSchema(department_api)

@department_api.route("/api/v1/department", methods=['POST'])
@cross_origin("*")
def create():

    try:
        input_json_data = request.get_json()
        db.create_all()
        db.session.commit()
        if not input_json_data:
            return {"message": "No input data provided"}, 400
        new_category = input_json_data['category']
        new_department = input_json_data['department']
        department_results = Department.query.filter(Department.department == new_department)
        #   validation of department details
        for temp in department_results:
            string_val = temp.serialize()
            if (new_department == string_val.get('department')) and (new_category == string_val.get('category')):
                data = {'Inserting Data': 'Failure', 'Error': "Department and Category have been already exists"}
                resp = jsonify(data), 205
                return resp

        #   assign department details to Department model
        department = Department(department=input_json_data['department'],
                                department_id=Sequence('user_id_seq').next_value(),
                                category=input_json_data['category'],
                                details=input_json_data['details'])
        db.session.add(department)
        db.session.commit()
        data = {'create': 'success', 'department_id': department.department_id}
        resp = jsonify(data), 201
    except Exception as e:
        data = {'create': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp


@department_api.route("/api/v1/location/<location_id>/department", methods=['GET'])
@cross_origin(origin="*")
def department(location_id):
    try:

        if location_id is None:
            data = {'info': 'location id is required parameter'}
            return jsonify(data), 422
        location_all = Location.query.filter(Location.location_id == location_id)
        departments_results = []
        results = []
        # Joining of location and department models with department column
        for temp in location_all:
            string_val = temp.serialize()
            departments_results.append(string_val.get('department'))
        for query_depart in departments_results:
            department_all = Department.query.filter(Department.department == query_depart)
            for temp in department_all:
                string_val = temp.serialize()
                results.append(string_val)
        data = {"Departments": results}
    except Exception as e:
        print("----error---",e)
    if len(data.get("Departments")) == 0:
        data["Departments"] = ["Department is not available in the database"]
    return current_app.response_class(json.dumps(data), mimetype="application/json")


@department_api.route("/api/v1/location/<location_id>/department/<department_id>", methods=['GET'])
@cross_origin(origin="*")
def departmentids(location_id,department_id):
    try:

        if (location_id is None) and (department_id is None):
            data = {'info': 'location and department ids are required parameter'}
            return jsonify(data), 422
        location_all = Location.query.filter(Location.location_id == location_id)
        department_results = []
        results = []
        # Joining location and department model with column department
        # more drill down level of data with department id condition
        for temp in location_all:
            string_val = temp.serialize()
            department_results.append(string_val.get('department'))
        for depart_query in department_results:
            department_all = Department.query.filter(Department.department == depart_query,
                                                     Department.department_id == department_id)
            for temp in department_all:
                string_val = temp.serialize()
                results.append(string_val)

        data = {"Department": results}

    except Exception as e:
        print("----error---",e)
    if len(data.get("Department")) == 0:
        data["Department"] = ["Department id is not available in the database"]

    return current_app.response_class(json.dumps(data), mimetype="application/json")

@department_api.route("/api/v1/department", methods=['PUT'])
@cross_origin(origin="*")
def update():
    pdb.set_trace()
    try:
        input_json_data = request.get_json()
        old_department = input_json_data["department"]
        new_department = input_json_data["department"]
        if not input_json_data:
            return {"message": "No input data provided"}, 400

        # Getting department details with old department and replacing with new value

        department_model = Department.query.filter(Department.department == old_department.first())
        department_model.department = new_department
        if old_department.upper() == new_department.upper():
            data = {'updating': old_department + "  same as " + new_department}
            resp = jsonify(data), 205
            return resp

        # Getting department details with old department and replacing with new value

        location_model = Location.query.filter(Location.department == old_department).first()
        location_model.department = new_department

        db.session.flush()
        db.session.commit()
        data = {'updated': new_department + "  with  " + old_department + "  in category,department && subcategory models "}
        resp = jsonify(data), 200

    except Exception as e:
        data = {'update': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp

@department_api.route("/api/v1/department", methods=['DELETE'])
@cross_origin(origin="*")
def delete():
    pdb.set_trace()
    try:
        input_json_data = request.get_json()
        del_department = input_json_data["department"]

        if not input_json_data:
            return {"message": "No input data provided"}, 400

        # Getting category details with old category and replacing with new value

        departmentFlag = bool(Department.query.filter(Department.department == del_department).first())
        if not departmentFlag:
            data = {'deleting': del_department + "  is not available in category model"}
            resp = jsonify(data), 205
            return resp

        department_model = Department.query.filter(Department.department == del_department).first()
        del_category = department_model.category
        categoryFlag = bool(Category.query.filter(Category.category == del_category).first())

        results=[]
        if categoryFlag:
            category_all = Category.query.filter(Category.category == del_category)
            for temp in category_all:
                string_val = temp.serialize()
                results.append(string_val.get('category'))
            data = {"Please delete child categories ": results}
            resp = jsonify(data),205
            return resp
        else:
            db.session.delete(department_model)
        db.session.flush()
        db.session.commit()
        data = {'Deleted': del_department + "  in department model "}
        resp = jsonify(data), 200

    except Exception as e:
        data = {'delete': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp