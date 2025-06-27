# app/routes/payments.py
from flask import Blueprint, jsonify, abort, request, current_app, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models import Order, Payment
from app.services.notification_service import create_notification
from app.utils.check_mac_value import verify_check_mac_value
import hashlib
import urllib.parse
from datetime import datetime
from urllib.parse import quote

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
        'ReturnURL':         current_app.config['ECPAY_NOTIFY_URL'],
        'ClientBackURL':     current_app.config['FRONTEND_URL'] + "/payments/payment_result",
        'OrderResultURL':    current_app.config['ECPAY_ORDER_RETURN_URL'],
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
    # 5. 計算 CheckMacValue
    raw_params['CheckMacValue'] = gen_mac(raw_params)
    send_params = { k: str(v) for k, v in raw_params.items() }

    return jsonify({
        'ecpay_url': base_url,
        'params':    send_params
    })

@bp_pay.route('/ecpay/return', methods=['POST'])
def ecpay_return():
    """
    綠界自動導回 (OrderResultURL) → 讀 POST 表單 → 轉 GET 重導到前端
    """
    data = request.form.to_dict()
    trade_no = data.get('MerchantTradeNo')
    rtn_code = data.get('RtnCode')

    # 假設你的 order_sn 就存於 Order model
    # 於回調裡可以依 trade_no 解析訂單 id 或查資料庫拿 order_sn
    order_id = int(trade_no.replace('OMS', '')[:-10])
    order = Order.query.get(order_id)
    order_sn = order.order_sn if order else ''

    # 組成前端要的 URL (使用你的前端網域與路由)
    client_url = current_app.config.get('FRONTEND_URL')
    redirect_to = (
      f"{client_url}/payments/payment_result"
      f"?order_sn={quote(order_sn)}"
      f"&tradeNo={quote(trade_no)}"
      f"&RtnCode={quote(rtn_code)}"
    )

    return redirect(redirect_to)

@bp_pay.route('/ecpay/callback', methods=['POST'])
def ecpay_callback():
    """
    綠界付款結果通知 (模擬)
    """
    data = request.form.to_dict()
    trade_no = data.get('MerchantTradeNo')
    rtn_code = data.get('RtnCode')
    check_mac_value = data.get('CheckMacValue')

    current_app.logger.info(f"接收到的回調資料: {data}")
    current_app.logger.info(f"驗證結果: {verify_check_mac_value(data)}")

    if rtn_code == '1':
        current_app.logger.info(f"交易成功，訂單編號: {trade_no}")
        try:
            order_id = int(trade_no.replace('OMS', '')[:-10])
        except Exception as e:
            current_app.logger.error(f"解析訂單編號失敗: {e}")
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
            # 新增：寫入訂單歷程
            from app.models.order import OrderHistory
            db.session.add(OrderHistory(order_id=order.id, status='paid', operator=str(order.user_id), operated_at=datetime.now(), remark='付款完成'))
            db.session.commit()
            current_app.logger.info("訂單狀態更新成功")

            create_notification(
                user_id=order.user_id,
                type='payment_success',
                title='付款成功',
                content=f'您的訂單 {order.order_sn} 已完成付款。'
            )

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
