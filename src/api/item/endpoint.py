from datetime import datetime

from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.booking import Booking
from model.item import Item
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

    @api.param("name", required=True)
    @api.param("image", required=True)
    @api.param("tag_ids")
    @api.param("description", required=True)
    @api.param("price", required=True)
    @api.param("item_status_id", required=True)
    @api.param("person", required=True, type=int)
    @api.param("item_type_id", required=True)
    @api.param("tag_ids")
    def post(self):
        name = request.json.get("name")
        image = request.json.get("image")
        description = request.json.get("description")
        price = request.json.get("price")
        item_status_id = request.json.get("item_status_id")
        person = request.json.get("person")
        item_type_id = request.json.get("item_type_id")
        item = Item(name, image, description, price, item_status_id, person, item_type_id)
        item.insert()
        if "tag_ids" in request.args.keys():
            tag_ids = request.args.get("tag_ids").split(",")
            for each in tag_ids:
                ItemTag(item_id=item.id, tag_id=each).insert()
        return "ok", 201


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
    @api.param("name")
    @api.param("image")
    @api.param("tag_ids")
    @api.param("description")
    @api.param("price")
    @api.param("item_status_id")
    @api.param("person", type=int)
    @api.param("item_type_id")
    @api.param("tag_ids")
    def patch(self, item_id):
        data = api.payload.copy()
        if "tag_ids" in data.keys():
            ItemTag.delete_by_item_id(item_id)
            tag_ids = data.get("tag_ids").split(",")
            for each in tag_ids:
                ItemTag(item_id=item_id, tag_id=each).insert()
            del data["tag_ids"]
        Item.update(item_id, data)
        item = Item.query_by_id(item_id)
        return response_structure(item), 200
