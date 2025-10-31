from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from . import bp # import bp แบบ Relative
from ..database import db, User # Import db และ Model User แบบ Relative (ใช้ .. เพื่อขึ้นไป 1 ระดับ)
from sqlalchemy import exc

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # ป้องกันผู้ใช้ที่ล็อกอินแล้วไม่ให้เข้าถึงหน้าลงทะเบียน
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        # ... ดึงข้อมูลฟอร์ม ...
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'student') # Default เป็น student

        # 1. ตรวจสอบผู้ใช้ซ้ำ
        if User.query.filter_by(email=email).first():
            flash('อีเมลนี้ถูกใช้แล้ว โปรดใช้อีเมลอื่น', 'warning')
            return redirect(url_for('auth.register'))

        # 2. สร้างผู้ใช้ใหม่
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password) # ใช้ฟังก์ชันแฮชรหัสผ่าน

        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user) 
            flash(f'ลงทะเบียนสำเร็จ! ยินดีต้อนรับ {username}', 'success')
            return redirect(url_for('main.dashboard'))
        except exc.IntegrityError:
            db.session.rollback()
            flash('เกิดข้อผิดพลาดในการบันทึกข้อมูล', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        # 1. ตรวจสอบผู้ใช้และรหัสผ่าน
        if user is None or not user.check_password(password):
            flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'danger')
            return redirect(url_for('auth.login'))

        # 2. ล็อกอินสำเร็จ
        login_user(user, remember=True)
        flash('เข้าสู่ระบบสำเร็จ!', 'success')
        
        # Redirect ไปหน้าก่อนหน้าหรือหน้า dashboard
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.dashboard'))

    return render_template('auth/login.html')

@bp.route('/logout')
@login_required 
def logout():
    logout_user()
    flash('คุณออกจากระบบแล้ว', 'info')
    return redirect(url_for('main.index'))