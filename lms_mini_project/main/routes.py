from flask import render_template
from main import bp

@bp.route('/')
def index():
    # เปลี่ยนจากการคืนค่าสตริงเป็นการเรนเดอร์ index.html
    return render_template('index.html')

@bp.route('/dashboard')
def dashboard():
    return "User Dashboard (Protected Page)"