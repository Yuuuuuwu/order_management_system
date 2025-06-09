# app/routes/products.py

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # # 修改：匯入 get_jwt_identity, get_jwt
from app import db
from app.models import Product

bp_prod = Blueprint('products', __name__, url_prefix='/products')

@bp_prod.route('', methods=['GET'])
@jwt_required()  # # 修改：新增 JWT 驗證
def list_products():
    """
    列出所有商品
    admin: 看所有；user: 只看自己
    """
    claims = get_jwt()                    # # 修改：取得 JWT claims
    uid = int(get_jwt_identity())         # # 修改：取得 user_id
    if claims.get("role") == "admin":     # # 修改：admin 可看所有
        qs = Product.query.order_by(Product.id)
    else:
        qs = Product.query.filter_by(user_id=uid).order_by(Product.id)  # # 修改：user 只看自己
    return jsonify([p.to_dict() for p in qs]), 200

@bp_prod.route('/<int:pid>', methods=['GET'])
@jwt_required()  # # 修改：新增 JWT 驗證
def get_product(pid):
    """
    取得單一商品
    admin: 任意；user: 只能自己的
    """
    claims = get_jwt()                    
    uid = int(get_jwt_identity())         
    p = Product.query.get_or_404(pid)
    if claims.get("role") != "admin" and p.user_id != uid:  # # 修改：非 admin 拒絕存取他人
        abort(403, description="沒有權限存取此商品")
    return jsonify(p.to_dict()), 200

@bp_prod.route('', methods=['POST'])
@jwt_required()  # # 修改：新增 JWT 驗證，移除原本僅 Admin 限制
def create_product():
    """
    新增商品
    admin/user 均可建立，屬於自己的商品
    """
    data = request.get_json() or {}
    for field in ('name', 'price'):
        if field not in data:
            abort(400, description=f"缺少欄位：{field}")
    uid = int(get_jwt_identity())        # # 修改：取得 user_id
    prod = Product(
        name=data['name'],
        price=data['price'],
        stock=data.get('stock', 0),
        desc=data.get('desc'),
        user_id=uid                       # # 修改：設定建立者
    )
    db.session.add(prod)
    db.session.commit()
    return jsonify(prod.to_dict()), 201

@bp_prod.route('/<int:pid>', methods=['PUT'])
@jwt_required()  # # 修改：新增 JWT 驗證
def update_product(pid):
    """
    更新商品
    admin: 任意；user: 只能更新自己的
    """
    claims = get_jwt()
    uid = int(get_jwt_identity())
    p = Product.query.get_or_404(pid)
    if claims.get("role") != "admin" and p.user_id != uid:  # # 修改：非 admin 拒絕修改他人
        abort(403, description="沒有權限修改此商品")
    data = request.get_json() or {}
    p.name  = data.get('name',  p.name)
    p.price = data.get('price', p.price)
    p.stock = data.get('stock', p.stock)
    p.desc  = data.get('desc',  p.desc)
    db.session.commit()
    return jsonify(p.to_dict()), 200

@bp_prod.route('/<int:pid>', methods=['DELETE'])
@jwt_required()  # # 修改：新增 JWT 驗證
def delete_product(pid):
    """
    刪除商品
    admin: 任意；user: 只能刪除自己的
    """
    claims = get_jwt()
    uid = int(get_jwt_identity())
    p = Product.query.get_or_404(pid)
    if claims.get("role") != "admin" and p.user_id != uid:  # # 修改：非 admin 拒絕刪除他人
        abort(403, description="沒有權限刪除此商品")
    db.session.delete(p)
    db.session.commit()
    return '', 204
