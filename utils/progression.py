from models.activity_log import ActivityLog
def calculate_level(xp):

    return (xp // 100) + 1

def award_user_xp(user, amount,description):

    user.xp += amount
    user.level = calculate_level(user.xp)
    
    activity = ActivityLog(
        user=user,
        description=description,
        xp_earned=amount
    )

    return activity
    

def award_skill_xp(skill, amount):

    skill.xp += amount
    skill.level = calculate_level(skill.xp)    