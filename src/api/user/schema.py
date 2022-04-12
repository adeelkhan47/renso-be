from flask_restx import fields

from . import api

userPostExpect = api.model(
    "userPostExpect",
    {
        "email": fields.String(),
        "name": fields.String(),
        "subscription": fields.String(),
        "image": fields.String(),
        "gender": fields.String(),
        "status": fields.Boolean(),
        "password": fields.String()

    }
)
userLoginPostExpect = api.model(
    "userLoginPostExpect",
    {
        "email": fields.String(),
        "password": fields.String(),
    }
)
User = api.model(
    "User",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "email": fields.String(),
        "subscription": fields.String(),
        "image": fields.String(),
        "gender": fields.String(),
        "status": fields.Boolean(),
        "user_key": fields.String()
    },
)

error = api.model(
    "Error",
    {

        "msg": fields.String(),

    },
)

get_list_responseUser = api.model(
    "getAll_User",
    {
        "total_rows": fields.Integer(),
        "objects": fields.Nested(User, as_list=True),
        "error": fields.Nested(error, allow_null=True),
    },
)
get_by_id_responseUser = api.model(
    "getUserById_User",
    {
        "objects": fields.Nested(User, skip_none=True),
        "error": fields.Nested(error, allow_null=True),

    },
)
