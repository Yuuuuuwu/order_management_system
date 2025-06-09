from app.models.product import Product
from app import db

def create_product(**kwargs):
    product = Product(**kwargs)
    db.session.add(product)
    db.session.commit()
    return product

def get_product_by_id(pid):
    return Product.query.get(pid)
