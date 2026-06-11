from flask import Blueprint
from flask import request
from flask import jsonify

from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

from models import db
from models import Company

company_bp = Blueprint(
    "company",
    __name__
)

bcrypt = Bcrypt()


@company_bp.route(
    "/company/register",
    methods=["POST"]
)
def register_company():

    data = request.json

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    company = Company(
        company_name=data["company_name"],
        email=data["email"],
        password=hashed_password
    )

    db.session.add(company)
    db.session.commit()

    return jsonify(
        {"message": "Company Registered"}
    )


@company_bp.route(
    "/company/login",
    methods=["POST"]
)
def login_company():

    data = request.json

    company = Company.query.filter_by(
        email=data["email"]
    ).first()

    if not company:
        return jsonify(
            {"message": "Company Not Found"}
        ), 404

    valid = bcrypt.check_password_hash(
        company.password,
        data["password"]
    )

    if not valid:
        return jsonify(
            {"message": "Invalid Password"}
        ), 401

    token = create_access_token(
        identity=company.id
    )

    return jsonify(
        {"token": token}
    )