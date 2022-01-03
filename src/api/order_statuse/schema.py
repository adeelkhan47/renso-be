from flask_restx import fields

from . import api


get_all_order_status = api.model(
    "getById_booking",
    {
        "objects": fields.List(fields.String()),

    },
)
