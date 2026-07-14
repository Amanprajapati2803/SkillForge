from flask import Flask, render_template
from routes.main import main_bp


app = Flask(__name__)

from config import Config
from database.database import db

# Import models
from models.user import User
from routes.main import main_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.learning import learning_bp
from routes.internship import internship_bp
from routes.skills import skills_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(internship_bp)
app.register_blueprint(skills_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
