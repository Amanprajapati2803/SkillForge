from flask import Blueprint, session, render_template,request,url_for,redirect
from models.skill import Skill
from utils.auth import login_required
from database.database import db
from models.user import User
from utils.progression import award_skill_xp, award_user_xp

skills_bp = Blueprint("skills", __name__)

@skills_bp.route("/skills", methods=["GET", "POST"])
@login_required
def skills():

    if request.method == "POST":

        skill_name = request.form.get("skill_name")

        new_skill = Skill(
            name=skill_name,
            user_id=session["user_id"]
        )

        db.session.add(new_skill)
        db.session.commit()

        return redirect(url_for("skills.skills"))

    skills = Skill.query.filter_by(
        user_id=session["user_id"]
    ).all()
    
    return render_template(
        "dashboard/skills.html",
        skills=skills
    )
    
@skills_bp.route("/skills/delete/<int:skill_id>", methods=["POST"])
@login_required
def delete_skill(skill_id):
    
    skill = Skill.query.filter_by(
        id=skill_id,
        user_id=session["user_id"]
    ).first()

    if skill:

        db.session.delete(skill)
        db.session.commit()

    return redirect(url_for("skills.skills"))


@skills_bp.route("/edit/<int:skill_id>", methods=["POST"])
@login_required
def edit_skill(skill_id):

    skill = Skill.query.filter_by(
        id=skill_id,
        user_id=session["user_id"]
    ).first_or_404()

    skill.name = request.form["skill_name"]

    db.session.commit()

    return redirect(url_for("skills.skills"))

# routes/skill.py

@skills_bp.route("/skills/<int:skill_id>/add-xp", methods=["POST"])
@login_required
def add_skill_xp(skill_id):
    
    skill = Skill.query.get_or_404(skill_id)

    award_skill_xp(skill, 10)

    activity = award_user_xp(
        skill.user,
        10,
        f"Practiced {skill.name}"
    )
    db.session.add(activity)

    db.session.commit()

    return redirect(url_for("dashboard.home"))
