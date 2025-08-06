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
        func.date_format(Order.created_at, '%Y-%m-%d' if period=='day' else ('%Y-%m' if period=='month' else '%Y')).label('date'),
        func.count(Order.id).label('order_count'),
        func.sum(Order.total_amount).label('total_amount')
    )
    if start:
        q = q.filter(Order.created_at >= start)
    if end:
        q = q.filter(Order.created_at <= end)
    q = q.group_by(1).order_by(1)
    return [{'date': r[0], 'order_count': int(r[1]), 'total_amount': float(r[2])} for r in q.all()]

def product_sales_ranking(start=None, end=None, limit=10):
    from app.models.order import OrderItem
    q = db.session.query(
        Product.name,
        func.sum(OrderItem.qty).label('total_qty'),
        func.sum(OrderItem.qty * OrderItem.price).label('total_amount')
    ).join(OrderItem, Product.id==OrderItem.product_id)\
     .join(Order, OrderItem.order_id==Order.id)
    if start:
        q = q.filter(Order.created_at >= start)
    if end:
        q = q.filter(Order.created_at <= end)
    q = q.group_by(Product.id).order_by(func.sum(OrderItem.qty).desc()).limit(limit)
    return [{'product_name': r[0], 'total_qty': int(r[1]), 'total_amount': float(r[2])} for r in q.all()]

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

def export_order_stats_csv(data):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['日期', '訂單數', '總金額'])
    for item in data:
        writer.writerow([item['date'], item['order_count'], item['total_amount']])
    return output.getvalue()

def export_product_rank_csv(data):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['商品名稱', '銷售數量', '銷售金額'])
    for item in data:
        writer.writerow([item['product_name'], item['total_qty'], item['total_amount']])
    return output.getvalue()
