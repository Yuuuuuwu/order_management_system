from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Order, OrderItem, OrderHistory, Product
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import joinedload  # 重要，為了一起查出 user
from datetime import datetime
import random
from app.services.notification_service import log_operation, create_notification

bp_orders = Blueprint('orders', __name__, url_prefix='/orders')

@bp_orders.route('', methods=['GET'])
@jwt_required()
def list_orders():
    """取得訂單列表，支援分頁、篩選、關鍵字、狀態、排序，並帶出 user"""
    claims = get_jwt()
    uid = int(get_jwt_identity())
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    status = request.args.get('status')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    keyword = request.args.get('keyword')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')

    q = Order.query.options(joinedload(Order.user))  # 關鍵，避免 N+1 查詢

    if claims.get('role') != 'admin':
        q = q.filter_by(user_id=uid)
    if status:
        q = q.filter(Order.status == status)
    if date_start:
        q = q.filter(Order.created_at >= date_start)
    if date_end:
        q = q.filter(Order.created_at <= date_end)
    if keyword:
        q = q.filter(or_(Order.order_sn.like(f"%{keyword}%"), Order.remark.like(f"%{keyword}%"), Order.receiver_name.like(f"%{keyword}%")))

    if sort_by in ['created_at', 'total_amount', 'status']:
        sort_col = getattr(Order, sort_by)
        q = q.order_by(sort_col.desc() if sort_order == 'desc' else sort_col.asc())

    total = q.count()
    orders = q.offset((page-1)*page_size).limit(page_size).all()

    return jsonify({
        "data": [o.to_dict(include_items=True, include_user=True) for o in orders],
        "total": total
    })

@bp_orders.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    claims = get_jwt()
    uid = int(get_jwt_identity())
    order = Order.query.get_or_404(order_id)
    if claims.get('role') != 'admin' and order.user_id != uid:
        return jsonify({'msg': 'Permission denied'}), 403
    # 修改：include_user=True
    return jsonify(order.to_dict(include_items=True, include_history=True, include_user=True))

# 以 order_sn 查訂單
@bp_orders.route('/sn/<string:order_sn>', methods=['GET'])
@jwt_required()
def get_order_by_sn(order_sn):
    """
    以 order_sn（訂單編號）取得訂單
    GET /orders/sn/{order_sn}
    """
    claims = get_jwt()
    uid = int(get_jwt_identity())
    order = Order.query.filter_by(order_sn=order_sn).first_or_404()
    if claims.get('role') != 'admin' and order.user_id != uid:
        abort(403, description="Permission denied")
    return jsonify(order.to_dict(include_items=True, include_history=True)), 200


@bp_orders.route('/<int:order_id>/history', methods=['GET'])
@jwt_required()
def get_order_history(order_id):
    claims = get_jwt()
    uid = int(get_jwt_identity())
    order = Order.query.get_or_404(order_id)
    if claims.get('role') != 'admin' and order.user_id != uid:
        return jsonify({'msg': 'Permission denied'}), 403
    history = OrderHistory.query.filter_by(order_id=order_id).order_by(OrderHistory.operated_at).all()
    return jsonify([h.to_dict() for h in history])

@bp_orders.route('/status', methods=['PUT'])
@jwt_required()
def batch_update_status():
    data = request.get_json() or {}
    ids = data.get('ids', [])
    status = data.get('status')
    remark = data.get('remark')
    claims = get_jwt()
    uid = int(get_jwt_identity())
    for oid in ids:
        order = Order.query.get(oid)
        if not order:
            continue
        if claims.get('role') != 'admin' and order.user_id != uid:
            continue
        order.status = status
        h = OrderHistory(order_id=order.id, status=status, operator=str(uid), operated_at=datetime.now(), remark=remark)
        db.session.add(h)
        # 狀態異動通知（站內）
        create_notification(order.user_id, 'order_status', f'訂單狀態更新', f'您的訂單 {order.id} 狀態已變更為 {order.status}')
    db.session.commit()
    return jsonify({'msg': '狀態更新成功'})

@bp_orders.route('', methods=['POST'])
@jwt_required()
def create_order():
    """
    建立新訂單 (Create a new order)
    """
    data = request.get_json() or {}
    user_id = int(get_jwt_identity())
    # 自動產生訂單編號
    order_sn = f"OMS{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100,999)}"
    receiver_name = data.get('receiver_name')
    receiver_phone = data.get('receiver_phone')
    shipping_address = data.get('shipping_address')
    remark = data.get('remark')
    items = data.get('items', [])
    if not all([receiver_name, receiver_phone, shipping_address, items]):
        abort(400, description="缺少必要欄位")
    # 計算金額
    total_amount = 0
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product:
            abort(400, description=f"找不到商品 {item['product_id']}")
        item['product_name'] = product.name
        item['price'] = product.price
        total_amount += product.price * item['qty']
    order = Order(
        user_id=user_id,
        order_sn=order_sn,
        total_amount=total_amount,
        status='pending',
        shipping_fee=0,
        payment_status='unpaid',
        remark=remark,
        receiver_name=receiver_name,
        receiver_phone=receiver_phone,
        shipping_address=shipping_address
    )
    db.session.add(order)
    db.session.flush()
    for item in items:
        db.session.add(OrderItem(order_id=order.id, product_id=item['product_id'], product_name=item['product_name'], qty=item['qty'], price=item['price']))
    # 狀態歷史
    db.session.add(OrderHistory(order_id=order.id, status='pending', operator=str(user_id), operated_at=datetime.now(), remark='訂單建立'))
    # 扣減商品庫存
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product:
            abort(400, description=f"找不到商品 {item['product_id']}")
        if product.stock < item['qty']:
            abort(400, description=f"商品 {product.name} 庫存不足")
        product.change_stock(-item['qty'])
    db.session.commit()
    return jsonify(order.to_dict(include_items=True, include_history=True)), 201

@bp_orders.route('/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    claims = get_jwt()
    uid = int(get_jwt_identity())
    o = Order.query.get_or_404(order_id)
    if claims.get("role") != "admin" and o.user_id != uid:
        abort(404, description="找不到或無權限修改此訂單")
    data = request.get_json() or {}
    if 'receiver_name' in data:
        o.receiver_name = data['receiver_name']
    if 'receiver_phone' in data:
        o.receiver_phone = data['receiver_phone']
    if 'shipping_address' in data:
        o.shipping_address = data['shipping_address']
    if 'remark' in data:
        o.remark = data['remark']
    # 商品明細可編輯（僅未結單）
    if o.status == 'pending' and 'items' in data:
        OrderItem.query.filter_by(order_id=o.id).delete()
        total_amount = 0
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if not product:
                abort(400, description=f"找不到商品 {item['product_id']}")
            db.session.add(OrderItem(order_id=o.id, product_id=product.id, product_name=product.name, qty=item['qty'], price=product.price))
            total_amount += product.price * item['qty']
        o.total_amount = total_amount
    db.session.commit()
    return jsonify(o.to_dict(include_items=True, include_history=True)), 200

@bp_orders.route('/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    claims = get_jwt()
    uid = int(get_jwt_identity())
    o = Order.query.get_or_404(order_id)
    if claims.get("role") != "admin" and o.user_id != uid:
        abort(404, description="找不到或無權限刪除此訂單")
    # 在刪除訂單時記錄操作日誌
    log_operation(uid, claims.get('username', str(uid)), 'delete', 'order', order_id, f"刪除訂單 {order_id}")
    db.session.delete(o)
    db.session.commit()
    return jsonify({"message": "訂單刪除成功"}), 200
