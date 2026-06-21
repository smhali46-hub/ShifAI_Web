from pathlib import Path
import re


USERS_DIR = Path("users")
USERS_DIR.mkdir(exist_ok=True)

CURRENT_USER_FILE = USERS_DIR / "current_user.txt"


def safe_name(name):
    name = name.strip()
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    return name or "Guest"


def set_current_user(username):
    username = safe_name(username)
    CURRENT_USER_FILE.write_text(username)
    return username


def get_current_user():
    if CURRENT_USER_FILE.exists():
        return CURRENT_USER_FILE.read_text().strip()
    return "Guest"


def get_progress_file():
    username = get_current_user()
    return USERS_DIR / f"{username}_progress.csv"


def logout_user():
    if CURRENT_USER_FILE.exists():
        CURRENT_USER_FILE.unlink()