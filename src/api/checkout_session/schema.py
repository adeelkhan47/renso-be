from flask_restx import fields
from flask_restx.fields import List, Nested, String, Float

from . import api

CreateSessionExpect = api.model(
    "createSessionExpect",
    {
        "product_name": String(),
        "price": Float(),
    },
)
SuccessSessionExpect = api.model(
    "successSessionExpect",
    {
        "session_id": String(),
    },
)

CheckOutSession = api.model(
    "checkOutSession",
    {"session_id": String()},
)


CheckOutSuccess = api.model(
    "checkOutSuccess",
    {"msg": String()},
)


CheckOutSessionResponse = api.model(
    "checkOutSessionResponse2",
    {
        "objects": Nested(
            CheckOutSession, as_list=True, skip_none=True, allow_null=True
        ),
        "errors": List(String),
    },
)
CheckOutSessionResponseSuccess = api.model(
    "checkOutSessionResponseSuccess",
    {
        "objects": Nested(
            CheckOutSuccess, as_list=True, skip_none=True, allow_null=True
        ),
        "errors": List(String),
    },
)
error = api.model(
    "Error",
    {
        "msg": fields.String(),
    },
)
