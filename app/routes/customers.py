from flask import Blueprint, request, jsonify
from app.schemas.customer import CustomerSchema
from app.forms.customer_form import CustomerForm
from app.services.customer_service import *
from app.models.customer import Customer
from app import db

bp = Blueprint('customers', __name__, url_prefix='/api/customers')

@bp.route('/', methods=['GET'])
def list_customers():
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

@bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Not found'}), 404
    schema = CustomerSchema()
    return jsonify(schema.dump(customer))

@bp.route('/', methods=['POST'])
def create():
    form = CustomerForm(data=request.json)
    if form.validate():
        customer = create_customer(form.data)
        return jsonify(CustomerSchema().dump(customer)), 201
    return jsonify({'error': form.errors}), 400

@bp.route('/<int:customer_id>', methods=['PUT'])
def update(customer_id):
    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Not found'}), 404
    form = CustomerForm(data=request.json)
    if form.validate():
        customer = update_customer(customer, form.data)
        return jsonify(CustomerSchema().dump(customer))
    return jsonify({'error': form.errors}), 400

@bp.route('/<int:customer_id>', methods=['DELETE'])
def delete(customer_id):
    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Not found'}), 404
    delete_customer(customer)
    return '', 204

@bp.route('/<int:customer_id>/orders', methods=['GET'])
def customer_orders(customer_id):
    from app.models.order import Order
    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Not found'}), 404
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return jsonify([o.to_dict() for o in orders])

@bp.route('/<int:customer_id>/stats', methods=['GET'])
def customer_stats(customer_id):
    stats = get_customer_order_stats(customer_id)
    return jsonify(stats)
