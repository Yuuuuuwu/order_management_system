# tests/test_users.py
def test_create_and_get_user(client):
    # 建立
    rv = client.post('/users', json={'username':'bob','email':'bob@example.com'})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['username']=='bob'
    # 取回
    rv2 = client.get(f"/users/{data['id']}")
    assert rv2.status_code == 200
