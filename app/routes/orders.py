from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Order
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # # 修改：匯入 get_jwt

bp_orders = Blueprint('orders', __name__, url_prefix='/orders')

@bp_orders.route('', methods=['POST'])
@jwt_required()
def create_order():
    """
    建立新訂單 (Create a new order)
    前端欄位: orderId, customer, amount, status, date, remark
    """
    data = request.get_json() or {}
    order_id = data.get('orderId')
    customer = data.get('customer')
    amount   = data.get('amount')
    status   = data.get('status')
    date     = data.get('date')
    remark   = data.get('remark')

    if not all([order_id, customer, amount, status, date]):
        abort(400, description="需要 orderId、customer、amount、status、date")

    if Order.query.filter_by(order_id=order_id).first():
        abort(400, description="訂單編號已存在")

    user_id = int(get_jwt_identity())
    order = Order(
        user_id=user_id,
        order_id=order_id,
        customer=customer,
        amount=amount,
        status=status,
        date=date,
        remark=remark
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

@bp_orders.route('', methods=['GET'])
@jwt_required()
def list_orders():
    """
    取得訂單列表 (List orders)
    admin: 看所有；user: 只看自己
    """
    claims = get_jwt()                    # # 修改：取得 JWT claims
    uid = int(get_jwt_identity())
    if claims.get("role") == "admin":     # # 修改：admin 看所有
        qs = Order.query.order_by(Order.created_at)
    else:
        qs = Order.query.filter_by(user_id=uid).order_by(Order.created_at)  # # 修改：user 看自己
    return jsonify([o.to_dict() for o in qs]), 200

@bp_orders.route('/<string:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """
    取得單一訂單 (Retrieve an order by orderId)
    admin: 任意；user: 自己
    """
    claims = get_jwt()
    uid = int(get_jwt_identity())
    o = Order.query.filter_by(order_id=order_id).first()
    if not o:
        abort(404, description="找不到訂單")
    if claims.get("role") != "admin" and o.user_id != uid:  # # 修改：非 admin 禁止存取他人
        abort(403, description="沒有權限存取此訂單")
    return jsonify(o.to_dict()), 200

@bp_orders.route('/<string:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    """
    更新訂單 (Update an existing order)
    admin: 任意；user: 自己
    """
    claims = get_jwt()
    uid = int(get_jwt_identity())
    o = Order.query.filter_by(order_id=order_id).first()
    if not o or (claims.get("role") != "admin" and o.user_id != uid):  # # 修改：檢查權限
        abort(404, description="找不到或無權限修改此訂單")

    data = request.get_json() or {}
    if 'customer' in data:
        o.customer = data['customer']
    if 'amount' in data:
        o.amount = data['amount']
    if 'status' in data:
        o.status = data['status']
    if 'date' in data:
        o.date = data['date']
    if 'remark' in data:
        o.remark = data['remark']

    db.session.commit()
    return jsonify(o.to_dict()), 200

@bp_orders.route('/<string:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    """
    刪除訂單 (Delete an order)
    admin: 任意；user: 自己
    """
    claims = get_jwt()
    uid = int(get_jwt_identity())
    o = Order.query.filter_by(order_id=order_id).first()
    if not o or (claims.get("role") != "admin" and o.user_id != uid):  # # 修改：檢查權限
        abort(404, description="找不到或無權限刪除此訂單")
    db.session.delete(o)
    db.session.commit()
    return jsonify({"message": "訂單刪除成功"}), 200
