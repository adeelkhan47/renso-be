from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.item_status import ItemStatus

from . import api, schema


@api.route("")
class ItemStatusList(Resource):
    @api.doc("Get all ItemStatus")
    @api.marshal_list_with(schema.get_list_responseItemStatus)
    def get(self):
        args = request.args
        all_rows, count = ItemStatus.filtration(args)
        return response_structure(all_rows, count), 200

    @api.param("name", required=True)
    @api.param("color", required=True)
    def post(self):
        name = request.args.get("name")
        color = request.args.get("color")
        item_status = ItemStatus(name, color)
        item_status.insert()
        return "ok", 201


@api.route("/<int:item_status_id>")
class tag_by_id(Resource):
    @api.doc("Get ItemStatus by id")
    @api.marshal_list_with(schema.get_by_id_responseItemStatus)
    def get(self, item_status_id):
        item_status = ItemStatus.query_by_id(item_status_id)
        return response_structure(item_status), 200

    @api.doc("Delete method by id")
    def delete(self, item_status_id):
        ItemStatus.delete(item_status_id)
        return "ok", 200
