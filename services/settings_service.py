from models.user import User
from database.database import db
from werkzeug.security import check_password_hash, generate_password_hash

import os
import time

from flask import current_app
from werkzeug.utils import secure_filename


def change_user_password(user_id, current_password, new_password, confirm_password):

    user = User.query.get(user_id)

    if not user:
        return False, "User not found."

    if not check_password_hash(user.password, current_password):
        return False, "Current password is incorrect."

    if new_password != confirm_password:
        return False, "New passwords do not match."

    if len(new_password) < 8:
        return False, "Password must be at least 8 characters."

    user.password = generate_password_hash(new_password)

    db.session.commit()

    return True, "Password changed successfully."


def toggle_two_factor(user_id):

    user = User.query.get(user_id)

    if not user:
        return False, "User not found.", None

    user.two_factor_enabled = not user.two_factor_enabled

    db.session.commit()

    return (
        True,
        "Two-factor authentication updated successfully.",
        user.two_factor_enabled
    )
    
def update_notification_preference(user_id, field, value):

    user = User.query.get(user_id)

    if not user:
        return False, "User not found."

    allowed_fields = {
        "notify_feed",
        "notify_sessions",
        "notify_digest",
        "notify_badges"
    }

    if field not in allowed_fields:
        return False, "Invalid notification type."

    setattr(user, field, value)

    db.session.commit()

    return True, "Notification preference updated."


SUPPORTED_PROVIDERS = {
    "google",
    "github",
    "linkedin"
}


def link_provider(user_id, provider):

    user = User.query.get(user_id)

    if not user:
        return False, "User not found."

    if provider not in SUPPORTED_PROVIDERS:
        return False, "Invalid provider."

    setattr(user, f"{provider}_linked", True)

    db.session.commit()

    return True, f"{provider.title()} account linked successfully."


def unlink_provider(user_id, provider):

    user = User.query.get(user_id)

    if not user:
        return False, "User not found."

    if provider not in SUPPORTED_PROVIDERS:
        return False, "Invalid provider."

    setattr(user, f"{provider}_linked", False)

    db.session.commit()

    return True, f"{provider.title()} account unlinked successfully."


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )
    
def update_avatar(user_id, avatar):

    if not avatar or avatar.filename == "":
        return False, "No image selected."

    if not allowed_file(avatar.filename):
        return False, "Only PNG, JPG, JPEG, GIF and WEBP files are allowed."

    user = User.query.get(user_id)

    extension = avatar.filename.rsplit(".", 1)[1].lower()

    filename = secure_filename(
        f"user_{user.id}_{int(time.time())}.{extension}"
    )

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "profile"
    )

    os.makedirs(upload_folder, exist_ok=True)

    if user.avatar:

        old_avatar = os.path.join(
            upload_folder,
            user.avatar
        )

        if os.path.exists(old_avatar):
            os.remove(old_avatar)

    avatar.save(
        os.path.join(upload_folder, filename)
    )

    user.avatar = filename

    return True, "Avatar updated successfully."