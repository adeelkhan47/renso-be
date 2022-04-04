from flask_restx import fields
from werkzeug.datastructures import FileStorage

from . import api

file_post_parameter = api.parser()
file_post_parameter.add_argument(
    "image", location="files", type=FileStorage, required=True, action="append"
)
file = api.model(
    "File",
    {
        "url": fields.String(),
        "key": fields.String(),
    },
)

error = api.model(
    "Error",
    {

        "msg": fields.String(),

    },
)

file_post_response = api.model(
    "FilePostResponse",
    {
        "objects": fields.Nested(file),
        "error": fields.Nested(error, allow_null=True),
    },
)
