from flask import Blueprint, render_template,request
from services.auth_service import register_user
from flask import redirect, url_for, session
from services.auth_service import login_user

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

            return redirect(url_for("dashboard.home"))

        return message

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        
        fullname=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        con_pass=request.form.get("conf_password")
        
        message = register_user(
            fullname,
            email,
            password,
            con_pass
        )

        return message
    
    return render_template(
        "auth/login.html",
        mode="register"
    )    


@auth_bp.route("/setting")
def setting():
    return render_template("auth/settings.html")        