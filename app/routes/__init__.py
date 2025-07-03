# routes/__init__.py
# 方便 Blueprint 自動載入

from .auth import bp_auth
from .main import bp_main
from .users import bp_users
from .products import bp_products
from .orders import bp_orders
from .payments import bp_payments
from .customers import bp_customers
from .reports import bp_reports
from .notifications import bp_notifications
from .categories import bp_categories
