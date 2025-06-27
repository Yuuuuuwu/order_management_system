# app/routes/users.py
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app import db
from app.models import User
from app.schemas import user_schema
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

bp_users = Blueprint('users', __name__, url_prefix='/users')

# ─────────────  Create  ─────────────
@bp_users.route('', methods=['POST'])
def create_user():

    """
    新增使用者 (Create a new user)
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - in: body
        name: user
        required: true
        schema:
          $ref: '#/components/schemas/UserInput'
    responses:
      201:
        description: 使用者建立成功
        schema:
          $ref: '#/components/schemas/User'
      400:
        description: 欄位驗證失敗
    """
    payload = request.get_json() or {}
    try:
        valid = user_schema.load(payload)
    except ValidationError as err:
        return jsonify({"code": 400, "name": "Bad Request", "errors": err.messages}), 400

    role = payload.get('role', 'customer')
    if role not in ("admin", "seller", "customer"):
        return jsonify({"code": 400, "name": "Bad Request", "errors": {"role": "role 必須是 'admin', 'seller' 或 'customer'"}}), 400

    user = User(
        username=valid['username'],
        email=valid['email'],
        role=role,
        phone=valid.get('phone')
    )
    if 'password' in payload:
        user.set_password(payload['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

# ─────────────  Read all  ─────────────
@bp_users.route('', methods=['GET'])
@jwt_required()
def list_users():
    """
    取得使用者列表 (List users)
    ---
    tags:
      - Users
    responses:
      200:
        description: 使用者列表
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/components/schemas/User'
                total:
                  type: integer
    """

    claims = get_jwt()
    if claims.get('role') == 'admin':
        qs = User.query.order_by(User.created_at)
    else:
        uid = int(get_jwt_identity())
        qs = User.query.filter_by(id=uid)
    users = [u.to_dict() for u in qs]
    return jsonify({"data": users, "total": len(users)}), 200

# ─────────────  Read one  ─────────────
@bp_users.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    取得單一使用者 (Get user by ID)
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        schema:
          type: integer
        required: true
        description: 使用者 ID
    responses:
      200:
        description: 使用者詳細資料
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
      404:
        description: 使用者不存在
    """

    claims = get_jwt()
    uid = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    if claims.get('role') != 'admin' and user.id != uid:
        return jsonify({'msg': 'Permission denied'}), 403
    return jsonify(user.to_dict())

# ─────────────  Update  ─────────────
@bp_users.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):

    """
    更新使用者資料 (Update a user)
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
        description: 使用者 ID
      - in: body
        name: user
        required: true
        schema:
          $ref: '#/components/schemas/UserInput'
    responses:
      200:
        description: 使用者更新成功
        schema:
          $ref: '#/components/schemas/User'
      400:
        description: 欄位驗證錯誤
      404:
        description: 使用者不存在
    """
    payload = request.get_json() or {}
    try:
        valid = user_schema.load(payload, partial=True)
    except ValidationError as err:
        return jsonify({"code": 400, "name": "Bad Request", "errors": err.messages}), 400

    u = User.query.get_or_404(user_id, description="找不到使用者")
    if 'username' in valid:
        u.username = valid['username']
    if 'email' in valid:
        u.email = valid['email']
    if 'phone' in valid:
        u.phone = valid['phone']
    if 'role' in payload:
        if payload['role'] not in ("admin", "seller", "customer"):
            return jsonify({"code": 400, "name": "Bad Request", "errors": {"role": "role 必須是 'admin', 'seller' 或 'customer'"}}), 400
        u.role = payload['role']
    if 'password' in payload:
        u.set_password(payload['password'])

    db.session.commit()
    return jsonify(u.to_dict()), 200

# ─────────────  Delete  ─────────────
@bp_users.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    刪除使用者 (Delete a user)
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        schema:
          type: integer
        required: true
        description: 使用者 ID
    responses:
      200:
        description: 刪除成功
      404:
        description: 使用者不存在
    """
    u = User.query.get_or_404(user_id, description="找不到使用者")
    try:
        db.session.delete(u)
        db.session.commit()
        return jsonify({"message": "使用者刪除成功"}), 200
    except Exception as e:
        db.session.rollback()
        print("刪除錯誤：", e)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500