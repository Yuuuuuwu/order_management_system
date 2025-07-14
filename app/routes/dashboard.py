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
    # 允許所有登入用戶查看統計
    if claims.get('role') not in ['admin', 'manager', 'seller']:
        return jsonify({'msg': 'Permission denied'}), 403
    
    # 統計資料
    total_sales = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    order_count = db.session.query(func.count(Order.id)).scalar() or 0
    customer_count = db.session.query(func.count(User.id)).scalar() or 0
    
    # 相容 MySQL 和 PostgreSQL 的月度統計
    try:
        # PostgreSQL
        month_expr = func.date_trunc("month", Order.created_at)
        monthly_sales_raw = (
            db.session.query(month_expr.label("month"), func.sum(Order.total_amount).label("value"))
            .group_by(month_expr)
            .order_by(month_expr)
            .all()
        )
    except:
        # MySQL fallback
        month_expr = func.date_format(Order.created_at, '%Y-%m')
        monthly_sales_raw = (
            db.session.query(month_expr.label("month"), func.sum(Order.total_amount).label("value"))
            .group_by(month_expr)
            .order_by(month_expr)
            .all()
        )
    
    # 序列化月度資料
    monthly_sales = []
    for row in monthly_sales_raw:
        # 格式化月份顯示，例如 "2024-01" -> "2024年1月"
        month_str = str(row.month)
        if len(month_str) >= 7:  # YYYY-MM 格式
            year, month = month_str[:7].split('-')
            formatted_month = f"{year}年{int(month)}月"
        else:
            formatted_month = month_str
            
        monthly_sales.append({
            "month": formatted_month,
            "value": float(row.value) if row.value else 0
        })
    
    # 新增2025年1-6月假數據，確保按順序排列
    fake_data = [
        {"month": "2025年1月", "value": 25000.0, "sort_key": "2025-01"},
        {"month": "2025年2月", "value": 32000.0, "sort_key": "2025-02"},
        {"month": "2025年3月", "value": 28500.0, "sort_key": "2025-03"},
        {"month": "2025年4月", "value": 35000.0, "sort_key": "2025-04"},
        {"month": "2025年5月", "value": 42000.0, "sort_key": "2025-05"},
        {"month": "2025年6月", "value": 38000.0, "sort_key": "2025-06"}
    ]
    
    # 為真實數據添加排序鍵
    for item in monthly_sales:
        month_display = item["month"]
        if "年" in month_display and "月" in month_display:
            # 從 "2024年12月" 格式提取年月
            year = month_display.split("年")[0]
            month = month_display.split("年")[1].replace("月", "")
            item["sort_key"] = f"{year}-{month.zfill(2)}"
        else:
            item["sort_key"] = "0000-00"  # 備用排序
    
    # 合併並按時間順序排序
    all_monthly_data = monthly_sales + fake_data
    all_monthly_data.sort(key=lambda x: x["sort_key"])
    
    # 移除排序鍵，只保留month和value
    monthly_sales = [{"month": item["month"], "value": item["value"]} for item in all_monthly_data]
    
    return jsonify({
        "total_sales": float(total_sales),
        "order_count": int(order_count),
        "customer_count": int(customer_count),
        "monthly_sales": monthly_sales
    })
