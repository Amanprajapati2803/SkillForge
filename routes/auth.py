from flask import Blueprint, render_template,request,session,flash
from services.auth_service import register_user
from flask import redirect, url_for, session
from services.auth_service import login_user
from services.user_service import get_user
from utils.auth import login_required
from models.user import User
from database.database import db
from models.skill import Skill
from models.activity_log import ActivityLog

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
@login_required
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        success, message, user = login_user(email, password)

        if success:

            session["user_id"] = user.id
            session["user_name"] = user.name

            return redirect(url_for("dashboard.home"))

        return message

    user = None

    if "user_id" in session:
        user = get_user(session["user_id"])

    return render_template(
        "auth/login.html",
        user=user
    )



@auth_bp.route("/register", methods=["GET","POST"])
@login_required
def register():
    if request.method=="POST":
        
        fullname=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        con_pass=request.form.get("conf_password")
        
        register_user(
            fullname,
            email,
            password,
            con_pass
        )
    
    return render_template(
        "auth/login.html",
        mode="register"
    )    


@auth_bp.route("/setting")
@login_required
def setting():
    
    user = User.query.get(session["user_id"])
    
    skill_count = Skill.query.filter_by(user_id=user.id).count()
    
    recent_activities = (
        ActivityLog.query
        .filter_by(user_id=user.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(2)
        .all()
    )
    
    return render_template(
        "auth/settings.html",
        user=user,
        skill_count=skill_count,
        recent_activities=recent_activities
    )     
    
@auth_bp.route("/setting/edit", methods=["POST"])
@login_required
def edit_profile():

    user = User.query.get(session["user_id"])
    
    user.name = request.form["name"]
    user.college = request.form["college"]
    user.bio = request.form["bio"]

    db.session.commit()

    flash("Profile updated successfully!", "success")

    return redirect(url_for("auth.setting"))   