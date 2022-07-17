from flask import request
from flask_restx import Resource

from common.helper import response_structure
from model.order_status import OrderStatus

from . import api, schema


@api.route("")
class OrderStatusList(Resource):
    @api.doc("Get all OrderStatus")
    @api.marshal_list_with(schema.get_list_responseOrderStatus)
    def get(self):
        args = request.args.copy()
        args["is_deleted:eq"] = "False"
        all_rows, count = OrderStatus.filtration(args)
        return response_structure(all_rows, count), 200

    @api.expect(schema.OrderStatusExpect)
    @api.marshal_list_with(schema.get_by_id_responseOrderStatus)
    def post(self):
        payload = api.payload
        name = payload.get("name")
        color = payload.get("color")
        order_status = OrderStatus(name, color)
        order_status.insert()
        return response_structure(order_status), 201


@api.route("/<int:order_status_id>")
class OrderStatus_by_id(Resource):
    @api.doc("Get OrderStatus by id")
    @api.marshal_list_with(schema.get_by_id_responseOrderStatus)
    def get(self, order_status_id):
        tag = OrderStatus.query_by_id(order_status_id)
        return response_structure(tag), 200

    @api.doc("Delete method by id")
    def delete(self, order_status_id):
        OrderStatus.soft_delete(order_status_id)
        return "ok", 200
