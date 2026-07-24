from flask import Blueprint, render_template,session,request,redirect,url_for
from utils.auth import login_required
from utils.internship_matcher import get_matching_internships
from models.user import User
from database.database import db
from models.applied_internship import AppliedInternship

internship_bp = Blueprint("internship", __name__)

@internship_bp.route("/internships")
@login_required
def interns():

    user = User.query.get(session["user_id"])
    
    recommendations = get_matching_internships(user)

    search = request.args.get("search", "").lower()
    internship_type = request.args.get("type", "")
    min_match = request.args.get("match", type=int)

    filtered = []

    for item in recommendations:

        internship = item["internship"]

        # Search
        if search:
            if (
                search not in internship.company.lower()
                and search not in internship.title.lower()
            ):
                continue

        # Type Filter
        if internship_type:
            if internship.internship_type != internship_type:
                continue

        # Match Filter
        if min_match is not None:
            if item["match_percentage"] < min_match:
                continue

        filtered.append(item)
        
    total_scrolls = len(filtered)

    legendary_matches = len([
        item for item in filtered
        if item["match_percentage"] >= 90
    ])

    epic_matches = len([
        item for item in filtered
        if 75 <= item["match_percentage"] < 90
    ])

    average_match = 0

    if total_scrolls > 0:
        average_match = sum(
            item["match_percentage"]
            for item in filtered
        ) // total_scrolls

    return render_template(
        "dashboard/internship.html",
        recommendations=filtered,
        total_scrolls=total_scrolls,
        legendary_matches=legendary_matches,
        epic_matches=epic_matches,
        average_match=average_match
    )


@internship_bp.route("/apply/<int:internship_id>")
@login_required
def apply_internship(internship_id):

    existing = AppliedInternship.query.filter_by(
        user_id=session["user_id"],
        internship_id=internship_id
    ).first()

    if existing:
        return redirect(url_for("internship.interns"))

    application = AppliedInternship(
        user_id=session["user_id"],
        internship_id=internship_id
    )

    db.session.add(application)
    db.session.commit()

    return redirect(url_for("internship.interns"))

@internship_bp.route("/applications")
@login_required
def applications():

    applications = AppliedInternship.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        AppliedInternship.applied_at.desc()
    ).all()

    return render_template(
        "dashboard/applications.html",
        applications=applications
    )
    
# @internship_bp.route("/application/<int:application_id>")
# @login_required
# def application_details(application_id):

#     application = AppliedInternship.query.filter_by(
#         id=application_id,
#         user_id=session["user_id"]
#     ).first_or_404()

#     return render_template(
#         "dashboard/application_details.html",
#         application=application
#     )