from flask import Blueprint, session, render_template, redirect, request, jsonify
import os
from db import *

current_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(current_dir, '..', 'templates')

exercises_bp = Blueprint('exercises', __name__, url_prefix='/exercises', template_folder=template_dir)

## exercise routes (viewing exercises or posting new one)
@exercises_bp.route('/', methods=["GET", "POST"])
def exercises():
    logged_in_user = session.get('logged_in_user')
    if not logged_in_user:
        return "need to log in first!", 401

    if request.method == "GET":
        result = db_block(view_all_exercises)
        if result:
                return result
    elif request.method == "POST":

        try:
            fields = ("name", "image")
            values = process_request(request, *fields)

            name, image = values['name'], values["image"]
        
            result = db_block(create_exercise, logged_in_user, name, image)

            return jsonify({'result': result})
        except:
            return "error occurred", 400

# individual exercise routes (selecting, updating or deleting)
@exercises_bp.route('/<int:id>', methods=["GET", "PUT", "DELETE"])
def exercise(id):
    # DEV ONLY not being used yet 11/4 GET or PUT ??
    if request.method == "GET":
        result = db_block(view_exercise, id)
        if result:
                return result
        else:
            return 404
        
    # DEV ONLY not being used yet 11/4 GET or PUT ??
    if request.method == "PUT":
        logged_in_user = session.get('logged_in_user')
        if not logged_in_user:
            return "Unauthorized", 401
        
        return update_wrapper(request, ["name", "image"], id, update_exercise, logged_in_user)

    if request.method == "DELETE":
        try:
            logged_in_user = session.get('logged_in_user')
            if not logged_in_user:
                return "Unauthorized", 401
            
            result, status_code = db_block(delete_exercise, id, logged_in_user)
            if status_code == 200:
                return result
            else:
                return result, status_code
        except:
            return 'error occurred'
 