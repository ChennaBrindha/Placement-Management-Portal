from flask import Blueprint
from flask import request
from flask import jsonify

from models import db
from models import Job

jobs_bp = Blueprint(
    "jobs",
    __name__
)


@jobs_bp.route(
    "/jobs",
    methods=["GET"]
)
def get_jobs():

    jobs = Job.query.all()

    result = []

    for job in jobs:

        result.append({

            "id": job.id,

            "title": job.title,

            "package": job.package,

            "description": job.description
        })

    return jsonify(result)


@jobs_bp.route(
    "/jobs",
    methods=["POST"]
)
def create_job():

    data = request.json

    job = Job(

        title=data["title"],

        package=data["package"],

        description=data["description"],

        company_id=data["company_id"]
    )

    db.session.add(job)

    db.session.commit()

    return jsonify(
        {"message": "Job Created"}
    )