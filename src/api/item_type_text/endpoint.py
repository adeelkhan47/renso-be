from flask import request
from flask_restx import Resource

from common.helper import response_structure
from decorator.authorization import auth
from model.item_type_text import ItemTypeText
from . import api, schema


@api.route("")
class ItemTypeTextList(Resource):
    @api.doc("Get all ItemTypeText")
    @api.marshal_list_with(schema.get_list_ItemTypeText)
    @auth
    def get(self):
        args = request.args.copy()
        all_rows, count = ItemTypeText.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.ItemTypeText_Expect2)
    @api.marshal_list_with(schema.get_by_id_ItemTypeText)
    @auth
    def post(self):
        payload = api.payload
        itemTypeText = ItemTypeText(**payload)
        itemTypeText.insert()
        return response_structure(itemTypeText), 201


@api.route("/<int:item_type_text_id>")
class ItemTypeText_by_id(Resource):
    @api.doc("Get ItemTypeText by id")
    @api.marshal_list_with(schema.get_by_id_ItemTypeText)
    @auth
    def get(self, item_type_text_id):
        itemTypeText = ItemTypeText.query_by_id(item_type_text_id)
        return response_structure(itemTypeText), 200

    @api.doc("Delete method by id")
    @auth
    def delete(self, item_type_text_id):
        ItemTypeText.delete(item_type_text_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_ItemTypeText)
    @api.expect(schema.ItemTypeText_Expect2)
    @auth
    def patch(self, item_type_text_id):
        payload = api.payload.copy()

        ItemTypeText.update(item_type_text_id, payload)
        itemTypeText = ItemTypeText.query_by_id(item_type_text_id)
        return response_structure(itemTypeText), 200

