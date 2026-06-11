from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(255)
    )

    branch = db.Column(
        db.String(50)
    )

    cgpa = db.Column(
        db.Float
    )

    skills = db.Column(
        db.Text
    )

    resume = db.Column(
        db.String(255)
    )


class Company(db.Model):

    __tablename__ = "companies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_name = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(255)
    )


class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100)
    )

    package = db.Column(
        db.Float
    )

    description = db.Column(
        db.Text
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id')
    )


class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id')
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey('jobs.id')
    )

    status = db.Column(
        db.String(30),
        default="Applied"
    )