from flask import Blueprint, jsonify

bp_main = Blueprint('main', __name__)

@bp_main.route('/ping', methods=['GET'])
def ping():
    """
    健康檢查端點 (Health check endpoint)
    只接受 GET，回傳純文字 "pong" 與 HTTP 200 (Only GET, returns 'pong' and HTTP 200)
    ---
    tags:
      - Utility
    responses:
      200:
        description: pong
    """
    return 'pong', 200

@bp_main.route('/', methods=['GET'])
def index():
    """
    歡迎端點 (Welcome endpoint)
    回傳系統歡迎訊息 (Returns welcome message)
    ---
    tags:
      - Utility
    responses:
      200:
        description: Hello message
    """
    return jsonify({
        "message": "訂單管理系統歡迎您！ (Hello, Order Management System!)"
    }), 200


