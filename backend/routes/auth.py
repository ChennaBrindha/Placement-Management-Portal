from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models import db, User, Student

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
bcrypt = Bcrypt()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    required = ["name", "email", "password", "role"]
    for field in required:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 409

    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    role = data["role"] if data["role"] in ["student", "admin"] else "student"

    user = User(name=data["name"], email=data["email"], password=hashed, role=role)
    db.session.add(user)
    db.session.flush()  # get user.id before commit

    if role == "student":
        student = Student(
            user_id=user.id,
            name=data["name"],
            email=data["email"],
            department=data.get("department", ""),
            graduation_year=data.get("graduation_year"),
        )
        db.session.add(student)

    db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password required"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "name": user.name},
    )

    # get student id if student
    student_id = None
    if user.role == "student":
        student = Student.query.filter_by(user_id=user.id).first()
        student_id = student.id if student else None

    return jsonify({
        "token": token,
        "role": user.role,
        "name": user.name,
        "user_id": user.id,
        "student_id": student_id,
    })