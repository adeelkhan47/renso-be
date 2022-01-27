from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.day_picker import DayPicker
from model.item_subtype import ItemSubType
from . import api, schema


@api.route("")
class item_types_list(Resource):
    @api.doc("Get all items")
    @api.marshal_list_with(schema.get_list_responseItem_Subtype)
    def get(self):
        args = request.args
        all_items, count = ItemSubType.filtration(args)
        return response_structure(all_items, count), 200

    @api.expect(schema.Item_subtype_Expect)
    @api.marshal_with(schema.get_by_id_responseItem_Subtype)
    def post(self):
        payload = api.payload
        name = payload.get("name")
        price = payload.get("price")
        item_type_id = payload.get("item_type_id")
        person = payload.get("person")
        item_subtype = ItemSubType(name, price, person, item_type_id)
        item_subtype.insert()
        day_picker = DayPicker(True, True, True, True, True, True, True, item_type_id, item_subtype.id)
        day_picker.insert()
        return response_structure(item_subtype), 201


@api.route("/<int:item_subtype_id>")
class item_subtype_by_id(Resource):
    @api.marshal_list_with(schema.get_by_id_responseItem_Subtype)
    def get(self, item_subtype_id):
        itemSubType = ItemSubType.query_by_id(item_subtype_id)
        return response_structure(itemSubType), 200

    @api.doc("Delete ItemSubType by id")
    def delete(self, item_subtype_id):
        ItemSubType.delete(item_subtype_id)
        return "ok", 200

    @api.marshal_list_with(schema.get_by_id_responseItem_Subtype)
    @api.expect(schema.Item_subtype_Expect)
    def patch(self, item_subtype_id):
        payload = api.payload
        data = payload.copy()
        ItemSubType.update(item_subtype_id, data)
        itemSubType = ItemSubType.query_by_id(item_subtype_id)
        return response_structure(itemSubType), 200


@api.route("/by_item_id/<int:item_type_id>")
class item_subtype_by_item_typeid(Resource):
    @api.marshal_list_with(schema.get_list_responseItem_Subtype)
    def get(self, item_type_id):
        itemSubType = ItemSubType.get_by_item_type_id(item_type_id)
        return response_structure(itemSubType, len(itemSubType)), 200
