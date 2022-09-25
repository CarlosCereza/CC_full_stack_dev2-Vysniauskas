'''File containing all RESTfull API methods'''

from datetime import datetime
from flask import jsonify, request, abort
from app import app, database
from model import Posts
import constants


@app.route(constants.BASE_URL, methods=["POST"])
def create():
    '''Creates a row in the database from the JSON provided and returns
    code 201, OR method fails with code 400 and returns custom error message
    '''
    data = request.get_json()
    full_name = data.get("Full_name")
    picture_url = data.get("Picture_url")
    date = data.get("Date")
    comment = data.get("Comment")

    if not full_name or not picture_url or not date or not comment:
        return abort(400, description=constants.ALL_REQUIRED)
    check_date(data)
    check_name(data)

    try:
        post = Posts(full_name, picture_url, date, comment)
        database.session.add(post)
        database.session.commit()
        return constants.CREATED, 201
    except Exception:
        database.session.rollback()
        return abort(400, description=constants.BAD_REQUEST)


@app.route(constants.BASE_URL + "<int:id_>", methods=["GET"])
def read(id_):
    '''Returns details about post that has given ID and code 200,
    OR fails with code 404 and error message if such post does not exist
    '''
    query_result = get_post_by_id(id_)
    if query_result is None:
        return abort(404, description=constants.NOT_FOUND + str(id_))
    return convert(query_result), 200


@app.route(constants.BASE_URL + "<int:id_>", methods=["PATCH"])
def update(id_):
    '''Updates details provided in JSON about post that has given ID
    and code 200, OR fails with code 404 and error message if such post does
    not exist, OR fails with code 400 if the JSON provided is
    empty/does not fit format
    '''
    query_result = get_post_by_id(id_)
    if query_result is None:
        return abort(404, description=constants.NOT_FOUND + str(id_))

    data = request.get_json()
    if data.get("Full_name") in ("", [], {}, None):
        check_name(data)
        query_result.Full_name = data["Full_name"]

    if data.get("Picture_url") not in ("", [], {}, None):
        query_result.Picture_url = data["Picture_url"]

    if data.get("Date") not in ("", [], {}, None):
        check_date(data)
        query_result.Date = data["Date"]

    if data.get("Comment") not in ("", [], {}, None):
        query_result.Comment = data["Comment"]

    try:
        database.session.commit()
        return constants.UPDATED, 200
    except Exception:
        database.session.rollback()
        return abort(500)


@app.route(constants.BASE_URL + "<int:id_>", methods=["DELETE"])
def delete(id_):
    '''Deletes post with given ID from database and return code 204,
    OR fails with code 404 and error message if such post does not exist
    '''
    query_result = get_post_by_id(id_)
    if query_result is None:
        return abort(404, description=constants.NOT_FOUND + str(id_))
    database.session.delete(query_result)
    database.session.commit()
    return "", 204


@app.route(constants.BASE_URL, methods=["GET"])
def read_all():
    '''Returns details about all posts
    in the table of the database and code 200
    '''
    posts_list = []

    query_result = Posts.query.all()
    for post in query_result:
        posts_list.append(convert(post))

    return jsonify(posts_list), 200

# Common functions bellow


def get_post_by_id(id_):
    '''Returns details about post at given ID, OR None if it doesn't exist'''
    try:
        post = Posts.query.filter_by(ID=id_).first()
        return post
    except Exception:
        return None


def convert(post):
    '''Converts given post to JSON format'''
    post_as_dictionary = {}

    post_as_dictionary["ID"] = post.ID
    post_as_dictionary["Full_name"] = post.Full_name
    post_as_dictionary["Picture_url"] = post.Picture_url
    post_as_dictionary["Date"] = post.Date.strftime("%Y-%m-%d")
    post_as_dictionary["Comment"] = post.Comment

    return post_as_dictionary


def check_date(data):
    '''Checks if date is in correct format and not in the future'''
    try:
        new_date = datetime.strptime(data.get("Date"), "%Y-%m-%d")
    except ValueError as error:
        return abort(400, description=error.args[0])

    if new_date > datetime.now():
        return abort(400, description=constants.REQUIREMENT1)


def check_name(data):
    '''Checks if name is not empty and both name and surname is provided'''
    if (data.get("Full_name")).count(" ") == 0:
        return abort(400, description=constants.REQUIREMENT2)

# Error handlers bellow


@app.errorhandler(404)
def throw404(error=None):
    print(str(error))
    return str(error), 404


@app.errorhandler(400)
def throw400(error=None):
    print(str(error))
    return str(error), 400


@app.errorhandler(405)
def throw405(error=None):
    print(constants.NOT_IMPLEMENTED)
    return constants.NOT_IMPLEMENTED, 405


@app.errorhandler(Exception)
def handle_any(error=None):
    error_message = str(error)
    print(error_message)
    return error_message, 500
