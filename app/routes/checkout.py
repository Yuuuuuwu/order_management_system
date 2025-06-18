from flask import Blueprint, request, jsonify
from app.services.order_service import create_order, get_order_by_sn
from app.models.product import Product
from app import db

bp_checkout = Blueprint('checkout', __name__, url_prefix='/checkout')

@bp_checkout.route('/preview', methods=['POST'])
def preview():
    data = request.json
    product_ids = data.get('product_ids', [])
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    if not products:
        return jsonify({'msg': 'No products found'}), 404

    preview_data = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock': product.stock
        } for product in products
    ]
    return jsonify({'preview': preview_data})

@bp_checkout.route('/process', methods=['POST'])
def process_checkout():
    data = request.json
    order_data = {
        'order_sn': data.get('order_sn'),
        'amount': data.get('amount'),
        'payment_method': data.get('payment_method')
    }
    order = create_order(**order_data)
    return jsonify({'msg': 'Order created', 'order_id': order.id})
