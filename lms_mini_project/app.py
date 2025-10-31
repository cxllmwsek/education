from flask import Flask
from .config import Config
from .database import db, login_manager



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'กรุณาเข้าสู่ระบบก่อนเข้าถึงหน้านี้'

    # Register blueprints
    from .auth import bp as auth_bp # pyright: ignore[reportMissingImports]
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .teacher import bp as teacher_bp
    app.register_blueprint(teacher_bp)

    # Create DB tables
    with app.app_context():
        from .database import User, Course, Lesson, Quiz, Score
        db.create_all()
        print("✅ Database ready.")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
