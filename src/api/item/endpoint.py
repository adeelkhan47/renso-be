from datetime import datetime

from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.booking import Booking
from model.item import Item
from model.item_location import ItemLocation
from model.item_tag import ItemTag
from . import api, schema


@api.route("/available")
class items_list(Resource):
    @api.doc("Get all items with date filter")
    @api.marshal_list_with(schema.get_list_responseItem)
    @api.param("start_time", required=True)
    @api.param("end_time", required=True)
    def get(self):
        args = request.args
        start_time = datetime.strptime(args["start_time"], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(args["end_time"], '%Y-%m-%d %H:%M:%S')
        available_items_ids = []
        for item in Item.get_all_active_items():
            for each in Booking.get_bookings_by_item_id(item.id):
                if not (each.start_time <= end_time and start_time <= each.end_time):
                    available_items_ids.append(str(item.id))
        if available_items_ids:
            new_args = {"id:eq": ",".join(available_items_ids)}
            all_items, count = Item.filtration(new_args)
            return response_structure(all_items, count), 200
        return response_structure([], 0), 200


@api.route("")
class items_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseItem)
    def get(self):
        args = request.args
        all_items, count = Item.filtration(args)
        return response_structure(all_items, count), 200

    @api.marshal_list_with(schema.get_by_id_responseItem, skip_none=True)
    @api.expect(schema.ItemExpect, validate=True)
    def post(self):

        name = request.json.get("name")
        image = request.json.get("image")
        description = request.json.get("description")
        item_status_id = request.json.get("item_status_id")
        item_type_id = request.json.get("item_type_id")
        item_subtype_id = request.json.get("item_subtype_id")
        item = Item(name, image, description, item_status_id, item_type_id, item_subtype_id)
        item.insert()
        if "tag_ids" in request.json.keys():
            if request.json.get("tag_ids") != "":
                tag_ids = request.json.get("tag_ids").split(",")
                for each in tag_ids:
                    ItemTag(item_id=item.id, tag_id=each).insert()
        if "location_ids" in request.json.keys():
            if request.json.get("location_ids") != "":
                location_ids = request.json.get("location_ids").split(",")
                for each in location_ids:
                    ItemLocation(item_id=item.id, location_id=each).insert()
        return response_structure(item), 201


@api.route("/<int:item_id>")
class item_by_id(Resource):
    @api.doc("Get all accounts")
    @api.marshal_list_with(schema.get_by_id_responseItem)
    def get(self, item_id):
        item = Item.query_by_id(item_id)
        return response_structure(item), 200

    @api.doc("Delete item by id")
    def delete(self, item_id):
        Item.delete(item_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseItem, skip_none=True)
    @api.expect(schema.ItemExpect)
    def patch(self, item_id):
        data = api.payload.copy()
        if "tag_ids" in data.keys():
            ItemTag.delete_by_item_id(item_id)
            tag_ids = data.get("tag_ids").split(",")
            for each in tag_ids:
                ItemTag(item_id=item_id, tag_id=each).insert()
            del data["tag_ids"]
        if "location_ids" in data.keys():
            ItemLocation.delete_by_item_id(item_id)
            location_ids = data.get("location_ids").split(",")
            for each in location_ids:
                ItemLocation(item_id=item_id, location_id=each)
            del data["location_ids"]
        Item.update(item_id, data)
        item = Item.query_by_id(item_id)
        return response_structure(item), 200
