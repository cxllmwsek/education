from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Extensions
db = SQLAlchemy()
login_manager = LoginManager()

# User Loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Database Models ---

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='student') # student, teacher, admin

    # Relationships
    courses_taught = db.relationship('Course', backref='author', lazy='dynamic')
    scores = db.relationship('Score', backref='student', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
    def is_teacher(self):
        # Teacher หรือ Admin สามารถสร้างคอร์สได้
        return self.role in ['teacher', 'admin']

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Foreign Key

    # Relationships
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic')

    def __repr__(self):
        return f'<Course {self.title}>'

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text) # Can be path to PDF/Video URL
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id')) # Foreign Key

    # Relationship
    quizzes = db.relationship('Quiz', backref='lesson', lazy='dynamic')

    def __repr__(self):
        return f'<Lesson {self.title}>'

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(120))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id')) # Foreign Key

    def __repr__(self):
        return f'<Quiz Q: {self.question[:30]}...>'

class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # Student
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    score = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())

    def __repr__(self):
        return f'<Score User:{self.user_id} Quiz:{self.quiz_id} Score:{self.score}>'