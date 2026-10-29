from models.internship import Internship
from models.internship_skill import InternshipSkill
from models.learning_game import LearningGame, LearningGameProgress
from models.skill import Skill


def get_matching_internships(user):
    user_skills = Skill.query.filter_by(user_id=user.id).all()
    skills_by_name = {skill.name.strip().casefold(): skill for skill in user_skills}
    game_ids = [game.id for game in LearningGame.query.join(Skill).filter(Skill.user_id == user.id).all()]
    demonstrated_skill_ids = set()
    if game_ids:
        passed = LearningGameProgress.query.filter(
            LearningGameProgress.user_id == user.id,
            LearningGameProgress.game_id.in_(game_ids),
            LearningGameProgress.quiz_passed.is_(True),
        ).all()
        passed_game_ids = {item.game_id for item in passed}
        demonstrated_skill_ids = {
            game.skill_id for game in LearningGame.query.filter(LearningGame.id.in_(passed_game_ids)).all()
        }

    recommendations = []
    for internship in Internship.query.all():
        required_names = [item.skill_name.strip() for item in InternshipSkill.query.filter_by(internship_id=internship.id).all()]
        demonstrated, developing, missing = [], [], []
        for required in required_names:
            skill = skills_by_name.get(required.casefold())
            if skill and skill.id in demonstrated_skill_ids:
                demonstrated.append(required)
            elif skill:
                developing.append(required)
            else:
                missing.append(required)

        match_percentage = round(len(demonstrated) / len(required_names) * 100) if required_names else 0
        if match_percentage >= 90:
            match_rank = "Strong Evidence"
        elif match_percentage >= 60:
            match_rank = "Good Evidence"
        elif demonstrated or developing:
            match_rank = "Building Skills"
        else:
            match_rank = "Start Learning"

        recommendations.append({
            "internship": internship,
            "match_percentage": match_percentage,
            "match_rank": match_rank,
            "matched_skills": demonstrated,
            "developing_skills": developing,
            "missing_skills": missing,
        })

    recommendations.sort(key=lambda item: (item["match_percentage"], len(item["developing_skills"])), reverse=True)
    return recommendations
