from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.date_picker import DatePicker
from . import api, schema


@api.route("")
class Date_Picker_lList(Resource):
    @api.doc("Get all Date Pickers")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_rows, count = DatePicker.filtration(args)
        return response_structure(all_rows, count), 200

    @api.param("allowed_days", required=True)
    @api.param("not_allowed_days", required=True)
    def post(self):
        allowed_days = request.args.get("allowed_days")
        not_allowed_days = request.args.get("not_allowed_days")

        date_picker = DatePicker(allowed_days, not_allowed_days)
        date_picker.insert()
        return "ok", 201


@api.route("/<int:date_picker_id>")
class date_picker_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, date_picker_id):
        widget = DatePicker.query_by_id(date_picker_id)
        return response_structure(widget), 200

    @api.doc("Delete Date Picker by id")
    def delete(self, date_picker_id):
        DatePicker.delete(date_picker_id)
        return "ok", 200
