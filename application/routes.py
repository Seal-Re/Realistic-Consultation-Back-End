# routes/__init__.py
from flask import Blueprint
from .home import home_bp
from .ai import ai_bp
from .audio import audio_bp
from .TablePool import table_list

# 创建一个新的蓝图，用于整合所有的路由*
main_bp = Blueprint('main', __name__)

# 注册所有的蓝图
main_bp.register_blueprint(home_bp)
main_bp.register_blueprint(ai_bp)
main_bp.register_blueprint(audio_bp)
main_bp.register_blueprint(table_list)
