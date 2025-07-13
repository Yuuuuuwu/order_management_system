#app/routes/dashboard.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.models import Order, User
from app import db
from sqlalchemy import func,extract

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
    # MySQL 兼容的日期截斷：使用 DATE_FORMAT 按月分組
    month_expr = func.date_format(Order.created_at, '%Y-%m')
    monthly_sales_data = (
        db.session.query(month_expr.label("month"), func.sum(Order.total_amount).label("value"))
        .group_by(month_expr)
        .order_by(month_expr)
        .all()
    )
    # 格式化月度銷售數據為前端期望的格式
    formatted_monthly_sales = [
        {
            "month": row[0],  # 格式: "2025-07"
            "value": float(row[1]) if row[1] else 0
        }
        for row in monthly_sales_data
    ]
    
    return jsonify({
        "total_sales": float(total_sales) if total_sales else 0,
        "order_count": order_count,
        "customer_count": customer_count,
        "monthly_sales": formatted_monthly_sales
    })
