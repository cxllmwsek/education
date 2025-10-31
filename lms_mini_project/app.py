import sys
import os

from flask import Flask
from config import Config
from database import db, login_manager
# ลบ importlib ออกไป เพราะเราจะใช้ flask run แทน

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    # Register blueprints (การ import นี้จะทำงานได้ถูกต้องเมื่อรันด้วย flask run)
    from auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from main import bp as main_bp
    app.register_blueprint(main_bp)


    # สร้างฐานข้อมูลหากยังไม่มี
    with app.app_context():
        # import Models เพื่อให้ SQLAlchemy รู้จัก
        from database import User, Course, Lesson, Quiz, Score
        db.create_all()
        print("Database initialized or checked.")

    return app

# ลบ: if __name__ == '__main__':
# ลบ:     app = create_app()
# ลบ:     app.run(debug=True)