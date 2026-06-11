import os

from flask import Blueprint
from flask import request
from flask import jsonify

from werkzeug.utils import secure_filename

from models import db
from models import Student

upload_bp = Blueprint(
    "upload",
    __name__
)

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):

    return "." in filename and \
           filename.rsplit(
               ".",
               1
           )[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route(
    "/upload_resume/<int:id>",
    methods=["POST"]
)
def upload_resume(id):

    if "resume" not in request.files:

        return jsonify(
            {"message": "No File"}
        )

    file = request.files["resume"]

    if file.filename == "":

        return jsonify(
            {"message": "No Selected File"}
        )

    if allowed_file(file.filename):

        filename = secure_filename(
            file.filename
        )

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        student = Student.query.get(id)

        student.resume = filepath

        db.session.commit()

        return jsonify({

            "message":
            "Resume Uploaded",

            "path":
            filepath
        })

    return jsonify(
        {"message": "Only PDF Allowed"}
    )