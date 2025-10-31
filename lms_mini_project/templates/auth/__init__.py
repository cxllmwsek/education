from flask import Blueprint

# สร้าง Blueprint ชื่อ 'auth'
bp = Blueprint('auth', __name__)

# ต้อง import routes.py ที่นี่เพื่อให้ Blueprint รู้จักฟังก์ชัน route
from . import routes