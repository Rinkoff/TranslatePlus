import re
from DB.db import DB

def register_verification(username,password,email):
    """
    A function to verify the registration details of a user.

    Args:
    username (str): The desired username for the user.
    password (str): The desired password for the user.
    email (str): The email address of the user.

    Returns:
    A list containing the username, password, and email if all are valid.
    A string specifying which field failed validation (e.g. "username", "password", "email").
    """

    db = DB()
    usernames = db.select_usernames()
    data = []
    fail = ""

    if username not in usernames:
        data.append(username)
    else:
        fail = "username"
        return fail

    if len(password) > 7:
        data.append(password)
    else:
        fail = password
        return fail

    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    if re.fullmatch(email_regex, email):
        data.append(email)
    else:
        fail = email
        return fail

    if len(data) == 3:
        return data
