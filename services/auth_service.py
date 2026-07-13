from models.user import User
from database.database import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

def register_user(fullname, email, password, confirm_password):

    # Remove extra spaces
    fullname = fullname.strip()
    email = email.strip()

    # Validation
    if not fullname or not email or not password or not confirm_password:
        return  "Please fill all the fields."
    
    if password != confirm_password:
        return  "Passwords do not match."
    
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return "Email already registered."

    hashed_password=generate_password_hash(password)

    new_user = User(
        name=fullname,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return "Registration Successful!"

def login_user(email,password):
    email=email.strip().lower()
    user=User.query.filter_by(email=email).first()
    
    if not user :
        return False, "emial not registered" , None
    
    if not check_password_hash(user.password,password):
        return False, "incorrect password" , None
    
    return True,"login successful" , user