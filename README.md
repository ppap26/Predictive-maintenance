# Predictive Maintenance Model (Vibration Analysis)

โปรเจกต์นี้ถูกพัฒนาขึ้นเพื่อวิเคราะห์ข้อมูลความสั่นสะเทือน (Vibration Waveform) ของเครื่องจักรจากไฟล์ Text โดยอัตโนมัติ ระบบจะทำการคำนวณหาค่าความรุนแรง (RMS) ประเมินสถานะความผิดปกติของเครื่องจักรตามมาตรฐาน ISO 10816-3 และใช้โมเดล Linear Regression เพื่อวิเคราะห์แนวโน้มและพยากรณ์วันที่เครื่องจักรอาจจะเกิดความเสียหาย (Estimated Failure Date)

## 📁 Project Structure

predictive-maintenance/
│
├── data/                   # โฟลเดอร์สำหรับวางไฟล์ข้อมูลดิบ (.txt)
├── src/                    # โฟลเดอร์เก็บ Source Code หลัก
│   ├── __init__.py
│   ├── data_handler.py     # จัดการอ่านไฟล์ ดึงค่าด้วย Regex และคำนวณ RMS
│   ├── iso_analyzer.py     # ประเมินสถานะเครื่องจักร (Zone A, B, C, D)
│   └── predictor.py        # วิเคราะห์แนวโน้มและพยากรณ์วันเสียด้วย Linear Regression
│
├── .env                    # ไฟล์ตั้งค่าตัวแปรระบบ (Thresholds)
├── .gitignore              # ไฟล์กำหนดสิ่งที่ไม่ต้องนำขึ้น Git
├── requirements.txt        # รายชื่อไลบรารี Python ที่จำเป็น
└── main.py                 # ไฟล์หลักสำหรับรันระบบ

## ⚙️ Prerequisites, Setup & Run

รันคำสั่งด้านล่างนี้ตามลำดับ:

1. สร้าง Virtual Environment:
   python3 -m venv .venv

2. เปิดใช้งาน Virtual Environment (สำหรับ Mac/Linux):
   source .venv/bin/activate
   (หมายเหตุ: สำหรับ Windows ให้ใช้คำสั่ง .venv\Scripts\activate แทน)

3. ติดตั้งไลบรารีที่จำเป็น:
   pip install -r requirements.txt

4. รันระบบประมวลผล:
   python3 main.py

## 🔧 Configuration (.env)

คุณสามารถปรับแต่งค่าเกณฑ์มาตรฐานและโฟลเดอร์ที่ใช้เก็บข้อมูลได้ผ่านไฟล์ .env:

DATA_DIR=./data
OUTPUT_FILE=predictive_maintenance_results.csv

THRESHOLD_YELLOW=VALUE_OF_YELLOW_ZONE
THRESHOLD_ORANGE=VALUE_OF_ORANGE_ZONE
THRESHOLD_RED=VALUE_OF_RED_ZONE
