from flask import Flask
from config import Config
from database import db, login_manager # <--- เพิ่มการ import

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions here
    db.init_app(app) # <--- เพิ่มการตั้งค่า DB
    login_manager.init_app(app) # <--- เพิ่มการตั้งค่า Login Manager
    login_manager.login_view = 'auth.login' # <--- กำหนดหน้า Login
    login_manager.login_message = 'Please log in to access this page.'

    # Register blueprints (routes will be added in later steps)
    # from auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # from main import bp as main_bp
    # app.register_blueprint(main_bp)


    # Simple route for testing
    @app.route('/')
    def index():
        return "LMS Mini Project Running! Database ready for creation." # <--- เปลี่ยนข้อความ

    # สร้างฐานข้อมูลหากยังไม่มี (ต้องรันภายใน app context)
    with app.app_context():
        # import Models เพื่อให้ SQLAlchemy รู้จัก
        from database import User, Course, Lesson, Quiz, Score
        db.create_all() # <--- สร้างตารางทั้งหมด (ถ้ายังไม่มี)
        print("Database initialized or checked.")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)