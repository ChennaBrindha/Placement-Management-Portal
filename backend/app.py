from flask import Flask

from flask_jwt_extended import JWTManager

from flask_cors import CORS

from config import Config

from models import db

from routes.auth import auth_bp
from routes.jobs import jobs_bp
from routes.company import company_bp
from routes.upload import upload_bp
from routes.applications import applications_bp



app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)

CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(jobs_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():

    return {
        "message":
        "Placement Portal Running"
    }


app.register_blueprint(company_bp)

app.register_blueprint(upload_bp)

app.register_blueprint(applications_bp)
if __name__ == "__main__":
    app.run(debug=True)