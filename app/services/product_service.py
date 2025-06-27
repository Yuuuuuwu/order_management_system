from app.models.product import Product, Category
from app import db

def create_product(**kwargs):
    prod = Product(**kwargs)
    db.session.add(prod)
    db.session.commit()
    return prod

def update_product(prod, **kwargs):
    for k, v in kwargs.items():
        setattr(prod, k, v)
    db.session.commit()
    return prod

def delete_product(prod):
    db.session.delete(prod)
    db.session.commit()

def batch_set_active(ids, is_active=True):
    for pid in ids:
        p = Product.query.get(pid)
        if p:
            p.is_active = is_active
    db.session.commit()

def change_stock(prod, delta):
    prod.change_stock(delta)
    db.session.commit()
    return prod

def create_category(**kwargs):
    cat = Category(**kwargs)
    db.session.add(cat)
    db.session.commit()
    return cat

def update_category(cat, **kwargs):
    for k, v in kwargs.items():
        setattr(cat, k, v)
    db.session.commit()
    return cat

def delete_category(cat):
    db.session.delete(cat)
    db.session.commit()
