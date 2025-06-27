from app.models import OperationLog, Notification
from app import db
from datetime import datetime

def log_operation(user_id, username, action, target_type, target_id=None, content=None):
    log = OperationLog(
        user_id=user_id,
        username=username,
        action=action,
        target_type=target_type,
        target_id=target_id,
        content=content,
        created_at=datetime.utcnow(),
    )
    db.session.add(log)
    db.session.commit()
    return log

def create_notification(user_id, type, title, content):
    notif = Notification(
        user_id=user_id,
        type=type,
        title=title,
        content=content,
        created_at=datetime.utcnow(),
    )
    db.session.add(notif)
    db.session.commit()
    return notif
