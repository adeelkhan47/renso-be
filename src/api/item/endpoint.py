from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.item import Item
from . import api, schema


@api.route("")
class items_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_response)
    def get(self):
        args = request.args
        all_items, count = Item.filtration(args)
        return response_structure(all_items, count), 200

    @api.param("name", required=True)
    @api.param("image", required=True)
    @api.param("tags", required=True)
    @api.param("description", required=True)
    @api.param("price", required=True)
    @api.param("user_id", required=True)
    def post(self):
        name = request.args.get("name")
        image = request.args.get("image")
        tags = request.args.get("tags")
        description = request.args.get("description")
        price = request.args.get("price")
        user_id = request.args.get("user_id")
        item = Item(name, image, tags, description, price, user_id)
        item.insert()
        return "ok", 201


@api.route("/<int:item_id>")
class item_by_id(Resource):
    @api.doc("Get all accounts")
    @api.marshal_list_with(schema.get_by_id_response)
    def get(self, item_id):
        item = Item.query_by_id(item_id)
        return response_structure(item), 200

    @api.doc("Delete item by id")
    def delete(self, item_id):
        Item.delete(item_id)
        return "ok", 200
