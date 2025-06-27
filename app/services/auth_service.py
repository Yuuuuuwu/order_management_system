from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, email, password, role="customer"):
    if role not in ("admin", "seller", "customer"):
        raise ValueError("role 必須是 'admin', 'seller' 或 'customer'")
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
