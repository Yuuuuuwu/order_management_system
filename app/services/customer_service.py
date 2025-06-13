from app.models.customer import Customer
from app import db
from sqlalchemy import func

def create_customer(data):
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return customer

def update_customer(customer, data):
    for k, v in data.items():
        setattr(customer, k, v)
    db.session.commit()
    return customer

def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)

def get_customers(query=None, tag=None, page=1, per_page=20):
    q = Customer.query
    if query:
        q = q.filter(Customer.name.like(f"%{query}%"))
    if tag:
        q = q.filter(Customer.tags.like(f"%{tag}%"))
    return q.order_by(Customer.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

def delete_customer(customer):
    db.session.delete(customer)
    db.session.commit()

def get_customer_order_stats(customer_id):
    from app.models.order import Order
    total_amount = db.session.query(func.sum(Order.total_amount)).filter(Order.customer_id==customer_id).scalar() or 0
    total_count = db.session.query(func.count(Order.id)).filter(Order.customer_id==customer_id).scalar() or 0
    return {'total_amount': total_amount, 'total_count': total_count}
