from flask import Blueprint, request, jsonify
from app.schemas.customer import CustomerSchema
from app.forms.customer_form import CustomerForm
from app.services.customer_service import *
from app.models.customer import Customer
from app import db

# 1. 關閉 strict_slashes，讓 /customers 和 /customers/ 都能對應
bp_customers = Blueprint('customers', __name__, url_prefix='/customers')

@bp_customers.route('', methods=['GET'])
def list_customers():
    """取得客戶列表（支援 query、tag、分頁）"""
    query = request.args.get('query')
    tag = request.args.get('tag')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    pagination = get_customers(query, tag, page, per_page)
    schema = CustomerSchema(many=True)
    return jsonify({
        'data': schema.dump(pagination.items),
        'total': pagination.total
    })

@bp_customers.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """取得單一客戶"""
    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(CustomerSchema().dump(customer))

@bp_customers.route('', methods=['POST'])
def create():
    """新增客戶"""
    form = CustomerForm(data=request.json)
    if form.validate():
        customer = create_customer(form.data)
        return jsonify(CustomerSchema().dump(customer)), 201
    return jsonify({'error': form.errors}), 400

@bp_customers.route('/<int:customer_id>', methods=['PUT'])
def update(customer_id):
    """更新客戶"""
    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Not found'}), 404
    form = CustomerForm(data=request.json)
    if form.validate():
        customer = update_customer(customer, form.data)
        return jsonify(CustomerSchema().dump(customer))
    return jsonify({'error': form.errors}), 400

@bp_customers.route('/<int:customer_id>', methods=['DELETE'])
def delete(customer_id):
    """刪除客戶"""
    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Not found'}), 404
    delete_customer(customer)
    return '', 204

@bp_customers.route('/<int:customer_id>/orders', methods=['GET'])
def customer_orders(customer_id):
    """某客戶的所有訂單"""
    from app.models.order import Order
    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Not found'}), 404
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return jsonify([o.to_dict() for o in orders])

@bp_customers.route('/<int:customer_id>/stats', methods=['GET'])
def customer_stats(customer_id):
    """某客戶的訂單統計資料"""
    stats = get_customer_order_stats(customer_id)
    return jsonify(stats)
