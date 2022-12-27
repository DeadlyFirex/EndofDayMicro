from flask import Blueprint

from services.utilities import Utilities

# Configure blueprint
generics = Blueprint('generics', __name__, url_prefix='/')


@generics.route("/ping", methods=['GET'])
def get_ping():
    """
    Ping. Pong.

    :return: JSON detailed status response with (login) data.
    """

    return Utilities.response(200, "Pong")
