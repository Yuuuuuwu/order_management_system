from app import create_app

app = create_app()

if __name__ == '__main__':
    # 啟動開發伺服器，預設監聽 127.0.0.1:5000
    app.run(debug=True)


#惠中0512
#遷移資料庫 migration資料夾出現，資料庫的 Git 倉庫
#export FLASK_APP=run.py
#export FLASK_APP="app:create_app"