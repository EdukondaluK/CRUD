import json

from flask import jsonify, Blueprint, request, current_app
from models.location import Location
from db.postgres import db
from flask_json_schema import JsonSchema
from flask_cors import cross_origin
from sqlalchemy import Sequence
import pdb
location_api = Blueprint('location_api', __name__)
location_api.config = {}
schema = JsonSchema(location_api)

@location_api.route("/api/v1/location", methods=['POST'])
@cross_origin("*")
def create():

    try:
        input_json_data = request.get_json()
        if not input_json_data:
            return {"message": "No input data provided"}, 400
        new_location = input_json_data['location']
        new_department = input_json_data['department']
        location_results = Location.query.filter(Location.location == new_location)
    #   validation of location
        for temp in location_results:
            string_val = temp.serialize()
            if (new_location == string_val.get('location') and new_department == string_val.get('department')):
                data = {'Inserting Data': 'Failure', 'Error': "Location and Department have been already exists"}
                resp = jsonify(data), 205
                return resp

        db.create_all()
        db.session.commit()
    #   assign new location details to Location model
        location = Location(location=input_json_data['location'],
                            department=input_json_data['department'],
                            location_id=Sequence('user_id_seq').next_value())
        db.session.add(location)
        db.session.commit()
        data = {'create': 'success', 'location_id': location.location_id}
        resp = jsonify(data), 201
    except Exception as e:
        data = {'create': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp

@location_api.route("/api/v1/location", methods=['GET'])
@cross_origin(origin="*")
def view():
    try:
        location_all = Location.query.filter()
        if location_all is None:
            data = {'info': 'No location data available in database'}
            return jsonify(data), 422
        results=[]
        for temp in location_all:
            string_val = temp.serialize()
            results.append(string_val)
        data = {"Locations": results}
    except Exception as e:
        print(e)
    return current_app.response_class(json.dumps(data), mimetype="application/json")


@location_api.route("/api/v1/location/<location_id>", methods=['GET'])
@cross_origin(origin="*")
def locationids(location_id):
    try:
        if location_id is None:
            data = {'info': 'location id is required parameter'}
            return jsonify(data), 422
        location_all = Location.query.filter(Location.location_id == location_id)
        results = []
        for temp in location_all:
            string_val = temp.serialize()
            results.append(string_val)
        data = {"Location": results}
    except Exception as e:
        print("----error---",e)
    if len(data.get("Location")) == 0:
        data["Location"] = ["Location id is not available in the database"]

    return current_app.response_class(json.dumps(data), mimetype="application/json")


@location_api.route("/api/v1/location", methods=['PUT'])
@cross_origin(origin="*")
def update():
    pdb.set_trace()
    try:
        input_json_data = request.get_json()
        old_location = input_json_data["location"]
        new_location = input_json_data["location"]
        if not input_json_data:
            return {"message": "No input data provided"}, 400

        # Getting location details with old location and replacing with new value

        location_model = Location.query.filter(Location.location == old_location.first())
        location_model.location = new_location
        if old_location.upper() == new_location.upper():
            data = {'updating': old_location + "  same as " + new_location}
            resp = jsonify(data), 205
            return resp

        db.session.flush()
        db.session.commit()
        data = {'updated': new_location + "  with  " + old_location + "  in location model "}
        resp = jsonify(data), 200

    except Exception as e:
        data = {'update': 'fail'}
        resp = jsonify(data), 500
        print(e)
    return resp
