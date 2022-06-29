from functools import wraps
import logging
from flask import g, request
from werkzeug.exceptions import Unauthorized

from common.helper import error_message
from model.user import User


def auth(f):
    @wraps(f)
    def decoder_wrapper_function(*args, **kwargs):
        """
        Authorize user by user_key

        :param args:
        :param kwargs:
        :return:
        """
        logging.error(request.base_url)
        authorization = request.headers.get("Authorization")

        if not authorization:
            raise Unauthorized(error_message("Authorization Missing."))
        user = User.get_by_user_key(authorization)

        if user:
            g.current_user = user
            func_call = f(*args, **kwargs)
            g.current_user = None
            return func_call
        raise Unauthorized(error_message("Unauthorized user."))

    return decoder_wrapper_function
