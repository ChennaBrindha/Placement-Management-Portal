from flask import Blueprint
from flask import request
from flask import jsonify

from flask_bcrypt import Bcrypt

from flask_jwt_extended import (
    create_access_token
)

from models import db
from models import Student

auth_bp = Blueprint(
    "auth",
    __name__
)

bcrypt = Bcrypt()


@auth_bp.route(
    "/student/register",
    methods=["POST"]
)
def register_student():

    data = request.json

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    student = Student(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        branch=data["branch"],
        cgpa=data["cgpa"],
        skills=data["skills"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify(
        {"message": "Student Registered"}
    )


@auth_bp.route(
    "/student/login",
    methods=["POST"]
)
def login_student():

    data = request.json

    student = Student.query.filter_by(
        email=data["email"]
    ).first()

    if not student:
        return jsonify(
            {"message": "User Not Found"}
        ), 404

    valid = bcrypt.check_password_hash(
        student.password,
        data["password"]
    )

    if not valid:
        return jsonify(
            {"message": "Wrong Password"}
        ), 401

    token = create_access_token(
        identity=student.id
    )

    return jsonify(
        {"token": token}
    )