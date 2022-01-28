from flask import request
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from common.helper import response_structure
from model.item_type import ItemType
from . import api, schema


@api.route("")
class item_types_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseItem_type)
    def get(self):
        args = request.args
        all_items, count = ItemType.filtration(args)
        return response_structure(all_items, count), 200

    @api.expect(schema.Item_type_Expect)
    @api.marshal_with(schema.get_by_id_responseItem_type)
    def post(self):
        payload = api.payload
        name = payload.get("name")
        maintenance = payload.get("maintenance")
        delivery_available = int(payload.get("delivery_available"))

        item_type = ItemType(name, maintenance, delivery_available)
        item_type.insert()
        return response_structure(item_type), 201


@api.route("/<int:item_type_id>")
class item_type_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseItem_type)
    def get(self, item_type_id):
        item = ItemType.query_by_id(item_type_id)
        if not item:
            raise NotFound("Item Type ID not found")
        return response_structure(item), 200

    @api.doc("Delete item by id")
    def delete(self, item_type_id):
        ItemType.delete(item_type_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseItem_type)
    @api.expect(schema.Item_type_Expect)
    def patch(self, item_type_id):
        payload = api.payload
        data = payload.copy()
        if "delivery_available" in data.keys():
            data["delivery_available"] = int(data["delivery_available"])
        ItemType.update(item_type_id, data)
        itemType = ItemType.query_by_id(item_type_id)
        return response_structure(itemType), 200
