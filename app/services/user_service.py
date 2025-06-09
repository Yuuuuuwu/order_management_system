from app.models.user import User
from app import db

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user(user, **kwargs):
    for k, v in kwargs.items():
        setattr(user, k, v)
    db.session.commit()
    return user
