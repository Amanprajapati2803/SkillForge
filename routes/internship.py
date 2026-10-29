from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from utils.auth import login_required
from utils.internship_matcher import get_matching_internships
from utils.achievements import check_achievements
from models.user import User
from models.internship import Internship
from database.database import db
from models.applied_internship import AppliedInternship
from services.skill_progress import get_skill_progress

internship_bp = Blueprint("internship", __name__)


@internship_bp.route("/internships")
@login_required
def interns():
    user = User.query.get(session["user_id"])
    if not user:
        return redirect(url_for("auth.login"))

    # Get raw recommendations (works even with 0 user skills)
    recommendations = get_matching_internships(user)

    # Read filters
    search = request.args.get("search", "").strip().lower()
    internship_type = request.args.get("type", "")
    min_match = request.args.get("match", type=int)

    filtered = []
    for item in recommendations:
        internship = item["internship"]

        # Search filter
        if search:
            search_in_company = search in internship.company.lower()
            search_in_title = search in internship.title.lower()
            search_in_desc = search in internship.description.lower()
            if not (search_in_company or search_in_title or search_in_desc):
                continue

        # Type filter
        if internship_type:
            if internship.internship_type != internship_type:
                continue

        # Match % filter
        if min_match is not None:
            if item["match_percentage"] < min_match:
                continue

        filtered.append(item)

    # Stats (computed on filtered set so they react to filters)
    total_scrolls = len(filtered)
    legendary_matches = len([i for i in filtered if i["match_percentage"] >= 90])
    epic_matches = len([i for i in filtered if 75 <= i["match_percentage"] < 90])
    average_match = 0
    if total_scrolls > 0:
        average_match = sum(i["match_percentage"] for i in filtered) // total_scrolls

    # Share the same transparent evidence calculation used by the skills pages.
    evidence_by_skill = get_skill_progress(user.id)
    user_skills = sorted(
        user.skills,
        key=lambda skill: evidence_by_skill.get(skill.id, {}).get("percent", 0),
        reverse=True,
    )[:3]
    skill_progress = []
    for skill in user_skills:
        evidence = evidence_by_skill.get(skill.id, {})
        skill_progress.append({
            "name": skill.name,
            "pct": evidence.get("percent", 0),
            "demonstrated": evidence.get("demonstrated", False),
            "best_accuracy": evidence.get("best_accuracy", 0),
            "attempts": evidence.get("attempts", 0),
        })

    return render_template(
        "dashboard/internship.html",
        user=user,
        recommendations=filtered,
        total_scrolls=total_scrolls,
        legendary_matches=legendary_matches,
        epic_matches=epic_matches,
        average_match=average_match,
        skill_progress=skill_progress,
        has_skills=len(user.skills) > 0,
        filter_search=request.args.get("search", ""),
        filter_type=request.args.get("type", ""),
        filter_match=request.args.get("match", ""),
    )


@internship_bp.route("/apply/<int:internship_id>", methods=["POST"])
@login_required
def apply_internship(internship_id):
    user = User.query.get(session["user_id"])
    if not user:
        return redirect(url_for("auth.login"))

    internship = Internship.query.get(internship_id)
    if not internship:
        flash("Recruitment Scroll not found.", "error")
        return redirect(url_for("internship.interns"))

    existing = AppliedInternship.query.filter_by(
        user_id=session["user_id"],
        internship_id=internship_id
    ).first()

    if existing:
        flash("You have already tracked this application.", "info")
        return redirect(url_for("internship.interns"))

    application = AppliedInternship(
        user_id=session["user_id"],
        internship_id=internship_id,
        status="Applied"
    )
    db.session.add(application)
    db.session.commit()

    check_achievements(user)

    flash(f"Application saved: {internship.company} — {internship.title}", "success")

    # The application row is saved first, then the listing's apply portal opens.
    return redirect(internship.apply_link)


@internship_bp.route("/applications/<int:application_id>/status", methods=["POST"])
@login_required
def update_application_status(application_id):
    application = AppliedInternship.query.filter_by(
        id=application_id, user_id=session["user_id"]
    ).first_or_404()
    allowed_statuses = {"Applied", "Under Review", "Interview", "Accepted", "Rejected"}
    status = request.form.get("status", "Applied").strip()
    if status not in allowed_statuses:
        flash("Choose a valid application status.", "error")
    else:
        application.status = status
        db.session.commit()
        flash("Application status updated.", "success")
    return redirect(url_for("internship.applications"))


@internship_bp.route("/applications")
@login_required
def applications():
    applications = (
        AppliedInternship.query.filter_by(user_id=session["user_id"])
        .order_by(AppliedInternship.applied_at.desc())
        .all()
    )
    return render_template(
        "dashboard/applications.html",
        applications=applications
    )