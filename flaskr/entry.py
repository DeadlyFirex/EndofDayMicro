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
                                     {"data": {"uuid": new_entry.uuid, "body": body, "tags": tags}})


@entry.route("/delete", methods=['DELETE'])
@user_required()
def delete_entry():
    """
    """
    uuid = request.args.get("uuid", None)

    if not isinstance(uuid, str) or not Utilities.validate_uuid(uuid):
        return Utilities.detailed_response(400, "Bad request, see details.",
                                           {"error": {"message": "Invalid UUID received", "input": uuid,
                                                      "type": type(uuid), "expected": "str",
                                                      "valid": Utilities.validate_uuid(uuid)}})

    to_delete = Entry.query.filter_by(uuid=uuid, user=get_jwt_identity())

    if to_delete is None:
        return Utilities.response(404, "Not found")

    to_delete.delete()
    db_session.commit()

    return Utilities.custom_response(200, f"Successfully removed entry",
                                     {"data": {"uuid": uuid}})