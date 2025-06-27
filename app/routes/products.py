# app/routes/products.py

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models.product import Product, Category
from app.schemas.product import product_schema, products_schema

bp_prod = Blueprint('products', __name__, url_prefix='/products')

# 允許未登入（訪客）也能查詢商品
@bp_prod.route('', methods=['GET'])
def list_products():
    """
    查詢商品清單，支援條件查詢（名稱、分類、上下架）、分頁、排序
    """
    name = request.args.get('name')
    category_id = request.args.get('category_id')
    is_active = request.args.get('is_active')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    q = Product.query
    if name:
        q = q.filter(Product.name.like(f"%{name}%"))
    if category_id:
        q = q.filter(Product.category_id == int(category_id))
    if is_active is not None:
        q = q.filter(Product.is_active == (is_active == 'true'))
    total = q.count()
    products = q.order_by(Product.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    return jsonify({
        "data": products_schema.dump(products),
        "total": total
    })

@bp_prod.route('/<int:pid>', methods=['GET'])
def get_product(pid):
    """取得單一商品"""
    p = Product.query.get_or_404(pid)
    return jsonify(product_schema.dump(p))

@bp_prod.route('', methods=['POST'])
@jwt_required()
def create_product():
    """新增商品"""
    data = request.get_json() or {}
    name = data.get('name')
    price = data.get('price')
    promo_price = data.get('promo_price')
    stock = data.get('stock', 0)
    desc = data.get('desc')
    image_url = data.get('image_url')
    is_active = data.get('is_active', True)
    category_id = data.get('category_id')
    if not name or price is None:
        abort(400, description="缺少必要欄位")
    prod = Product(
        name=name,
        price=price,
        promo_price=promo_price,
        stock=stock,
        desc=desc,
        image_url=image_url,
        is_active=is_active,
        category_id=category_id
    )
    db.session.add(prod)
    db.session.commit()
    return jsonify(product_schema.dump(prod)), 201

@bp_prod.route('/<int:pid>', methods=['PUT'])
@jwt_required()
def update_product(pid):
    """編輯商品"""
    p = Product.query.get_or_404(pid)
    data = request.get_json() or {}
    for field in ['name', 'price', 'promo_price', 'stock', 'desc', 'image_url', 'is_active', 'category_id']:
        if field in data:
            setattr(p, field, data[field])
    db.session.commit()
    return jsonify(product_schema.dump(p))

@bp_prod.route('/<int:pid>', methods=['DELETE'])
@jwt_required()
def delete_product(pid):
    """刪除商品"""
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'msg': '商品已刪除'})

@bp_prod.route('/batch/active', methods=['PUT'])
@jwt_required()
def batch_active():
    """批次上下架商品"""
    data = request.get_json() or {}
    ids = data.get('ids', [])
    is_active = data.get('is_active', True)
    for pid in ids:
        p = Product.query.get(pid)
        if p:
            p.is_active = is_active
    db.session.commit()
    return jsonify({'msg': '批次上下架完成'})

@bp_prod.route('/<int:pid>/stock', methods=['PUT'])
@jwt_required()
def change_stock(pid):
    """庫存異動（進貨/銷售）"""
    p = Product.query.get_or_404(pid)
    data = request.get_json() or {}
    delta = data.get('delta')
    if delta is None:
        abort(400, description="缺少 delta 參數")
    p.change_stock(delta)
    db.session.commit()
    return jsonify(product_schema.dump(p))

@bp_prod.route('/options', methods=['GET'])
@jwt_required()
def product_options():
    """商品下拉選單用（id, name, price, stock）"""
    qs = Product.query.filter_by(is_active=True).order_by(Product.created_at)
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in qs
    ])
