from datetime import datetime

from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure, error_message
from decorator.authorization import auth
from model.booking import Booking
from model.item_subtype import ItemSubType
from model.item_type import ItemType
from model.location import Location
from model.restricted_dates import RestrictedDates
from . import api, schema


@api.route("")
class item_sub_types_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseItem_Subtype)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
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
        company_id = payload.get("company_id")
        person = payload.get("person")
        least_price = payload.get("least_price")
        discount_after_higher_price = payload.get("discount_after_higher_price")
        same_price_days = payload.get("same_price_days")
        description = payload.get("description")
        show_description = payload.get("show_description")
        item_subtype = ItemSubType(name, price, person, item_type_id, image, g.current_user.id, least_price,
                                   discount_after_higher_price, same_price_days, show_description, description,
                                   company_id)
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


@api.route("/extra_by_item_type_id/<int:item_type_id>")
class item_subtype_extra_by_item_type_id(Resource):
    @api.marshal_list_with(schema.get_list_responseItem_Subtype)
    @auth
    def get(self, item_type_id):
        itemType = ItemType.query_by_id(item_type_id)
        extra_sub_types = []
        for each in itemType.itemTypeExtras:
            extra_sub_types.append(each.item_subtype)
        return response_structure(extra_sub_types, len(extra_sub_types)), 200


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
        # VALIDATE RESTRICTED DATES
        start_date = start_time.date()
        end_date = end_time.date()
        first = RestrictedDates.validate_booking_date(args["item_type_id"], start_date)
        second = RestrictedDates.validate_booking_date(args["item_type_id"], end_date)
        if not first or not second:
            return error_message("This Item_type is not available on these dates Temporary."), 400
        #
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


@api.route("/extra_available")
class items_extrasubtype_list(Resource):
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
        item_sub_types = ItemType.query_by_id(args["item_type_id"]).itemTypeExtras
        item_sub_types = [x.item_subtype for x in item_sub_types]
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
