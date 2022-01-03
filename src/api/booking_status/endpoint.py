from flask_restx import Resource

from common.helper import response_structure
from . import api, schema


@api.route("")
class BookingStatusList(Resource):
    @api.doc("Get all valid_status for booking")
    @api.marshal_list_with(schema.get_all_booking_status)
    def get(self):
        list = ["Active", "Closed", "Draft"]
        return response_structure(list), 200
