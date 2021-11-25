from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.item_type import ItemType
from . import api, schema


@api.route("")
class items_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_items, count = ItemType.filtration(args)
        return response_structure(all_items, count), 200

    @api.param("name", required=True)
    @api.param("maintenance", required=True)
    @api.param("delivery_available", required=True)
    def post(self):
        name = request.args.get("name")
        maintenance = request.args.get("maintenance")
        delivery_available = request.args.get("delivery_available")

        item_type = ItemType(name, maintenance, delivery_available)
        item_type.insert()
        return "ok", 201


@api.route("/<int:item_type_id>")
class item_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, item_type_id):
        item = ItemType.query_by_id(item_type_id)
        return response_structure(item), 200

    @api.doc("Delete item by id")
    def delete(self, item_type_id):
        ItemType.delete(item_type_id)
        return "ok", 200
