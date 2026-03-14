import re
import numpy as np
from datetime import datetime

def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ดึงชื่อ Equipment
    eq_match = re.search(r'Equipment:\s+(.+)', content)
    equipment = eq_match.group(1).strip() if eq_match else "Unknown"
    
    # ดึงวันที่
    date_match = re.search(r'Date/Time:\s+([0-9]{2}-[a-zA-Z]{3}-[0-9]{2})', content)
    date_str = date_match.group(1) if date_match else None
    record_date = datetime.strptime(date_str, '%d-%b-%y') if date_str else datetime.now()

    # ดึงค่า Amplitude และคำนวณ RMS
    lines = content.split('\n')
    data_lines = [line for line in lines if re.match(r'^\s*[\d\.]+\s+', line)]
    
    amplitudes = []
    for line in data_lines:
        values = line.split()
        for i in range(1, len(values), 2):
            try:
                amplitudes.append(float(values[i]))
            except ValueError:
                pass
                
    arr = np.array(amplitudes)
    rms_value = np.sqrt(np.mean(arr**2)) if len(arr) > 0 else 0.0

    return {'Equipment': equipment, 'Date': record_date, 'RMS': rms_value}