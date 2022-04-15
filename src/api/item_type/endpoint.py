from flask import g
from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from decorator.authorization import auth
from model.day_picker import DayPicker
from model.item_type import ItemType
from model.item_type_extra import ItemTypeExtra
from model.location_item_type import LocationItemTypes
from model.season import Season
from . import api, schema


@api.route("")
class item_types_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseItem_type)
    @auth
    def get(self):
        args = request.args.copy()
        args["user_id:eq"] = str(g.current_user.id)
        all_items, count = ItemType.filtration(args)
        return response_structure(all_items, count), 200

    @api.expect(schema.Item_type_Expect)
    @api.marshal_with(schema.get_by_id_responseItem_type)
    @auth
    def post(self):
        payload = api.payload
        name = payload.get("name")
        maintenance = payload.get("maintenance")
        image = payload.get("image")
        location_ids = payload.get("location_ids").split(",")
        delivery_available = int(payload.get("delivery_available"))
        item_type = ItemType(name, maintenance, delivery_available, image, g.current_user.id)
        item_type.insert()
        for each in location_ids:
            if each:
                LocationItemTypes(each, item_type.id).insert()
        day_picker = DayPicker(True, True, True, True, True, True, True, item_type.id)
        day_picker.insert()

        return response_structure(item_type), 201


@api.route("/<int:item_type_id>")
class item_type_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseItem_type)
    @auth
    def get(self, item_type_id):
        item = ItemType.query_by_id(item_type_id)
        if not item:
            raise NotFound("Item Type ID not found")
        return response_structure(item), 200

    @api.doc("Delete item by id")
    @auth
    def delete(self, item_type_id):
        ItemType.delete(item_type_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseItem_type)
    @api.expect(schema.Item_type_Expect)
    @auth
    def patch(self, item_type_id):
        payload = api.payload.copy()
        if "location_ids" in payload.keys():
            LocationItemTypes.delete_by_item_type_id(item_type_id)
            for each in payload.get("location_ids"):
                if each:
                    LocationItemTypes(each, item_type_id).insert()
            del payload["location_ids"]
        ItemType.update(item_type_id, payload)
        itemType = ItemType.query_by_id(item_type_id)
        return response_structure(itemType), 200


@api.route("/for_current_season")
class item_types_for_season_list(Resource):
    @api.doc("Get all items for_season")
    @api.marshal_list_with(schema.get_list_responseItem_type)
    @auth
    def get(self):
        seasons = [each.id for each in Season.current_seasons_by_user_id(g.current_user.id)]
        all_items, count = ItemType.filtration({"user_id:eq": str(g.current_user.id)})
        items_to_return = []
        for item_type in all_items:
            for each_season in item_type.seasonItemTypes:
                if each_season.season_id in seasons and item_type not in items_to_return and item_type.name != "Extra":
                    items_to_return.append(item_type)
                    break
        return response_structure(items_to_return, len(items_to_return)), 200


@api.route("/extras")
class item_type_for_extras(Resource):
    @api.expect(schema.Item_type_extra_Expect)
    @api.marshal_list_with(schema.get_by_id_responseItem_type)
    @auth
    def post(self):
        payload = api.payload
        item_type_id = payload.get("item_type_id")
        old_record = ItemTypeExtra.get_by_item_type_id(item_type_id)
        if old_record:
            return response_structure("Record Already Exist."), 400
        item_subtype_ids = payload.get("item_sub_type_ids").split(",")
        for each in item_subtype_ids:
            if each:
                ItemTypeExtra(each, item_type_id).insert()
        item_type = ItemType.query_by_id(item_type_id)
        return response_structure(item_type), 200

    @api.expect(schema.Item_type_extra_Expect)
    @api.marshal_list_with(schema.get_by_id_responseItem_type)
    @auth
    def patch(self):
        payload = api.payload
        item_type_id = payload.get("item_type_id")
        item_subtype_ids = payload.get("item_sub_type_ids").split(",")
        ItemTypeExtra.delete_by_item_type_id(item_type_id)
        for each in item_subtype_ids:
            if each:
                ItemTypeExtra(each, item_type_id).insert()
        item_type = ItemType.query_by_id(item_type_id)
        return response_structure(item_type), 200
