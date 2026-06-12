from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, User, Student, Job, Application, Company
from routes.rbac import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")
bcrypt = Bcrypt()


@admin_bp.route("/dashboard", methods=["GET"])
@role_required("admin")
def dashboard():
    total_students = Student.query.count()
    placed = Student.query.filter_by(is_placed=True).count()
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter_by(is_active=True).count()
    total_companies = Company.query.count()
    total_applications = Application.query.count()

    status_counts = db.session.query(
        Application.status, db.func.count(Application.id)
    ).group_by(Application.status).all()

    dept_placed = db.session.query(
        Student.department,
        db.func.count(Student.id).label("total"),
        db.func.sum(db.cast(Student.is_placed, db.Integer)).label("placed"),
    ).group_by(Student.department).all()

    return jsonify({
        "total_students": total_students,
        "placed_students": placed,
        "unplaced_students": total_students - placed,
        "placement_rate": round((placed / total_students * 100), 1) if total_students else 0,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "total_companies": total_companies,
        "total_applications": total_applications,
        "application_status_breakdown": [
            {"status": s, "count": c} for s, c in status_counts
        ],
        "dept_stats": [
            {
                "department": d,
                "total": t,
                "placed": int(p or 0),
            }
            for d, t, p in dept_placed
        ],
    })


@admin_bp.route("/seed", methods=["POST"])
def seed_admin():
    """One-time seed to create default admin. Remove in production."""
    if User.query.filter_by(role="admin").first():
        return jsonify({"message": "Admin already exists"}), 409

    hashed = bcrypt.generate_password_hash("admin123").decode("utf-8")
    admin = User(name="Admin", email="admin@placement.com", password=hashed, role="admin")
    db.session.add(admin)
    db.session.commit()
    return jsonify({"message": "Admin created", "email": "admin@placement.com", "password": "admin123"}), 201