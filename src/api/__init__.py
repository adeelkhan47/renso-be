from flask import Blueprint
from flask_restx import Api

from .booking.endpoint import api as booking_api
from .booking_widget.endpoint import api as booking_widget_api
from .day_picker.endpoint import api as day_picker_api
from .item.endpoint import api as item_api
from .item_type.endpoint import api as item_type_api
from .language.endpoint import api as language_api
from .order.endpoint import api as order_api
from .payment_methods.endpoint import api as payment_method_api
from .tax.endpoint import api as tax_api
from .user.endpoint import api as user_api
from .tag.endpoint import api as tag_api
from .time_picker.endpoint import api as time_picker_api

blueprint = Blueprint("api", __name__)
api = Api(blueprint, title="Renso Api's", version="0.1", description="Renso official api's")

api.add_namespace(user_api)
api.add_namespace(item_api)
api.add_namespace(item_type_api)
api.add_namespace(booking_api)
api.add_namespace(order_api)
api.add_namespace(payment_method_api)
api.add_namespace(tax_api)
api.add_namespace(language_api)
api.add_namespace(booking_widget_api)
api.add_namespace(day_picker_api)
api.add_namespace(time_picker_api)
api.add_namespace(tag_api)
