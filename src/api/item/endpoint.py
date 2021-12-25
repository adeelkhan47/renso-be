from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.item import Item
from model.item_tag import ItemTag
from . import api, schema


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
    @api.param("item_type_id", required=True)
    @api.param("tag_ids", )
    def post(self):
        name = request.args.get("name")
        image = request.args.get("image")
        description = request.args.get("description")
        price = request.args.get("price")
        item_type_id = request.args.get("item_type_id")
        item = Item(name, image, description, price, item_type_id)
        item.insert()
        if "tag_ids" in request.args.keys():
            tag_ids = request.args.get("item_type_id").split(",")
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
