from flask import Blueprint, session, render_template, request, url_for, redirect
from models import user
from models.skill import Skill
from models.resources import Resource
from utils.auth import login_required
from database.database import db
from utils.progression import award_skill_xp, award_user_xp
from services.resources_service import get_skill_resources
from models.user import User
from services.achievement_service import unlock_achievement
from services.challenge_service import update_challenge_progress
from utils.achievements import check_achievements

skills_bp = Blueprint("skills", __name__)


@skills_bp.route("/skills", methods=["GET", "POST"])
@login_required
def skills():

    if request.method == "POST":

        skill_name = request.form.get("skill_name")

        new_skill = Skill(name=skill_name, user_id=session["user_id"])

        db.session.add(new_skill)
        db.session.commit()
        
        check_achievements(user)
        
        update_challenge_progress(
            session["user_id"],
            "Skill Builder"
        )
        
        unlock_achievement(session["user_id"], "First Step")

        return redirect(url_for("skills.skills"))

    skills = Skill.query.filter_by(user_id=session["user_id"]).all()

    return render_template("dashboard/skills.html", skills=skills)


@skills_bp.route("/skills/delete/<int:skill_id>", methods=["POST"])
@login_required
def delete_skill(skill_id):

    skill = Skill.query.filter_by(id=skill_id, user_id=session["user_id"]).first()

    if skill:

        db.session.delete(skill)
        db.session.commit()

    return redirect(url_for("skills.skills"))


@skills_bp.route("/edit/<int:skill_id>", methods=["POST"])
@login_required
def edit_skill(skill_id):

    skill = Skill.query.filter_by(
        id=skill_id, user_id=session["user_id"]
    ).first_or_404()

    skill.name = request.form["skill_name"]

    db.session.commit()

    return redirect(url_for("skills.skills"))


# routes/skill.py


@skills_bp.route("/skills/<int:skill_id>/add-xp", methods=["POST"])
@login_required
def add_skill_xp(skill_id):

    skill = Skill.query.filter_by(
        id=skill_id, user_id=session["user_id"]
    ).first_or_404()

    award_skill_xp(skill, 10)

    activity = award_user_xp(skill.user, 10, f"Practiced {skill.name}")
    db.session.add(activity)

    db.session.commit()
    


    return redirect(url_for("dashboard.home"))


# resources routes


@skills_bp.route("/skills/<int:skill_id>")
@login_required
def skill_realm(skill_id):

    skill = Skill.query.filter_by(
        id=skill_id,
        user_id=session["user_id"]
    ).first_or_404()

    resources = get_skill_resources(skill.id)

    sessions = sorted(
        skill.sessions,
        key=lambda s: s.id,
        reverse=True
    )

    return render_template(
        "dashboard/skill_realm.html",
        skill=skill,
        resources=resources,
        sessions=sessions
    )


# @skills_bp.route("/skills/<int:skill_id>/resources/add", methods=["POST"])
# @login_required
# def add_resource(skill_id):

#     skill = Skill.query.filter_by(
#         id=skill_id, user_id=session["user_id"]
#     ).first_or_404()

#     create_resource(
#         skill_id=skill.id,
#         title=request.form.get("title"),
#         resource_type=request.form.get("resource_type"),
#         url=request.form.get("url"),
#         description=request.form.get("description"),
#     )

#     update_challenge_progress(
#         User.id,
#         "Resource Collector"
#     )
#     return redirect(url_for("skills.skill_realm", skill_id=skill.id))


# @skills_bp.route("/resources/<int:resource_id>/delete", methods=["POST"])
# @login_required
# def delete_resource_route(resource_id):

#     resource = Resource.query.get_or_404(resource_id)

#     skill = Skill.query.filter_by(
#         id=resource.skill_id, user_id=session["user_id"]
#     ).first_or_404()

#     delete_resource(resource)

#     return redirect(url_for("skills.skill_realm", skill_id=skill.id))


# @skills_bp.route("/resources/<int:resource_id>/edit", methods=["POST"])
# @login_required
# def edit_resource(resource_id):

#     resource = Resource.query.get_or_404(resource_id)

#     skill = Skill.query.filter_by(
#         id=resource.skill_id, user_id=session["user_id"]
#     ).first_or_404()

#     update_resource(
#         resource=resource,
#         title=request.form.get("title"),
#         resource_type=request.form.get("resource_type"),
#         url=request.form.get("url"),
#         description=request.form.get("description"),
#     )

#     return redirect(url_for("skills.skill_realm", skill_id=skill.id))


