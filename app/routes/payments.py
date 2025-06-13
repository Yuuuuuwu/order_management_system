# app/routes/payments.py
from flask import Blueprint, jsonify, abort, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models import Order, Payment
import hashlib
import urllib.parse
from datetime import datetime

bp_pay = Blueprint('payments', __name__, url_prefix='/payments')

@bp_pay.route('/<int:order_id>', methods=['POST'])
@jwt_required()
def pay_order(order_id):
    """
    付款訂單
    ---
    tags:
      - Payments
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: order_id
        schema:
          type: integer
        required: true
        description: 訂單 ID
    responses:
      201:
        description: 付款成功
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Payment'
      400:
        description: 訂單狀態不允許付款
      403:
        description: 不是該用戶的訂單
      404:
        description: 找不到訂單
    """
    claims = get_jwt()
    uid = int(get_jwt_identity())
    order = Order.query.get_or_404(order_id)

    # 只允許 admin 或本人付款
    if claims.get('role') != 'admin' and order.user_id != uid:
        abort(403, description="這不是你的訂單")

    # 只有 pending 狀態可付款
    if order.status != 'pending':
        abort(400, description="訂單已付款或已取消")

    # 建立 Payment 紀錄，使用 total_amount 屬性
    payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        status='success',
        payment_method='mock',
        paid_at=datetime.now()
    )
    order.status = 'paid'
    db.session.add(payment)
    db.session.commit()

    return jsonify(payment.to_dict()), 201
@bp_pay.route('/ecpay/<int:order_id>', methods=['POST'])
@jwt_required()
def ecpay_pay_order(order_id):
    """
    綠界支付模擬 - 產生付款連結
    ---
    tags:
      - Payments
    parameters:
      - in: path
        name: order_id
        schema:
          type: integer
        required: true
        description: 訂單 ID
    responses:
      200:
        description: 回傳綠界付款連結
    """
    claims = get_jwt()
    uid    = int(get_jwt_identity())
    order  = Order.query.get_or_404(order_id)

    if claims.get('role') != 'admin' and order.user_id != uid:
        abort(403, "這不是你的訂單")
    if order.status != 'pending':
        abort(400, "訂單已付款或已取消")

    merchant_id = current_app.config.get('ECPAY_MERCHANT_ID')
    hash_key    = current_app.config.get('ECPAY_HASH_KEY')
    hash_iv     = current_app.config.get('ECPAY_HASH_IV')
    base_url    = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'
    notify_url  = current_app.config.get('ECPAY_NOTIFY_URL')
    return_url  = current_app.config.get('ECPAY_RETURN_URL')
    trade_no    = f'OMS{order.id}{int(datetime.now().timestamp())}'

    raw_params = {
        'MerchantID':        merchant_id,
        'MerchantTradeNo':   trade_no,
        'MerchantTradeDate': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'PaymentType':       'aio',
        'TotalAmount':       int(order.total_amount),
        'TradeDesc':         'OMS訂單付款',
        'ItemName':          'OMS商品x1',
        'ReturnURL':         notify_url,
        'ClientBackURL':     return_url,
        'ChoosePayment':     'ALL',
        'EncryptType':       1,
    }

    def gen_mac(params: dict):
      # 1. 按 key 字典序排序後拼成字串
      ordered = sorted(params.items())
      raw = "&".join(f"{k}={v}" for k, v in ordered)
      raw = f"HashKey={hash_key}&{raw}&HashIV={hash_iv}"

      # 2. URL encode 全串，用 quote_plus (空格會變 '+')，並轉小寫
      urlenc = urllib.parse.quote_plus(raw).lower()

      # 3. 還原綠界要求的保留字元
      for enc, ch in [
          ('%2d','-'), ('%5f','_'), ('%2e','.'), 
          ('%21','!'), ('%2a','*'), ('%28','('), ('%29',')'),
      ]:
          urlenc = urlenc.replace(enc, ch)

      # 4. 做 SHA256，hex → 再轉大寫
      return hashlib.sha256(urlenc.encode('utf-8')).hexdigest().upper()


    raw_params['CheckMacValue'] = gen_mac(raw_params)

    # 準備前端 form 要送出的欄位，全部 quote()
    send_params = {k: str(v) for k, v in raw_params.items()}

    return jsonify({
        'ecpay_url': base_url,
        'params':    send_params
    })



@bp_pay.route('/ecpay/callback', methods=['POST'])
def ecpay_callback():
    """
    綠界付款結果通知 (模擬)
    """
    data = request.form.to_dict()
    trade_no = data.get('MerchantTradeNo')
    rtn_code = data.get('RtnCode')
    # 這裡可加 CheckMacValue 驗證
    if rtn_code == '1':
        try:
            order_id = int(trade_no.replace('OMS', '')[:-10])
        except Exception:
            return 'fail'
        order = Order.query.get(order_id)
        if order:
            order.status = 'paid'
            payment = Payment(
                order_id=order.id,
                amount=order.total_amount,
                status='success',
                payment_method='ecpay',
                transaction_id=trade_no,
                paid_at=datetime.now()
            )
            db.session.add(payment)
            db.session.commit()
        return '1|OK'
    return '0|FAIL'

@bp_pay.route('', methods=['GET'])
@jwt_required()
def list_payments():
    claims = get_jwt()
    uid = int(get_jwt_identity())
    if claims.get('role') == 'admin':
        qs = Payment.query.order_by(Payment.created_at.desc())
    else:
        qs = Payment.query.join(Order).filter(Order.user_id == uid).order_by(Payment.created_at.desc())
    return jsonify([p.to_dict() for p in qs]), 200

@bp_pay.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id):
    claims = get_jwt()
    uid = int(get_jwt_identity())
    payment = Payment.query.get_or_404(payment_id)
    if claims.get('role') != 'admin' and payment.order.user_id != uid:
        abort(403, description="Permission denied")
    return jsonify(payment.to_dict()), 200
