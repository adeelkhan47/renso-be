from flask import Blueprint
from flask_restx import Api

from .booking.endpoint import api as booking_api
from .item.endpoint import api as item_api
from .item_type.endpoint import api as item_type_api
from .order.endpoint import api as order_api
from .user.endpoint import api as user_api

blueprint = Blueprint("api", __name__)
api = Api(blueprint, title="Renso Api's", version="0.1", description="Renso official api's")

api.add_namespace(user_api)
api.add_namespace(item_api)
api.add_namespace(item_type_api)
api.add_namespace(booking_api)
api.add_namespace(order_api)
