from app.models.payment import Payment
from app import db

def create_payment(**kwargs):
    payment = Payment(**kwargs)
    db.session.add(payment)
    db.session.commit()
    return payment

def get_payment_by_id(pid):
    return Payment.query.get(pid)
