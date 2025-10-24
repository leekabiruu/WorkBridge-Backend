from ..models.user import User
from ..extensions import db
from sqlalchemy.exc import IntegrityError

def create_user(username, email, password, full_name=None):
    user = User(username=username, email=email, full_name=full_name)
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None, "Username or email already exists"
    return user, None
