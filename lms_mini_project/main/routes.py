from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ✅ เพิ่ม route แสดงรายละเอียดคอร์ส
@bp.route('/course/<int:course_id>')
def course_detail(course_id):
    courses = {
        1: {
            'title': 'พื้นฐานเทคโนโลยีสารสนเทศ',
            'description': 'เรียนรู้พื้นฐานของฮาร์ดแวร์ ซอฟต์แวร์ และเครือข่ายในศตวรรษที่ 21',
            'content': [
                'บทที่ 1: ฮาร์ดแวร์และซอฟต์แวร์',
                'บทที่ 2: การทำงานของคอมพิวเตอร์',
                'บทที่ 3: อินเทอร์เน็ตและระบบเครือข่าย',
                'บทที่ 4: ความปลอดภัยทางไซเบอร์'
            ]
        },
        2: {
            'title': 'หลักการเขียนโปรแกรมเบื้องต้น',
            'description': 'เข้าใจตรรกะการเขียนโปรแกรมและสร้างโค้ดแรกด้วยภาษา Python',
            'content': [
                'บทที่ 1: รู้จักกับภาษา Python',
                'บทที่ 2: ตัวแปรและชนิดข้อมูล',
                'บทที่ 3: เงื่อนไขและการวนลูป',
                'บทที่ 4: ฟังก์ชันและโครงสร้างโปรแกรม'
            ]
        },
        3: {
            'title': 'นวัตกรรมทางการศึกษา',
            'description': 'ศึกษาการประยุกต์ใช้เทคโนโลยีดิจิทัลในห้องเรียนยุคใหม่',
            'content': [
                'บทที่ 1: เทคโนโลยีในห้องเรียนยุคดิจิทัล',
                'บทที่ 2: การออกแบบการเรียนรู้ด้วยนวัตกรรม',
                'บทที่ 3: เครื่องมือออนไลน์สำหรับครู'
            ]
        }
    }

    course = courses.get(course_id)
    if not course:
        return render_template('404.html'), 404

    return render_template('course_detail.html', course=course)


