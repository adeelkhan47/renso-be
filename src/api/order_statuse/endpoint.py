from flask_restx import Resource

from common.helper import response_structure
from . import api, schema


@api.route("")
class OrderStatusList(Resource):
    @api.doc("Get all valid_status for Order")
    @api.marshal_list_with(schema.get_all_order_status)
    def get(self):
        list = ["Active", "Completed", "Cancelled"]
        return response_structure(list), 200
