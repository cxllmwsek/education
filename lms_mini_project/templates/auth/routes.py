from flask import render_template
from auth import bp

@bp.route('/register')
def register():
    # หน้าลงทะเบียนผู้ใช้
    return "This is the Register page for LMS."

@bp.route('/login')
def login():
    # หน้าเข้าสู่ระบบ
    return "This is the Login page for LMS."

@bp.route('/logout')
def logout():
    # ฟังก์ชันออกจากระบบ
    return "You have been logged out."