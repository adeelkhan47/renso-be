import logging
import os
from http import HTTPStatus

from .user.endpoint import api as user_api
from .item.endpoint import api as item_api
from flask import Blueprint
from flask_restx import Api
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, Unauthorized

blueprint = Blueprint("api", __name__)
api = Api(blueprint, title="Renso Api's", version="0.1", description="Renso official api's")

api.add_namespace(user_api)
api.add_namespace(item_api)