from datetime import datetime

from flask import g
from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.booking import Booking
from model.item import Item
from model.item_location import ItemLocation
from model.item_status import ItemStatus
from model.item_subtype import ItemSubType
from model.item_tag import ItemTag
from . import api, schema


@api.route("/filter_location")
class items_list_locationFilter(Resource):
    @api.doc("Get all filtered items")
    @api.marshal_list_with(schema.get_list_responseItem)
    @api.param("item_subtype_id")
    @api.param("location_ids")
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        if ("item_subtype_id" in args.keys() and args["item_subtype_id"]) and (
                "location_ids" in args.keys() and args["location_ids"]) and (
        ItemSubType.query_by_id(args["item_subtype_id"])):
            dummy_args = {'item_subtype_id:eq': args["item_subtype_id"]}
            location_ids = [int(x) for x in args["location_ids"].split(",")]
            all_items, total = Item.filtration(dummy_args)
            required_items_id = []
            for each in all_items:
                for item_location in each.item_locations:
                    if item_location.location.id in location_ids:
                        required_items_id.append(each.id)
                        break
            all_filtered_id = ','.join((str(n) for n in required_items_id))
            del args["location_ids"]
            del args["item_subtype_id"]
            args["id:eq"] = all_filtered_id
            all_items, count = Item.filtration(args)
            return response_structure(all_items, count), 200
        args["item_subtype_id:eq"] = args["item_subtype_id"]
        all_items, count = Item.filtration(args)
        return response_structure(all_items, count), 200


@api.route("/available")
class items_list(Resource):
    @api.doc("Get all items with date filter")
    @api.marshal_list_with(schema.get_list_responseItem)
    @api.param("start_time", required=True)
    @api.param("end_time", required=True)
    @auth
    def get(self):
        args = request.args
        start_time = datetime.strptime(args["start_time"], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(args["end_time"], '%Y-%m-%d %H:%M:%S')
        available_items_ids = []

        for item in Item.get_all_active_items(g.current_user.id):
            for each in Booking.get_bookings_by_item_id(item.id):
                if not (each.start_time <= end_time and start_time <= each.end_time):
                    available_items_ids.append(str(item.id))
        if available_items_ids:
            new_args = {"id:eq": ",".join(available_items_ids), "user_id:eq": g.current_user.id}
            all_items, count = Item.filtration(new_args)
            return response_structure(all_items, count), 200
        return response_structure([], 0), 200


@api.route("")
class items_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseItem)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_items, count = Item.filtration(args)
        return response_structure(all_items, count), 200

    @api.marshal_list_with(schema.get_list_responseItem, skip_none=True)
    @api.expect(schema.ItemExpect, validate=True)
    @auth
    def post(self):

        name = request.json.get("name")
        image = request.json.get("image")
        description = request.json.get("description")
        item_status_id = ItemStatus.get_id_by_name("Available")
        item_type_id = request.json.get("item_type_id")
        item_subtype_id = request.json.get("item_subtype_id")
        count = request.json.get("count")
        items = []
        for each in range(count):
            item = Item(name, image, description, item_status_id, item_type_id, item_subtype_id, g.current_user.id)
            items.append(item)
            item.insert()
            if "tag_ids" in request.json.keys():
                if request.json.get("tag_ids") != "":
                    tag_ids = request.json.get("tag_ids").split(",")
                    for each in tag_ids:
                        if each:
                            ItemTag(item_id=item.id, tag_id=each).insert()
            if "location_ids" in request.json.keys():
                if request.json.get("location_ids") != "":
                    location_ids = request.json.get("location_ids").split(",")
                    for each in location_ids:
                        if each:
                            ItemLocation(item_id=item.id, location_id=each).insert()
        return response_structure(items, len(items)), 201


@api.route("/<int:item_id>")
class item_by_id(Resource):
    @api.doc("Get all accounts")
    @api.marshal_list_with(schema.get_by_id_responseItem)
    @auth
    def get(self, item_id):
        item = Item.query_by_id(item_id)
        return response_structure(item), 200

    @api.doc("Delete item by id")
    @auth
    def delete(self, item_id):
        Item.delete(item_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseItem, skip_none=True)
    @api.expect(schema.ItemExpect)
    @auth
    def patch(self, item_id):
        data = api.payload.copy()
        if "tag_ids" in data.keys():
            ItemTag.delete_by_item_id(item_id)
            tag_ids = data.get("tag_ids").split(",")
            for each in tag_ids:
                if each:
                    ItemTag(item_id=item_id, tag_id=each).insert()
            del data["tag_ids"]
        if "location_ids" in data.keys():
            ItemLocation.delete_by_item_id(item_id)
            location_ids = data.get("location_ids").split(",")
            for each in location_ids:
                if each:
                    ItemLocation(item_id=item_id, location_id=each).insert()
            del data["location_ids"]
        Item.update(item_id, data)
        item = Item.query_by_id(item_id)
        return response_structure(item), 200
