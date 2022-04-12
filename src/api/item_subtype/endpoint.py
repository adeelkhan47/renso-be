from datetime import datetime

from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.booking import Booking
from model.day_picker import DayPicker
from model.item_subtype import ItemSubType
from model.item_type import ItemType
from model.location import Location
from . import api, schema


@api.route("")
class item_sub_types_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseItem_Subtype)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = g.current_user.id
        all_items, count = ItemSubType.filtration(args)
        return response_structure(all_items, count), 200

    @api.expect(schema.Item_subtype_Expect)
    @api.marshal_with(schema.get_by_id_responseItem_Subtype)
    @auth
    def post(self):
        payload = api.payload
        name = payload.get("name")
        image = payload.get("image")
        price = payload.get("price")
        item_type_id = payload.get("item_type_id")
        person = payload.get("person")
        item_subtype = ItemSubType(name, price, person, item_type_id, image, g.current_user.id)
        item_subtype.insert()

        return response_structure(item_subtype), 201


@api.route("/<int:item_subtype_id>")
class item_subtype_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseItem_Subtype)
    @auth
    def get(self, item_subtype_id):
        itemSubType = ItemSubType.query_by_id(item_subtype_id)
        return response_structure(itemSubType), 200

    @api.doc("Delete ItemSubType by id")
    @auth
    def delete(self, item_subtype_id):
        ItemSubType.delete(item_subtype_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseItem_Subtype)
    @api.expect(schema.Item_subtype_Expect)
    @auth
    def patch(self, item_subtype_id):
        payload = api.payload
        data = payload.copy()
        ItemSubType.update(item_subtype_id, data)
        itemSubType = ItemSubType.query_by_id(item_subtype_id)
        return response_structure(itemSubType), 200


@api.route("/by_item_id/<int:item_type_id>")
class item_subtype_by_item_typeid(Resource):
    @api.marshal_list_with(schema.get_list_responseItem_Subtype)
    @auth
    def get(self, item_type_id):
        itemSubType = ItemSubType.get_by_item_type_id(item_type_id)
        return response_structure(itemSubType, len(itemSubType)), 200


@api.route("/available")
class items_subtype_list(Resource):
    @api.doc("Get all items with date filter")
    @api.marshal_list_with(schema.get_list_Availability_responseItem_Subtype_)
    @api.param("start_time", required=True)
    @api.param("end_time", required=True)
    @api.param("item_type_id", required=True)
    @api.param("location_id", required=True)
    @auth
    def get(self):
        args = request.args
        start_time = datetime.strptime(args["start_time"], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(args["end_time"], '%Y-%m-%d %H:%M:%S')
        item_sub_types = ItemType.query_by_id(args["item_type_id"]).item_sub_type
        location = Location.query_by_id(args["location_id"])
        response_data = []
        for each in item_sub_types:
            data = {"item_sub_type_object": each}
            list_of_ids = []
            for item in each.items:
                if item.item_status.name == "Available":
                    if location in [loc.location for loc in item.item_locations]:
                        found = False
                        for each_booking in Booking.get_bookings_by_item_id(item.id):
                            if each_booking.start_time <= end_time and start_time <= each_booking.end_time:
                                found = True
                                break
                        if not found:
                            list_of_ids.append(item.id)
            data["available_item_ids"] = list_of_ids
            response_data.append(data)
        return response_structure(response_data, len(response_data)), 200
