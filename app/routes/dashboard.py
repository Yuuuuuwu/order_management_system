from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models import Order, User
from app import db
from sqlalchemy import func

bp_dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp_dashboard.route('/summary', methods=['GET'])
@jwt_required()
def summary():
    claims = get_jwt()
    # 僅 admin 可看全部統計
    if claims.get('role') not in ['admin', 'manager']:
        return jsonify({'msg': 'Permission denied'}), 403
    # 修正欄位名稱錯誤
    total_sales = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    order_count = db.session.query(func.count(Order.id)).scalar() or 0
    customer_count = db.session.query(func.count(User.id)).scalar() or 0
    return jsonify({
        "total_sales": total_sales,
        "order_count": order_count,
        "customer_count": customer_count
    })
