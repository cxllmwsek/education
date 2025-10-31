import os

# หาพาธของโฟลเดอร์รากโปรเจ็ค (ที่ config.py อยู่)
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')

# ตรวจสอบและสร้างโฟลเดอร์ 'instance' ถ้ายังไม่มี
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

class Config:
    # SECRET_KEY ใช้สำหรับเข้ารหัสเซสชัน
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret'
    
    # กำหนดพาธฐานข้อมูลแบบเต็ม
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'lms_mini.sqlite')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
