from flask import g
from flask_httpauth import HTTPBasicAuth

import models

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_username, password):
    try:
        user = models.User.get(
            (models.User.username == email_or_username) |
            (models.User.email == email_or_username)
        )
        if not user.verify_password(password):
            return False
    except models.User.DoesNotExist:
        return False
    else:
        g.user = user
        return True

