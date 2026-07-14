from models.user import User

def get_user(user_id):
    
    return User.query.get(user_id)