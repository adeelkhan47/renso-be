from http import HTTPStatus
from typing import Dict, Tuple

from flask_restx import Resource
from werkzeug.exceptions import BadRequest

from common.helper import response_structure, error_message
from service.s3 import upload_image
from . import api, schema


@api.route("")
class FileList(Resource):
    @api.doc("Upload File")
    @api.marshal_list_with(schema.file_post_response, skip_none=True)
    @api.response(HTTPStatus.OK, "Success")
    def post(self) -> Tuple[Dict, int]:
        """
        Upload File to s3

        :param audience_id:
        :return:
        """
        args = schema.file_post_parameter.parse_args()
        files = args["image"]
        if len(files) >= 1:
            url, key = upload_image(files[0])
            return response_structure({"url": url, "key": key}), HTTPStatus.OK
        else:
            raise BadRequest(error_message("File Upload failed."))
