from flask import Blueprint, request, jsonify, Response
from app.services.report_service import *
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app import db

bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@bp.route('/sales', methods=['GET'])
def sales():
    period = request.args.get('period', 'day')
    start = request.args.get('start')
    end = request.args.get('end')
    data = sales_summary(period, start, end)
    return jsonify(data)

@bp.route('/product-ranking', methods=['GET'])
def product_ranking():
    start = request.args.get('start')
    end = request.args.get('end')
    limit = int(request.args.get('limit', 10))
    data = product_sales_ranking(start, end, limit)
    return jsonify(data)

@bp.route('/customer-summary', methods=['GET'])
def customer_summary():
    data = customer_sales_summary()
    return jsonify(data)

@bp.route('/export/customers', methods=['GET'])
def export_customers():
    customers = Customer.query.all()
    csv_data = export_customers_csv(customers)
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=customers.csv'})

@bp.route('/export/orders', methods=['GET'])
def export_orders():
    orders = Order.query.all()
    csv_data = export_orders_csv(orders)
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=orders.csv'})

@bp.route('/export/products', methods=['GET'])
def export_products():
    products = Product.query.all()
    csv_data = export_products_csv(products)
    return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=products.csv'})
