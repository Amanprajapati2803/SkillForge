from flask import Blueprint, render_template

internship_bp = Blueprint("internship", __name__)

@internship_bp.route("/interns")
def interns():
    return render_template("dashboard/internship.html")