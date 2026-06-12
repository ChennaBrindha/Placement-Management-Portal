import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from models import db, Student

upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/resume/<int:student_id>", methods=["POST"])
@jwt_required()
def upload_resume(student_id):
    if "resume" not in request.files:
        return jsonify({"message": "No file attached"}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Only PDF files allowed"}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    filename = secure_filename(f"student_{student_id}_{file.filename}")
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    student.resume = filename
    db.session.commit()

    return jsonify({"message": "Resume uploaded", "filename": filename})


@upload_bp.route("/resume/download/<filename>", methods=["GET"])
@jwt_required()
def download_resume(filename):
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, filename, as_attachment=True)