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
    @api.expect(schema.Day_Picker_Expect)
    def post(self):
        args = api.payload
        monday = args["monday"]
        tuesday = args["tuesday"]
        wednesday = args["wednesday"]
        thursday = args["thursday"]
        friday = args["friday"]
        saturday = args["saturday"]
        sunday = args["sunday"]
        item_type_id = args["item_type_id"]
        item_subtype_id = args["item_subtype_id"]
        if ItemType.query_by_id(item_type_id):
            day_picker = DayPicker(monday, tuesday, wednesday, thursday, friday, saturday, sunday, item_type_id,
                                   item_subtype_id)
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
    @api.expect(schema.Day_Picker_Expect)
    def patch(self, day_picker_id):
        args = api.payload
        data = {}
        data["monday"] = args["monday"]
        data["tuesday"] = args["tuesday"]
        data["wednesday"] = args["wednesday"]
        data["thursday"] = args["thursday"]
        data["friday"] = args["friday"]
        data["saturday"] = args["saturday"]
        data["sunday"] = args["sunday"]
        data["item_type_id"] = args["item_type_id"]

        if ItemType.query_by_id(data["item_type_id"]):
            DayPicker.update(day_picker_id, data)

            return response_structure(DayPicker.query_by_id(day_picker_id)), 201
        else:
            raise NotFound("item_type_id not exist")
