@auth_bp.route(
    "/student/register",
    methods=["POST"]
)
def student_register():

    data = request.json

    existing = Student.query.filter_by(
        email=data["email"]
    ).first()

    if existing:

        return jsonify({
            "message":
            "Email already exists"
        }), 400

    hashed = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    student = Student(

        name=data["name"],

        email=data["email"],

        password=hashed,

        branch=data.get("branch"),

        cgpa=data.get("cgpa"),

        skills=data.get("skills")
    )

    db.session.add(student)

    db.session.commit()

    return jsonify({
        "message":
        "Student Registered"
    })