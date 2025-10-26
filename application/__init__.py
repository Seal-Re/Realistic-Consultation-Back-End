from flask import Flask
from application.config import config
from .routes import main_bp
from flask_cors import CORS
import sys
import io

def create_app(config_name='default'):
    app = Flask(__name__, static_folder='../tts')
    app.config.from_object(config[config_name])
    CORS(app)

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    # 注册合并后的蓝图
    app.register_blueprint(main_bp)
    return app