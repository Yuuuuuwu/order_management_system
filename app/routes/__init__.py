# routes/__init__.py
# 方便 Blueprint 自動載入

from .customers import bp as customers_bp
from .reports import bp as reports_bp
from .notifications import bp as notifications_bp
