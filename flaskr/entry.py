from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from models.entry import Entry
from services.database import db_session
from services.utilities import Utilities, user_required

# Configure blueprint
entry = Blueprint('entry', __name__, url_prefix='/entry')


@entry.route("/add", methods=['POST'])
@user_required()
def post_entry_add():
    """
    Logs a user in.\n
    Returns a ``JWT`` token for authentication.

    :return: JSON detailed status response with (login) data.
    """
    try:
        body = request.json.get("body", None)
        tags = request.json.get("tags", None)

        if not isinstance(body, str):
            raise ValueError(f"Expected str, instead got {type(body)} for field <username>")
        if not isinstance(tags, list):
            raise ValueError(f"Expected str, instead got {type(tags)} for field <password>")

    except (AttributeError, ValueError) as e:
        return Utilities.detailed_response(400, "Bad request, see details.", {"error": e.__str__()})

    new_entry = Entry(text=body, tags=tags, user=get_jwt_identity())
    db_session.add(new_entry)
    db_session.commit()

    return Utilities.custom_response(200, f"Successfully received response",
                                     {"data": {"body": body, "tags": tags}})
