# app/routes/orders.py
from flask import Blueprint, jsonify, request, abort
from app import db
from app.models import Order, OrderItem, User

bp_orders = Blueprint('orders', __name__, url_prefix='/orders')

@bp_orders.route('', methods=['POST'])
def create_order():
    """
    建立新訂單 (Create a new order)
    """
    data = request.get_json() or {}
    user_id = data.get('user_id')
    items   = data.get('items')
    remark  = data.get('remark')

    # 基本檢查
    if not user_id or not isinstance(items, list) or len(items) == 0:
        abort(400, description="需要 user_id 以及至少一筆 items (user_id and items[] are required)")

    if not User.query.get(user_id):
        abort(404, description="找不到指定使用者 (Specified user not found)")

    # 建立 Order 主表
    order = Order(user_id=user_id, remark=remark)
    db.session.add(order)
    db.session.flush()  # 拿到 order.id

    total_price = 0.0
    # 建立每筆明細
    for idx, it in enumerate(items, start=1):
        pid = it.get('product_id')
        qty = it.get('quantity')
        price = it.get('price')

        if not pid or not qty or not price:
            abort(400,
                  description=f"第 {idx} 筆 items 缺少 product_id / quantity / price (item[{idx}] missing product_id/quantity/price)")

        oi = OrderItem(
            order_id=order.id,
            product_id=pid,
            quantity=qty,
            price=price
        )
        db.session.add(oi)
        total_price += qty * price

    # 更新 total_price
    order.total_price = total_price
    db.session.commit()

    # 回傳完整訂單
    return jsonify({
        "id":          order.id,
        "user_id":     order.user_id,
        "status":      order.status,
        "remark":      order.remark,
        "created_at":  order.created_at.isoformat(),
        "items": [{
            "product_id": it.product_id,
            "quantity":   it.quantity,
            "price":      it.price
        } for it in order.items],
        "total_qty":   sum(it.quantity for it in order.items),
        "total_amt":   total_price
    }), 201


@bp_orders.route('', methods=['GET'])
def list_orders():
    """
    取得所有訂單 (List all orders)
    """
    orders = Order.query.all()
    result = []
    for o in orders:
        items = [{
            "product_id": it.product_id,
            "quantity":   it.quantity,
            "price":      it.price
        } for it in o.items]

        total_qty = sum(it['quantity'] for it in items)
        total_amt = sum(it['quantity'] * it['price'] for it in items)

        result.append({
            "id":          o.id,
            "user_id":     o.user_id,
            "status":      o.status,
            "remark":      o.remark,
            "created_at":  o.created_at.isoformat(),
            "items":       items,
            "total_qty":   total_qty,
            "total_amt":   total_amt
        })
    return jsonify(result), 200


@bp_orders.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    取得單一訂單 (Retrieve an order by ID)
    """
    o = Order.query.get_or_404(order_id, description="找不到訂單 (Order not found)")
    items = [{
        "product_id": it.product_id,
        "quantity":   it.quantity,
        "price":      it.price
    } for it in o.items]

    total_qty = sum(it['quantity'] for it in items)
    total_amt = sum(it['quantity'] * it['price'] for it in items)

    return jsonify({
        "id":          o.id,
        "user_id":     o.user_id,
        "status":      o.status,
        "remark":      o.remark,
        "created_at":  o.created_at.isoformat(),
        "items":       items,
        "total_qty":   total_qty,
        "total_amt":   total_amt
    }), 200


@bp_orders.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    更新訂單資料 (Update an existing order)
    """
    o = Order.query.get_or_404(order_id, description="找不到訂單 (Order not found)")
    data = request.get_json() or {}

    # 更新備註
    if 'remark' in data:
        o.remark = data['remark']

    # 如果有修改 items，就先刪掉舊明細，再新增
    if 'items' in data:
        OrderItem.query.filter_by(order_id=order_id).delete()
        total_price = 0.0
        for idx, it in enumerate(data['items'], start=1):
            pid = it.get('product_id')
            qty = it.get('quantity')
            price = it.get('price')
            if not pid or not qty or not price:
                abort(400,
                      description=f"第 {idx} 筆 items 缺少 product_id / quantity / price")
            oi = OrderItem(
                order_id=order_id,
                product_id=pid,
                quantity=qty,
                price=price
            )
            db.session.add(oi)
            total_price += qty * price
        o.total_price = total_price

    db.session.commit()
    return jsonify({"message": "訂單更新成功"}), 200


@bp_orders.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    刪除訂單 (Delete an order)
    """
    o = Order.query.get_or_404(order_id, description="找不到訂單 (Order not found)")
    db.session.delete(o)
    db.session.commit()
    return jsonify({"message": "訂單刪除成功"}), 200
