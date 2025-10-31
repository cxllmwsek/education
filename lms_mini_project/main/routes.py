from flask import render_template
from flask_login import login_required
from . import bp

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required # เพิ่ม: ต้องล็อกอินก่อน
def dashboard():
    return render_template('dashboard.html')