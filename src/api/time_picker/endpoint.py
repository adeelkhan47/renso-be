from flask import g
from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from decorator.authorization import auth
from model.day_picker import DayPicker
from model.time_picker import TimePicker
from . import api, schema


@api.route("")
class TimePickerList(Resource):
    @api.doc("Get all Time Pickers")
    @api.marshal_list_with(schema.get_list_responseTime_Picker)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        args["is_deleted:eq"] = "False"
        all_rows, count = TimePicker.filtration(args)
        return response_structure(all_rows, count), 200

    @api.marshal_list_with(schema.get_by_id_responseTime_Picker)
    @api.expect(schema.Time_Picker_expect)
    @auth
    def post(self):
        args = api.payload
        start_time = args["start_time"]
        end_time = args["end_time"]
        day = args["day"]
        day_picker_id = int(args["day_picker_id"])
        if DayPicker.query_by_id(day_picker_id):
            time_picker = TimePicker(start_time, end_time, day, day_picker_id, g.current_user.id)
            time_picker.insert()
            return response_structure(TimePicker.query_by_id(time_picker.id)), 201
        else:
            raise NotFound("day_picker_id not exist")


@api.route("/<int:time_picker_id>")
class picker_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseTime_Picker)
    @auth
    def get(self, time_picker_id):
        widget = TimePicker.query_by_id(time_picker_id)
        return response_structure(widget), 200

    @api.doc("Delete time Picker by id")
    @auth
    def delete(self, time_picker_id):
        TimePicker.soft_delete(time_picker_id)
        return "ok", 204
