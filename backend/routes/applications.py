from flask import Blueprint
from flask import request
from flask import jsonify

from models import db
from models import Application
from models import Student

applications_bp = Blueprint(
    "applications",
    __name__
)


@applications_bp.route(
    "/apply",
    methods=["POST"]
)
def apply_job():

    data = request.json

    application = Application(
        student_id=data["student_id"],
        job_id=data["job_id"]
    )

    db.session.add(application)
    db.session.commit()

    return jsonify(
        {"message": "Applied Successfully"}
    )


@applications_bp.route(
    "/applications",
    methods=["GET"]
)
def view_applications():

    applications = Application.query.all()

    result = []

    for app in applications:

        result.append({

            "id": app.id,

            "student_id": app.student_id,

            "job_id": app.job_id,

            "status": app.status
        })

    return jsonify(result)
@applications_bp.route(
    "/job/<int:job_id>/applicants",
    methods=["GET"]
)
def applicants(job_id):

    applications = Application.query.filter_by(
        job_id=job_id
    ).all()

    result = []

    for application in applications:

        student = Student.query.get(
            application.student_id
        )

        result.append({

            "student_id":
            student.id,

            "name":
            student.name,

            "email":
            student.email,

            "cgpa":
            student.cgpa,

            "resume":
            student.resume,

            "status":
            application.status
        })

    return jsonify(result)