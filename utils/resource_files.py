from pathlib import Path
from uuid import uuid4

from flask import current_app
from werkzeug.utils import secure_filename


def upload_directory():
    directory = Path(current_app.instance_path) / "learning_resources"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def store_resource_file(payload, original_filename):
    safe_name = secure_filename(original_filename or "resource") or "resource"
    suffix = Path(safe_name).suffix.lower()[:12]
    key = f"{uuid4().hex}{suffix}"
    (upload_directory() / key).write_bytes(payload)
    return key, safe_name


def resource_file_path(key):
    # Only generated basenames are accepted; never trust a path from a DB row.
    safe_key = Path(key or "").name
    if not safe_key or safe_key != key:
        return None
    path = upload_directory() / safe_key
    return path if path.is_file() else None
