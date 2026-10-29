from flask import Flask

from config import Config
from database.database import db


# Import models
from models.user import User
from models.learning_session import LearningSession
from models.learning_game import LearningGame, LearningGameProgress, LearningGameMatch

from routes.main import main_bp
from routes.auth import auth_bp, oauth
from routes.dashboard import dashboard_bp
from routes.learning import learning_bp
from routes.learning_game import learning_game_bp
from routes.internship import internship_bp
from routes.skill import skills_bp
from routes.settings import setting_bp

from routes.achievement import achievement_bp

from flask_migrate import Migrate

from routes.community import community_bp
# from seeders.achievement_seeder import seed_achievements
# from seeders.internships_seeder import seed_internships
# from seeders.resources_seeder import seed_resources
#from seeders.sessions_seeder import seed_sessionsfrom routes.community import community_bp

app = Flask(__name__)

app.config.from_object(Config)

# OAuth
oauth.init_app(app)

oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)

oauth.register(
    name="github",
    client_id=app.config["GITHUB_CLIENT_ID"],
    client_secret=app.config["GITHUB_CLIENT_SECRET"],
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={
        "scope": "read:user user:email"
    }
)

db.init_app(app)

migrate=Migrate(app,db)

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(learning_game_bp)
app.register_blueprint(internship_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(achievement_bp)
app.register_blueprint(setting_bp)
app.register_blueprint(community_bp)


with app.app_context():
    db.create_all() 
    # seed_achievements()
    # seed_internships()
    # seed_resources()
    #seed_sessions()

if __name__ == "__main__":
    app.run(debug=True)
