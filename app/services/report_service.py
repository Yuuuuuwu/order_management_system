from app.models.order import Order
from app.models.product import Product
from app.models.customer import Customer
from app import db
from sqlalchemy import func
from datetime import datetime
import csv, io

def sales_summary(period='day', start=None, end=None):
    # period: day/month/year
    q = db.session.query(
        func.date_format(Order.created_at, '%Y-%m-%d' if period=='day' else ('%Y-%m' if period=='month' else '%Y')),
        func.sum(Order.total_amount)
    )
    if start:
        q = q.filter(Order.created_at >= start)
    if end:
        q = q.filter(Order.created_at <= end)
    q = q.group_by(1).order_by(1)
    return [{'period': r[0], 'total': float(r[1])} for r in q.all()]

def product_sales_ranking(start=None, end=None, limit=10):
    from app.models.order import OrderItem
    q = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('qty'),
        func.sum(OrderItem.subtotal).label('amount')
    ).join(OrderItem, Product.id==OrderItem.product_id)
    if start:
        q = q.filter(OrderItem.created_at >= start)
    if end:
        q = q.filter(OrderItem.created_at <= end)
    q = q.group_by(Product.id).order_by(func.sum(OrderItem.quantity).desc()).limit(limit)
    return [{'product': r[0], 'quantity': int(r[1]), 'amount': float(r[2])} for r in q.all()]

def customer_sales_summary():
    q = db.session.query(
        Customer.id, Customer.name,
        func.count(Order.id),
        func.sum(Order.total_amount)
    ).join(Order, Customer.id==Order.customer_id).group_by(Customer.id)
    return [{'customer_id': r[0], 'name': r[1], 'order_count': int(r[2]), 'total_amount': float(r[3])} for r in q.all()]

def export_customers_csv(customers):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', '姓名', '電話', '地址', 'Email', '標籤'])
    for c in customers:
        writer.writerow([c.id, c.name, c.phone, c.address, c.email, c.tags])
    return output.getvalue()

def export_orders_csv(orders):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['訂單編號', '客戶', '金額', '狀態', '建立時間'])
    for o in orders:
        writer.writerow([o.id, o.customer_id, o.total_amount, o.status, o.created_at])
    return output.getvalue()

def export_products_csv(products):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['商品ID', '名稱', '分類', '價格', '促銷價', '庫存'])
    for p in products:
        writer.writerow([p.id, p.name, p.category_id, p.price, p.promo_price, p.stock])
    return output.getvalue()
