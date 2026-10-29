from flask import Blueprint, render_template,request,session,flash,current_app
from authlib.integrations.flask_client import OAuth

from models.user import User
from database.database import db
from services.auth_service import register_user
from flask import redirect, url_for, session
from services.auth_service import login_user
from services.user_service import get_user

# from services.challenge_service import ensure_daily_challenges

auth_bp = Blueprint("auth", __name__)

oauth=OAuth()

@auth_bp.route("/auth/google")
def google_login():
    redirect_uri = url_for("auth.google_callback", _external=True)
    return oauth.create_client("google").authorize_redirect(
        redirect_uri
    )


@auth_bp.route("/auth/google/callback")
def google_callback():
    google = oauth.create_client("google")

    token = google.authorize_access_token()

    user_info = token.get("userinfo")

    if not user_info:
        flash("Could not get information from Google.", "error")
        return redirect(url_for("auth.login"))

    google_email = user_info.get("email")
    google_name = user_info.get("name")

    if not google_email:
        flash("Google did not provide an email address.", "error")
        return redirect(url_for("auth.login"))

    # Check if this email already exists in SkillForge
    user = User.query.filter_by(email=google_email.lower()).first()

    if user:
        # Existing SkillForge account
        user.google_linked = True

    else:
        # Create a new SkillForge account
        user = User(
            name=google_name or "SkillForge User",
            email=google_email.lower(),
            password=None,
            google_linked=True
        )

        db.session.add(user)

    db.session.commit()

    # Create SkillForge session
    session["user_id"] = user.id
    session["user_name"] = user.name

    return redirect(url_for("dashboard.home"))


@auth_bp.route("/auth/github")
def github_login():
    redirect_uri = url_for("auth.github_callback", _external=True)

    return oauth.create_client("github").authorize_redirect(
        redirect_uri
    )


@auth_bp.route("/auth/github/callback")
def github_callback():
    github = oauth.create_client("github")

    token = github.authorize_access_token()

    response = github.get("user")

    if not response.ok:
        flash("Could not get information from GitHub.", "error")
        return redirect(url_for("auth.login"))

    github_user = response.json()

    github_name = github_user.get("name") or github_user.get("login")
    github_id = github_user.get("id")

    # Get the user's email
    email_response = github.get("user/emails")

    if not email_response.ok:
        flash("Could not get your GitHub email.", "error")
        return redirect(url_for("auth.login"))

    emails = email_response.json()

    github_email = None

    for email in emails:
        if email.get("primary") and email.get("verified"):
            github_email = email.get("email")
            break

    if not github_email:
        flash("No verified GitHub email was found.", "error")
        return redirect(url_for("auth.login"))

    # Find existing SkillForge user
    user = User.query.filter_by(
        email=github_email.lower()
    ).first()

    if user:
        # Existing account
        user.github_linked = True

    else:
        # New GitHub account
        user = User(
            name=github_name or "SkillForge User",
            email=github_email.lower(),
            password=None,
            github_linked=True
        )

        db.session.add(user)

    db.session.commit()

    # Create SkillForge session
    session["user_id"] = user.id
    session["user_name"] = user.name

    return redirect(url_for("dashboard.home"))

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

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have signed out.", "info")
    return redirect(url_for("auth.login"))
