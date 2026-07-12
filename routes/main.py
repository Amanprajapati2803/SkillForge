from flask import Blueprint,render_template

main_bp = Blueprint("main", __name__)

from flask import Blueprint

main_bp = Blueprint("main", __name__)


# @main_bp.route("/")
# def index():
#     return "SkillForge Backend Running 🚀"

@main_bp.route("/")
def landing():
    return render_template("dashboard/landing.html")

@main_bp.route("/realm")
def realm():
    return render_template("realm.html")