# tests/test_validation.py

def test_user_validation_success(client):
    # 合法欄位：username 與 email 都給正確格式
    resp = client.post("/users", json={
        "username": "charlie",
        "email": "charlie@example.com"
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["username"] == "charlie"


def test_user_validation_missing_fields(client):
    # 缺少 email
    resp = client.post("/users", json={
        "username": "no_email"
    })
    assert resp.status_code == 400
    err = resp.get_json()
    # 假設你的 ValidationError 處理器會把錯誤訊息放在 'errors' 裡
    assert "email" in err.get("errors", {})


def test_user_validation_bad_email_format(client):
    # email 格式不正確
    resp = client.post("/users", json={
        "username": "bad_email",
        "email": "not-an-email"
    })
    assert resp.status_code == 400
    err = resp.get_json()
    assert "email" in err.get("errors", {})
