#原本user.py的驗證部分搬來這裡

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

# ---------- 註冊 ----------
@bp_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    required = {'username', 'email', 'password'}
    missing = required - data.keys()
    if missing:
        abort(400, description=f"缺少欄位: {', '.join(missing)}")

    if User.query.filter_by(username=data['username']).first():
        abort(400, description="使用者名稱已存在")
    if User.query.filter_by(email=data['email']).first():
        abort(400, description="Email 已被註冊")

    user = User(username=data['username'], email=data['email'])
    user.password_hash = generate_password_hash(data['password'])
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "access_token": token
    }), 201

# ---------- 登入 ----------
@bp_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not check_password_hash(user.password_hash, data.get('password', '')):
        abort(401, description="帳號或密碼錯誤")

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return jsonify({"access_token": token}), 200

# ---------- 範例：取得自己的資訊 ----------
@bp_auth.route('/me', methods=['GET'])
@jwt_required()
def me():
    uid = get_jwt_identity()
    uid = int(uid)
    user = User.query.get_or_404(uid)
    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 200
