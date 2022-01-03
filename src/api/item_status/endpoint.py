from flask_restx import Resource

from common.helper import response_structure
from . import api, schema


@api.route("")
class ItemStatusList(Resource):
    @api.doc("Get all valid_status for items")
    @api.marshal_list_with(schema.get_all_item_status)
    def get(self):
        list = ["Available", "Booked", "Maintenance", "Expired"]
        return response_structure(list), 200
