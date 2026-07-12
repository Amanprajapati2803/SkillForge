from flask import Blueprint, render_template
dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/home")
def home():
    return render_template("dashboard/home.html")



@dashboard_bp.route("/sessions")
def sessions():
    return render_template("dashboard/sessions.html")


@dashboard_bp.route("/rewards")
def rewards():
    return render_template("dashboard/rewards.html")


@dashboard_bp.route("/skills")
def skills():
    return render_template("dashboard/skills.html")


@dashboard_bp.route("/certify")
def certify():
    return render_template("dashboard/certificate.html")


@dashboard_bp.route("/community")
def community():
    return render_template("dashboard/community.html")


@dashboard_bp.route("/leaderboard")
def lead():
    return render_template("dashboard/leaderboard.html")