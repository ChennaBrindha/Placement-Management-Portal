from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Student
from routes.rbac import role_required

student_bp = Blueprint("student", __name__, url_prefix="/api/students")


@student_bp.route("/", methods=["GET"])
@role_required("admin")
def get_students():
    """Admin: list all students with optional filters."""
    department = request.args.get("department")
    min_cgpa = request.args.get("min_cgpa", type=float)
    is_placed = request.args.get("is_placed")

    query = Student.query
    if department:
        query = query.filter_by(department=department)
    if min_cgpa is not None:
        query = query.filter(Student.cgpa >= min_cgpa)
    if is_placed is not None:
        query = query.filter_by(is_placed=is_placed.lower() == "true")

    students = query.all()
    return jsonify([s.to_dict() for s in students])


@student_bp.route("/<int:student_id>", methods=["GET"])
@jwt_required()
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict())


@student_bp.route("/<int:student_id>", methods=["PUT"])
@jwt_required()
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.json

    student.name = data.get("name", student.name)
    student.phone = data.get("phone", student.phone)
    student.department = data.get("department", student.department)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.graduation_year = data.get("graduation_year", student.graduation_year)
    student.skills = data.get("skills", student.skills)

    db.session.commit()
    return jsonify({"message": "Profile updated", "student": student.to_dict()})


@student_bp.route("/stats", methods=["GET"])
@role_required("admin")
def placement_stats():
    """Return placement statistics for admin dashboard."""
    total = Student.query.count()
    placed = Student.query.filter_by(is_placed=True).count()
    departments = db.session.query(
        Student.department, db.func.count(Student.id)
    ).group_by(Student.department).all()

    return jsonify({
        "total_students": total,
        "placed": placed,
        "unplaced": total - placed,
        "placement_rate": round((placed / total * 100), 1) if total else 0,
        "by_department": [{"department": d, "count": c} for d, c in departments],
    })