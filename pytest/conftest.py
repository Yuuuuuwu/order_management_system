# tests/conftest.py
import pytest
from app import create_app, db


@pytest.fixture(scope="function")        # ← 每個 test function 都會重建一次 app
def client():
    """
    測試用 client fixture
    - 啟用 TESTING 模式
    - 使用 in‑memory SQLite（乾淨又快速）
    - 每次測試前先 drop_all 再 create_all，確保資料表是全新的
    """
    app = create_app()

    # *** 1. 設定測試用 config  ***
    app.config.update({
        "TESTING": True,
        "PROPAGATE_EXCEPTIONS": True,           # ← 例外直接往外拋，pytest 可看到 traceback
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # in‑memory DB
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    # *** 2. 重新建立資料表（確保乾淨） ***
    with app.app_context():
        db.drop_all()
        db.create_all()

    # *** 3. 回傳測試 client ***
    with app.test_client() as client:
        yield client
        # 不用額外收尾：離開 with block 會自動關閉 session
