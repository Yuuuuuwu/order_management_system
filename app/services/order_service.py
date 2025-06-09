from app.models.order import Order
from app import db

def create_order(**kwargs):
    order = Order(**kwargs)
    db.session.add(order)
    db.session.commit()
    return order

def get_order_by_sn(order_sn):
    return Order.query.filter_by(order_sn=order_sn).first()
