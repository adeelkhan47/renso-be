from flask_restx import fields

from . import api


get_all_item_status = api.model(
    "getById_booking",
    {
        "objects": fields.List(fields.String()),

    },
)
