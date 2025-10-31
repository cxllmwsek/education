from flask import Blueprint

# สร้าง Blueprint ชื่อ 'main'
bp = Blueprint('main', __name__)

# ต้อง import routes.py ที่นี่
from . import routes