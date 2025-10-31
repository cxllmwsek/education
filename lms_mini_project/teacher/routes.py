from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import bp
from ..database import db, Course
from sqlalchemy import exc

# Decorator ตรวจสอบบทบาท Teacher
def teacher_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_teacher():
            flash('สิทธิ์ไม่เพียงพอ คุณต้องเป็นผู้สอนหรือผู้ดูแลระบบ', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/create_course', methods=['GET', 'POST'])
@teacher_required 
def create_course():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title or not description:
            flash('โปรดกรอกข้อมูลให้ครบถ้วน', 'warning')
            return redirect(url_for('teacher.create_course'))

        # 1. สร้างคอร์สใหม่
        new_course = Course(
            title=title, 
            description=description, 
            teacher_id=current_user.id
        )

        try:
            # 2. บันทึกข้อมูล
            db.session.add(new_course)
            db.session.commit()
            flash(f'สร้างคอร์ส "{title}" สำเร็จแล้ว!', 'success')
            return redirect(url_for('main.dashboard')) 
        except exc.IntegrityError:
            db.session.rollback()
            flash('เกิดข้อผิดพลาดในการบันทึกคอร์ส', 'danger')
            return redirect(url_for('teacher.create_course'))

    return render_template('teacher/create_course.html')