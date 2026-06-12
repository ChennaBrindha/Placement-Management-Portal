from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Job, Company
from routes.rbac import role_required
from datetime import datetime

jobs_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")


@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    """Public endpoint - list all active jobs with optional filters."""
    company_id = request.args.get("company_id", type=int)
    job_type = request.args.get("job_type")
    min_cgpa = request.args.get("min_cgpa", type=float)

    query = Job.query.filter_by(is_active=True)
    if company_id:
        query = query.filter_by(company_id=company_id)
    if job_type:
        query = query.filter_by(job_type=job_type)
    if min_cgpa is not None:
        query = query.filter(Job.eligibility_cgpa <= min_cgpa)

    jobs = query.order_by(Job.posted_at.desc()).all()
    return jsonify([j.to_dict() for j in jobs])


@jobs_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict())


@jobs_bp.route("/", methods=["POST"])
@role_required("admin")
def create_job():
    data = request.json
    required = ["company_id", "title"]
    for f in required:
        if not data.get(f):
            return jsonify({"message": f"{f} is required"}), 400

    deadline = None
    if data.get("deadline"):
        try:
            deadline = datetime.fromisoformat(data["deadline"])
        except ValueError:
            return jsonify({"message": "Invalid deadline format"}), 400

    job = Job(
        company_id=data["company_id"],
        title=data["title"],
        description=data.get("description", ""),
        location=data.get("location", ""),
        package=data.get("package", ""),
        eligibility_cgpa=data.get("eligibility_cgpa", 0.0),
        skills_required=data.get("skills_required", ""),
        deadline=deadline,
        job_type=data.get("job_type", "Full-time"),
        is_active=True,
    )
    db.session.add(job)
    db.session.commit()
    return jsonify({"message": "Job posted", "job": job.to_dict()}), 201


@jobs_bp.route("/<int:job_id>", methods=["PUT"])
@role_required("admin")
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.json

    job.title = data.get("title", job.title)
    job.description = data.get("description", job.description)
    job.location = data.get("location", job.location)
    job.package = data.get("package", job.package)
    job.eligibility_cgpa = data.get("eligibility_cgpa", job.eligibility_cgpa)
    job.skills_required = data.get("skills_required", job.skills_required)
    job.job_type = data.get("job_type", job.job_type)
    job.is_active = data.get("is_active", job.is_active)

    if data.get("deadline"):
        try:
            job.deadline = datetime.fromisoformat(data["deadline"])
        except ValueError:
            return jsonify({"message": "Invalid deadline format"}), 400

    db.session.commit()
    return jsonify({"message": "Job updated", "job": job.to_dict()})


@jobs_bp.route("/<int:job_id>", methods=["DELETE"])
@role_required("admin")
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted"})