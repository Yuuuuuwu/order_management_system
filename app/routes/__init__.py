# routes/__init__.py
# 方便 Blueprint 自動載入

from .auth import bp_auth
from .main import bp_main
from .users import bp_users
from .products import bp_prod
from .orders import bp_orders
from .payments import bp_pay
from .customers import bp_customers
from .reports import bp as reports_bp
from .notifications import bp as notifications_bp
from .categories import bp_categories
