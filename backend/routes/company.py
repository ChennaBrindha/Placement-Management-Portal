from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, Company
from routes.rbac import role_required

company_bp = Blueprint("company", __name__, url_prefix="/api/companies")
bcrypt = Bcrypt()


@company_bp.route("/", methods=["GET"])
def get_companies():
    companies = Company.query.all()
    return jsonify([c.to_dict() for c in companies])


@company_bp.route("/<int:company_id>", methods=["GET"])
def get_company(company_id):
    company = Company.query.get_or_404(company_id)
    return jsonify(company.to_dict())


@company_bp.route("/register", methods=["POST"])
@role_required("admin")
def register_company():
    data = request.json
    required = ["company_name", "email", "password"]
    for f in required:
        if not data.get(f):
            return jsonify({"message": f"{f} is required"}), 400

    if Company.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Company already registered"}), 409

    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    company = Company(
        company_name=data["company_name"],
        email=data["email"],
        password=hashed,
        industry=data.get("industry", ""),
        website=data.get("website", ""),
        description=data.get("description", ""),
    )
    db.session.add(company)
    db.session.commit()
    return jsonify({"message": "Company registered", "company": company.to_dict()}), 201


@company_bp.route("/<int:company_id>", methods=["PUT"])
@role_required("admin")
def update_company(company_id):
    company = Company.query.get_or_404(company_id)
    data = request.json
    company.company_name = data.get("company_name", company.company_name)
    company.industry = data.get("industry", company.industry)
    company.website = data.get("website", company.website)
    company.description = data.get("description", company.description)
    db.session.commit()
    return jsonify({"message": "Company updated", "company": company.to_dict()})


@company_bp.route("/<int:company_id>", methods=["DELETE"])
@role_required("admin")
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    return jsonify({"message": "Company deleted"})