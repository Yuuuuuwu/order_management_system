import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # 本地開發時啟動開發伺服器
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host=host, port=port, debug=debug)