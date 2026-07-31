from flask import Blueprint, render_template,request,session,flash
from services.auth_service import register_user
from flask import redirect, url_for, session
from services.auth_service import login_user
from services.user_service import get_user

# from services.challenge_service import ensure_daily_challenges

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        success, message, user = login_user(email, password)

        if success:

            session["user_id"] = user.id
            session["user_name"] = user.name
            
             # Generate today's challenges if they don't exist
            # ensure_daily_challenges(user.id)

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