from flask import Blueprint,request,render_template,session,redirect,url_for,flash,jsonify
from database.database import db
from utils.auth import login_required
from models.user import User
from models.skill import Skill
from models.activity_log import ActivityLog
from services.settings_service import change_user_password,toggle_two_factor as toggle_two_factor_services,update_notification_preference,link_provider,unlink_provider,update_avatar


setting_bp = Blueprint("settings", __name__)

@setting_bp.route("/setting")
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
    
@setting_bp.route("/setting/edit", methods=["POST"])
@login_required
def edit_profile():

    user = User.query.get(session["user_id"])
    
    user.name = request.form["name"]
    user.college = request.form["college"]
    user.bio = request.form["bio"]

    avatar = request.files.get("avatar")

    if avatar and avatar.filename:

        success, message = update_avatar(
            user.id,
            avatar
        )

        if not success:
            flash(message, "error")
            return redirect(url_for("settings.setting"))
    
    db.session.commit()

    flash("Profile updated successfully!", "success")

    return redirect(url_for("settings.setting"))   


@setting_bp.route("/setting/password", methods=["POST"])
@login_required
def change_password():
    data = request.get_json()

    success, message = change_user_password(
        session["user_id"],
        data.get("current_password"),
        data.get("new_password"),
        data.get("confirm_password")
    )

    if success:
        return jsonify({
            "success": True,
            "message": message
        })

    return jsonify({
        "success": False,
        "message": message
    }), 400


@setting_bp.route("/setting/two-factor", methods=["POST"])
@login_required
def toggle_two_factor():
    success, message, enabled = toggle_two_factor_services(session["user_id"])

    if success:
        return jsonify({
            "success": True,
            "message": message,
            "enabled": enabled
        })

    return jsonify({
        "success": False,
        "message": message
    }), 400

@setting_bp.route("/setting/notifications", methods=["POST"])
@login_required
def update_notifications():
    
    data = request.get_json()

    success, message = update_notification_preference(
        session["user_id"],
        data.get("field"),
        data.get("value")
    )

    if success:
        return jsonify({
            "success": True,
            "message": message
        })

    return jsonify({
        "success": False,
        "message": message
    }), 400

@setting_bp.route("/setting/appearance", methods=["POST"])
@login_required
def update_appearance():
    pass
    
@setting_bp.route("/setting/avatar", methods=["POST"])
@login_required
def upload_avatar():
    pass

@setting_bp.route("/setting/link/<provider>", methods=["POST"])
@login_required
def link_account(provider):

    success, message = link_provider(
        session["user_id"],
        provider
    )

    return jsonify({
        "success": success,
        "message": message
    })
    
@setting_bp.route("/setting/<provider>/callback")
@login_required
def oauth_callback(provider):
    pass

@setting_bp.route("/setting/unlink/<provider>", methods=["POST"])
@login_required
def unlink_account(provider):

    success, message = unlink_provider(
        session["user_id"],
        provider
    )

    return jsonify({
        "success": success,
        "message": message
    })