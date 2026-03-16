import re
import numpy as np
from datetime import datetime
from scipy.integrate import cumulative_trapezoid

def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    content = "".join(lines)
    # ดึง Metadata (Equipment และ Date) จากเนื้อหาไฟล์
    eq_match = re.search(r'Equipment:\s+(.+)', content)
    equipment = eq_match.group(1).replace("(CHPP) ", "").strip() if eq_match else "Unknown"
    
    date_match = re.search(r'Date/Time:\s+([0-9]{2}-[a-zA-Z]{3}-[0-9]{2})', content)
    date_str = date_match.group(1) if date_match else None
    record_date = datetime.strptime(date_str, '%d-%b-%y') if date_str else datetime.now()

    # --- ส่วนที่ปรับตามเพื่อน: เริ่มอ่านข้อมูลเมื่อเจอคีย์เวิร์ด ---
    data = []
    start_reading = False
    for line in lines:
        if "Time" in line and "Amplitude" in line:
            start_reading = True
            continue
        
        if start_reading:
            parts = line.split()
            # เก็บข้อมูลเป็นคู่ๆ (Time, Amplitude)
            for i in range(0, len(parts), 2):
                try:
                    t = float(parts[i])
                    a = float(parts[i+1])
                    data.append([t, a])
                except (ValueError, IndexError):
                    continue

    if not data:
        return {'Equipment': equipment, 'Date': record_date, 'RMS': 0.0}

    # แปลงเป็น Array เพื่อคำนวณ
    data_np = np.array(data)
    time_s = data_np[:, 0] / 1000.0  # ms -> s
    accel = data_np[:, 1]
    
    # ลบค่าเฉลี่ย (DC Offset) ตามหลักวิศวกรรม
    accel = accel - np.mean(accel)
    
    # ใช้ค่า Amplitude เดิมจากไฟล์ตามแบบจำลองของเพื่อน 
    velocity_mms = cumulative_trapezoid(accel, time_s, initial=0)
    velocity_mms = velocity_mms - np.mean(velocity_mms) # Detrend
    
    # คำนวณ RMS Velocity (mm/s)
    rms_value = np.sqrt(np.mean(velocity_mms**2))

    return {'Equipment': equipment, 'Date': record_date, 'RMS': rms_value}