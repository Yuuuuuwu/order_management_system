from app import db
from datetime import datetime

class OperationLog(db.Model):
    __tablename__ = 'operation_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    action = db.Column(db.String(32), nullable=False)  # create/update/delete
    target_type = db.Column(db.String(32), nullable=False)  # e.g. 'order', 'product'
    target_id = db.Column(db.Integer, nullable=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'action': self.action,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'content': self.content,
            'created_at': self.created_at,
        }
