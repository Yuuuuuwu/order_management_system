from flask import Blueprint, request, jsonify, abort
from app import db
from app.models.product import Category
from app.schemas.product import category_schema, categories_schema
from flask_jwt_extended import jwt_required, get_jwt

bp_categories = Blueprint('categories', __name__, url_prefix='/categories')

@bp_categories.route('', methods=['GET'])
@jwt_required(optional=True)
def list_categories():
    """取得所有分類（巢狀結構）"""
    roots = Category.query.filter_by(parent_id=None).all()
    return jsonify(categories_schema.dump(roots))

@bp_categories.route('/<int:cid>', methods=['GET'])
@jwt_required(optional=True)
def get_category(cid):
    cat = Category.query.get_or_404(cid)
    return jsonify(category_schema.dump(cat))

@bp_categories.route('', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json() or {}
    name = data.get('name')
    parent_id = data.get('parent_id')
    if not name:
        abort(400, description="缺少分類名稱")
    cat = Category(name=name, parent_id=parent_id)
    db.session.add(cat)
    db.session.commit()
    return jsonify(category_schema.dump(cat)), 201

@bp_categories.route('/<int:cid>', methods=['PUT'])
@jwt_required()
def update_category(cid):
    cat = Category.query.get_or_404(cid)
    data = request.get_json() or {}
    if 'name' in data:
        cat.name = data['name']
    if 'parent_id' in data:
        cat.parent_id = data['parent_id']
    db.session.commit()
    return jsonify(category_schema.dump(cat))

@bp_categories.route('/<int:cid>', methods=['DELETE'])
@jwt_required()
def delete_category(cid):
    cat = Category.query.get_or_404(cid)
    db.session.delete(cat)
    db.session.commit()
    return jsonify({'msg': '分類已刪除'})
