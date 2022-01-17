from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from model.day_picker import DayPicker
from model.item_type import ItemType
from . import api, schema


@api.route("")
class DayPickerList(Resource):
    @api.doc("Get all Date Pickers")
    @api.marshal_list_with(schema.get_list_responseDay_Picker)
    def get(self):
        args = request.args
        all_rows, count = DayPicker.filtration(args)
        return response_structure(all_rows, count), 200

    @api.marshal_list_with(schema.get_by_id_responseDay_Picker)
    @api.param("monday", required=True, type=int)
    @api.param("tuesday", required=True, type=int)
    @api.param("wednesday", required=True, type=int)
    @api.param("thursday", required=True, type=int)
    @api.param("friday", required=True, type=int)
    @api.param("saturday", required=True, type=int)
    @api.param("sunday", required=True, type=int)
    @api.param("item_type_id", required=True, type=int)
    def post(self):
        args = api.payload
        monday = int(args["monday"])
        tuesday = int(args["tuesday"])
        wednesday = int(args["wednesday"])
        thursday = int(args["thursday"])
        friday = int(args["friday"])
        saturday = int(args["saturday"])
        sunday = int(args["sunday"])
        item_type_id = int(args["item_type_id"])
        if ItemType.query_by_id(item_type_id):
            day_picker = DayPicker(monday, tuesday, wednesday, thursday, friday, saturday, sunday, item_type_id)
            day_picker.insert()
            return response_structure(DayPicker.query_by_id(day_picker.id)), 201
        else:
            return "item_type_id not exist", 404


@api.route("/<int:day_picker_id>")
class day_picker_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseDay_Picker)
    def get(self, day_picker_id):
        widget = DayPicker.query_by_id(day_picker_id)
        return response_structure(widget), 200

    @api.doc("Delete Date Picker by id")
    def delete(self, day_picker_id):
        DayPicker.delete(day_picker_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseDay_Picker, skip_none=True)
    @api.param("monday", required=True, type=int)
    @api.param("tuesday", required=True, type=int)
    @api.param("wednesday", required=True, type=int)
    @api.param("thursday", required=True, type=int)
    @api.param("friday", required=True, type=int)
    @api.param("saturday", required=True, type=int)
    @api.param("sunday", required=True, type=int)
    @api.param("item_type_id", required=True, type=int)
    def patch(self, day_picker_id):
        args = api.payload
        data = {}
        data["monday"] = int(args["monday"])
        data["tuesday"] = int(args["tuesday"])
        data["wednesday"] = int(args["wednesday"])
        data["thursday"] = int(args["thursday"])
        data["friday"] = int(args["friday"])
        data["saturday"] = int(args["saturday"])
        data["sunday"] = int(args["sunday"])
        data["item_type_id"] = int(args["item_type_id"])

        if ItemType.query_by_id(data["item_type_id"]):
            DayPicker.update(day_picker_id, data)

            return response_structure(DayPicker.query_by_id(day_picker_id)), 201
        else:
            raise NotFound("item_type_id not exist")
