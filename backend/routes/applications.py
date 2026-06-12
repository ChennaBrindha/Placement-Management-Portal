from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Application, Student, Job
from routes.rbac import role_required
from datetime import datetime

applications_bp = Blueprint("applications", __name__, url_prefix="/api/applications")

VALID_STATUSES = ["Applied", "Shortlisted", "Interview Scheduled", "Rejected", "Selected"]


@applications_bp.route("/apply", methods=["POST"])
@jwt_required()
def apply_job():
    data = request.json
    student_id = data.get("student_id")
    job_id = data.get("job_id")

    if not student_id or not job_id:
        return jsonify({"message": "student_id and job_id required"}), 400

    student = Student.query.get(student_id)
    job = Job.query.get(job_id)

    if not student:
        return jsonify({"message": "Student not found"}), 404
    if not job:
        return jsonify({"message": "Job not found"}), 404
    if not job.is_active:
        return jsonify({"message": "Job is no longer active"}), 400
    if job.eligibility_cgpa and student.cgpa and student.cgpa < job.eligibility_cgpa:
        return jsonify({"message": f"Minimum CGPA {job.eligibility_cgpa} required"}), 400

    # prevent duplicate
    existing = Application.query.filter_by(student_id=student_id, job_id=job_id).first()
    if existing:
        return jsonify({"message": "Already applied to this job"}), 409

    application = Application(student_id=student_id, job_id=job_id)
    db.session.add(application)
    db.session.commit()
    return jsonify({"message": "Applied successfully", "application": application.to_dict()}), 201


@applications_bp.route("/student/<int:student_id>", methods=["GET"])
@jwt_required()
def student_applications(student_id):
    """All applications for a student, with job details."""
    apps = Application.query.filter_by(student_id=student_id).all()
    result = []
    for app in apps:
        job = Job.query.get(app.job_id)
        entry = app.to_dict()
        if job:
            entry["job_title"] = job.title
            entry["company_name"] = job.company.company_name if job.company else ""
            entry["location"] = job.location
            entry["package"] = job.package
        result.append(entry)
    return jsonify(result)


@applications_bp.route("/job/<int:job_id>/applicants", methods=["GET"])
@role_required("admin")
def job_applicants(job_id):
    """Admin: all applicants for a specific job."""
    apps = Application.query.filter_by(job_id=job_id).all()
    result = []
    for app in apps:
        student = Student.query.get(app.student_id)
        entry = app.to_dict()
        if student:
            entry["student_name"] = student.name
            entry["student_email"] = student.email
            entry["cgpa"] = student.cgpa
            entry["department"] = student.department
            entry["resume"] = student.resume
        result.append(entry)
    return jsonify(result)


@applications_bp.route("/<int:application_id>/status", methods=["PUT"])
@role_required("admin")
def update_status(application_id):
    """Admin: update application status."""
    app = Application.query.get_or_404(application_id)
    data = request.json
    new_status = data.get("status")

    if new_status not in VALID_STATUSES:
        return jsonify({"message": f"Status must be one of: {VALID_STATUSES}"}), 400

    app.status = new_status

    if new_status == "Interview Scheduled" and data.get("interview_date"):
        try:
            app.interview_date = datetime.fromisoformat(data["interview_date"])
        except ValueError:
            return jsonify({"message": "Invalid interview_date format"}), 400

    if new_status == "Selected":
        student = Student.query.get(app.student_id)
        if student:
            student.is_placed = True

    db.session.commit()
    return jsonify({"message": "Status updated", "application": app.to_dict()})


@applications_bp.route("/all", methods=["GET"])
@role_required("admin")
def all_applications():
    apps = Application.query.all()
    result = []
    for app in apps:
        entry = app.to_dict()
        student = Student.query.get(app.student_id)
        job = Job.query.get(app.job_id)
        if student:
            entry["student_name"] = student.name
        if job:
            entry["job_title"] = job.title
            entry["company_name"] = job.company.company_name if job.company else ""
        result.append(entry)
    return jsonify(result)