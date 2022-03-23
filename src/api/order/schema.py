from flask_restx import fields

from . import api
from ..booking.schema import Booking
from ..order_status.schema import OrderStatus

CustomDataModel = api.model(
    "customDataModel",

    {
        "id": fields.Integer(),
        "name": fields.String(),
        "value": fields.String()
    }
)
bookings = api.model(
    "bookings",
    {"booking": fields.Nested(Booking, as_list=True)}
)
customData = api.model(
    "customData",
    {"custom_data": fields.Nested(CustomDataModel, as_list=True)}
)

Order_Expect = api.model(
    "Order_Expect",
    {
        "client_name": fields.String(),
        "client_email": fields.String(),
        "phone_number": fields.String(),
        "time_period": fields.String(),
        "cart_id": fields.Integer()
    },
)

Order = api.model(
    "Order",
    {
        "id": fields.Integer(),
        "client_name": fields.String(),
        "client_email": fields.String(),
        "phone_number": fields.String(),
        "order_status": fields.Nested(OrderStatus),
        "time_period": fields.String(),
        "total_cost": fields.Float(),
        "order_bookings": fields.Nested(bookings, as_list=True),
        "order_custom_data": fields.Nested(customData, as_list=True)
    },
)
Order_With_Session = api.model(
    "Order_With_Session", {
        "order": fields.Nested(Order),
        "session_id": fields.String()
    }

)
error = api.model(
    "Error",
    {

        "msg": fields.String(),

    },
)

get_list_responseOrder = api.model(
    "getAll_Order",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(Order, as_list=True),
        "error": fields.Nested(error, allow_null=True),
    },
)
get_by_id_responseOrder_with_session = api.model(
    "getById_Order_with_session",
    {
        "objects": fields.Nested(Order_With_Session),
        "error": fields.Nested(error, allow_null=True),

    },
)

get_by_id_responseOrder = api.model(
    "getById_Order",
    {
        "objects": fields.Nested(Order),
        "error": fields.Nested(error, allow_null=True),

    },
)
