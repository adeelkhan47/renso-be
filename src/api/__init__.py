from http import HTTPStatus

from flask import Blueprint
from flask_restx import Api
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, Unauthorized

from common.helper import error_message
from model.base import db

from .associate_email.endpoint import api as associateEmail_api
from .booking.endpoint import api as booking_api
from .booking_status.endpoint import api as booking_status_api
from .booking_widget.endpoint import api as booking_widget_api
from .checkout_session.endpoint import api as checkout_api
from .custom_parameter.endpoint import api as custom_parameter_api
from .day_picker.endpoint import api as day_picker_api
from .item.endpoint import api as item_api
from .item_status.endpoint import api as item_status_api
from .item_subtype.endpoint import api as item_subtype_api
from .item_type.endpoint import api as item_type_api
from .language.endpoint import api as language_api
from .location.endpoint import api as location_api
from .order.endpoint import api as order_api
from .order_status.endpoint import api as order_status_api
from .payment_methods.endpoint import api as payment_method_api
from .season.endpoint import api as season_api
from .tag.endpoint import api as tag_api
from .tax.endpoint import api as tax_api
from .time_picker.endpoint import api as time_picker_api
from .user.endpoint import api as user_api
from .voucher.endpoint import api as voucher_api
from .file_upload.endpoint import api as file_upload_api

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
api.add_namespace(order_status_api)
api.add_namespace(item_status_api)
api.add_namespace(booking_status_api)
api.add_namespace(custom_parameter_api)
api.add_namespace(item_subtype_api)
api.add_namespace(voucher_api)
api.add_namespace(location_api)
api.add_namespace(season_api)
api.add_namespace(associateEmail_api)
api.add_namespace(checkout_api)
api.add_namespace(file_upload_api)


@api.errorhandler(NotFound)
def handle_not_found_error(exception_cause):
    """
    Catch not found error exception globally and respond with 404.
    :param exception_cause:
    :return objects, response Code:
    """
    return error_message(exception_cause.description), HTTPStatus.NOT_FOUND


@api.errorhandler(BadRequest)
def handle_bad_request_error(exception_cause):
    """
    Catch bad request error exception globally and respond with 400.
    :param exception_cause:
    :return objects, response Code:
    """

    return error_message(exception_cause.description), HTTPStatus.BAD_REQUEST


@api.errorhandler(Unauthorized)
def handle_unauthorized_error(exception_cause):
    """
    Catch unauthorized globally and respond with 401.
    :param exception_cause:
    :return objects , response Code:
    """
    return error_message(exception_cause.description), HTTPStatus.UNAUTHORIZED


@api.errorhandler(Forbidden)
def handle_forbidden_error(exception_cause):
    """
    Catch forbidden globally and respond with 403.
    :param exception_cause:
    :return objects , response Code:
    """

    return error_message(exception_cause.description), HTTPStatus.FORBIDDEN


@api.errorhandler(Exception)
def handle_internal_server_error(exception_cause):
    """
    Catch internal server error exception globally and respond with 500.
    :param exception_cause:
    :return objects , response Code:
    """
    db.session.rollback()
    return error_message("internal server error"), HTTPStatus.INTERNAL_SERVER_ERROR

