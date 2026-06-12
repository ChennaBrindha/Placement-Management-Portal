from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")  # student | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    graduation_year = db.Column(db.Integer)
    skills = db.Column(db.Text)
    resume = db.Column(db.String(255))
    is_placed = db.Column(db.Boolean, default=False)
    applications = db.relationship("Application", backref="student", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "cgpa": self.cgpa,
            "graduation_year": self.graduation_year,
            "skills": self.skills,
            "resume": self.resume,
            "is_placed": self.is_placed,
        }


class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(100))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    jobs = db.relationship("Job", backref="company", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "company_name": self.company_name,
            "email": self.email,
            "industry": self.industry,
            "website": self.website,
            "description": self.description,
        }


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    package = db.Column(db.String(50))
    eligibility_cgpa = db.Column(db.Float, default=0.0)
    skills_required = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    job_type = db.Column(db.String(50))  # Full-time | Internship
    is_active = db.Column(db.Boolean, default=True)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship("Application", backref="job", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "company_name": self.company.company_name if self.company else "",
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "package": self.package,
            "eligibility_cgpa": self.eligibility_cgpa,
            "skills_required": self.skills_required,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "job_type": self.job_type,
            "is_active": self.is_active,
            "posted_at": self.posted_at.isoformat() if self.posted_at else None,
        }


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    status = db.Column(db.String(30), default="Applied")  # Applied | Shortlisted | Rejected | Selected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    interview_date = db.Column(db.DateTime)
    offer_letter = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "job_id": self.job_id,
            "status": self.status,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
            "interview_date": self.interview_date.isoformat() if self.interview_date else None,
            "offer_letter": self.offer_letter,
        }