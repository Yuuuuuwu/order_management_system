from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt
from app.services.report_service import *
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app import db

bp_reports = Blueprint('reports', __name__, url_prefix='/api/reports')

@bp_reports.route('/sales', methods=['GET'])
@jwt_required()
def sales():
    # 權限檢查：只有 admin 和 seller 可以查看報表
    current_user_claims = get_jwt()
    current_user_role = current_user_claims.get('role', 'customer')
    
    if current_user_role not in ['admin', 'seller']:
        return jsonify({'code': 403, 'message': '權限不足，只有管理員和銷售員可以查看報表'}), 403
    
    period = request.args.get('period', 'day')
    start = request.args.get('date_start') or request.args.get('start')
    end = request.args.get('date_end') or request.args.get('end')
    data = sales_summary(period, start, end)
    return jsonify(data)

@bp_reports.route('/product-ranking', methods=['GET'])
@jwt_required()
def product_ranking():
    # 權限檢查：只有 admin 和 seller 可以查看報表
    current_user_claims = get_jwt()
    current_user_role = current_user_claims.get('role', 'customer')
    
    if current_user_role not in ['admin', 'seller']:
        return jsonify({'code': 403, 'message': '權限不足，只有管理員和銷售員可以查看報表'}), 403
    
    start = request.args.get('date_start') or request.args.get('start')
    end = request.args.get('date_end') or request.args.get('end')
    limit = int(request.args.get('limit', 10))
    data = product_sales_ranking(start, end, limit)
    return jsonify(data)

@bp_reports.route('/customer-summary', methods=['GET'])
@jwt_required()
def customer_summary():
    # 權限檢查：只有 admin 和 seller 可以查看報表
    current_user_claims = get_jwt()
    current_user_role = current_user_claims.get('role', 'customer')
    
    if current_user_role not in ['admin', 'seller']:
        return jsonify({'code': 403, 'message': '權限不足，只有管理員和銷售員可以查看報表'}), 403
    
    data = customer_sales_summary()
    return jsonify(data)

@bp_reports.route('/export/customers', methods=['GET'])
@jwt_required()
def export_customers():
    # 權限檢查：只有 admin 和 seller 可以匯出報表
    current_user_claims = get_jwt()
    current_user_role = current_user_claims.get('role', 'customer')
    
    if current_user_role not in ['admin', 'seller']:
        return jsonify({'code': 403, 'message': '權限不足，只有管理員和銷售員可以匯出報表'}), 403
    
    customers = Customer.query.all()
    csv_data = export_customers_csv(customers)
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=customers.csv'})

@bp_reports.route('/export/orders', methods=['GET'])
@jwt_required()
def export_orders():
    # 權限檢查：只有 admin 和 seller 可以匯出報表
    current_user_claims = get_jwt()
    current_user_role = current_user_claims.get('role', 'customer')
    
    if current_user_role not in ['admin', 'seller']:
        return jsonify({'code': 403, 'message': '權限不足，只有管理員和銷售員可以匯出報表'}), 403
    
    orders = Order.query.all()
    csv_data = export_orders_csv(orders)
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=orders.csv'})

@bp_reports.route('/export/products', methods=['GET'])
@jwt_required()
def export_products():
    # 權限檢查：只有 admin 和 seller 可以匯出報表
    current_user_claims = get_jwt()
    current_user_role = current_user_claims.get('role', 'customer')
    
    if current_user_role not in ['admin', 'seller']:
        return jsonify({'code': 403, 'message': '權限不足，只有管理員和銷售員可以匯出報表'}), 403
    
    products = Product.query.all()
    csv_data = export_products_csv(products)
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=products.csv'})

@bp_reports.route('/export/order_stats', methods=['GET'])
@jwt_required()
def export_order_stats():
    # 權限檢查：只有 admin 和 seller 可以匯出報表
    current_user_claims = get_jwt()
    current_user_role = current_user_claims.get('role', 'customer')
    
    if current_user_role not in ['admin', 'seller']:
        return jsonify({'code': 403, 'message': '權限不足，只有管理員和銷售員可以匯出報表'}), 403
    
    period = request.args.get('period', 'day')
    start = request.args.get('date_start') or request.args.get('start')
    end = request.args.get('date_end') or request.args.get('end')
    data = sales_summary(period, start, end)
    csv_data = export_order_stats_csv(data)
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=order_stats.csv'})

@bp_reports.route('/export/product_rank', methods=['GET'])
@jwt_required()
def export_product_rank():
    # 權限檢查：只有 admin 和 seller 可以匯出報表
    current_user_claims = get_jwt()
    current_user_role = current_user_claims.get('role', 'customer')
    
    if current_user_role not in ['admin', 'seller']:
        return jsonify({'code': 403, 'message': '權限不足，只有管理員和銷售員可以匯出報表'}), 403
    
    start = request.args.get('date_start') or request.args.get('start')
    end = request.args.get('date_end') or request.args.get('end')
    limit = int(request.args.get('limit', 10))
    data = product_sales_ranking(start, end, limit)
    csv_data = export_product_rank_csv(data)
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=product_rank.csv'})
