from models.skill import Skill
from models.internship import Internship
from models.internship_skill import InternshipSkill


def get_matching_internships(user):

    # Get all user skills
    user_skills = Skill.query.filter_by(user_id=user.id).all()

    # Convert to lowercase for case-insensitive comparison
    user_skill_names = {
        skill.name.strip().lower()
        for skill in user_skills
    }

    internships = Internship.query.all()

    recommendations = []

    for internship in internships:

        required_skills = InternshipSkill.query.filter_by(
            internship_id=internship.id
        ).all()

        required_names = [
            skill.skill_name
            for skill in required_skills
        ]

        matched = []
        missing = []

        for skill in required_names:

            if skill.lower() in user_skill_names:
                matched.append(skill)
            else:
                missing.append(skill)

        if len(required_names) == 0:
            match_percentage = 0
        else:
            match_percentage = int(
                (len(matched) / len(required_names)) * 100
            )


        if match_percentage >= 90:
            match_rank = "Legendary Match"

        elif match_percentage >= 75:
            match_rank = "Epic Match"

        elif match_percentage >= 50:
            match_rank = "Rare Match"

        elif match_percentage >= 25:
            match_rank = "Common Match"

        else:
            match_rank = "Training Required"
            
        recommendations.append({

            "internship": internship,

            "match_percentage": match_percentage,

            "matched_skills": matched,

            "missing_skills": missing,
            
            "internship": internship,

            "match_percentage": match_percentage,

            "match_rank": match_rank,

            "matched_skills": matched,

            "missing_skills": missing

        })

    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return recommendations