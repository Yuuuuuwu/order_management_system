from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Notification, OperationLog
from app.schemas import NotificationSchema, OperationLogSchema
from app import db

bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@bp.route('', methods=['GET'])
@jwt_required()
def list_notifications():
    uid = int(get_jwt_identity())
    notifs = Notification.query.filter((Notification.user_id == uid) | (Notification.user_id == None)).order_by(Notification.created_at.desc()).all()
    return jsonify(NotificationSchema(many=True).dump(notifs))

@bp.route('/<int:notif_id>/read', methods=['POST'])
@jwt_required()
def mark_read(notif_id):
    uid = int(get_jwt_identity())
    notif = Notification.query.get_or_404(notif_id)
    if notif.user_id and notif.user_id != uid:
        return jsonify({'msg': '無權限'}), 403
    notif.is_read = True
    db.session.commit()
    return jsonify({'msg': '已標記為已讀'})

@bp.route('/logs', methods=['GET'])
@jwt_required()
def list_logs():
    # 僅 admin 可看全部，user 只能看自己
    from flask_jwt_extended import get_jwt
    claims = get_jwt()
    uid = int(get_jwt_identity())
    if claims.get('role') == 'admin':
        logs = OperationLog.query.order_by(OperationLog.created_at.desc()).all()
    else:
        logs = OperationLog.query.filter_by(user_id=uid).order_by(OperationLog.created_at.desc()).all()
    return jsonify(OperationLogSchema(many=True).dump(logs))
