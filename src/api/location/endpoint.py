from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.location import Location
from . import api, schema


@api.route("")
class LocationList(Resource):
    @api.doc("Get all location")
    @api.marshal_list_with(schema.get_list_responseLocation)
    def get(self):
        args = request.args
        all_rows, count = Location.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.location_Expect)
    @api.marshal_list_with(schema.get_by_id_responseLocation, skip_none=True)
    def post(self):
        payload = api.payload
        location = Location(**payload)
        location.insert()
        return response_structure(location), 201


@api.route("/<int:location_id>")
class LocationbyId(Resource):
    @api.doc("Get location by id")
    @api.marshal_list_with(schema.get_by_id_responseLocation, skip_none=True)
    def get(self, location_id):
        location = Location.query_by_id(location_id)
        return response_structure(location), 200

    @api.doc("Delete method by id")
    def delete(self, location_id):
        Location.delete(location_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseLocation,skip_none=True)
    @api.expect(schema.location_Expect)
    def patch(self, location_id):
        payload = api.payload
        Location.update(location_id, payload)
        location = Location.query_by_id(location_id)
        return response_structure(location), 200
