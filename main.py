import os
import glob
import pandas as pd
from dotenv import load_dotenv

from src.data_handler import parse_file
from src.iso_analyzer import get_iso_status
from src.predictor import calculate_trend_and_failure
from src.visualizer import plot_trend_comparison, plot_rul_prediction

# โหลดค่าคอนฟิกจาก .env
load_dotenv()

DATA_DIR = os.getenv('DATA_DIR', './data')
OUTPUT_FILE = os.getenv('OUTPUT_FILE', 'predictive_maintenance_results.csv')
T_ORANGE = float(os.getenv('THRESHOLD_ORANGE', 4.5))

def get_recommendation(status):
    """วิเคราะห์แนวทางปฏิบัติงาน (Decision Support)"""
    rec_map = {
        "Excellent": "Routine Monitoring",
        "Good": "Routine Monitoring",
        "Acceptable": "Increase Inspection Frequency",
        "Restricted": "Schedule Maintenance Soon",
        "Damage": "IMMEDIATE SHUTDOWN & REPAIR"
    }
    return rec_map.get(status, "Verify Data Accuracy")

def main():
    file_list = glob.glob(os.path.join(DATA_DIR, '*.txt'))
    if not file_list:
        print(f"Error: No data files found in {DATA_DIR}")
        return

    # 1. รวบรวมข้อมูลดิบ
    df_raw = pd.DataFrame([parse_file(f) for f in file_list])
    results = []
    
    # วาดกราฟภาพรวม (Trend Comparison)
    plot_trend_comparison(df_raw)
    
    # 2. วิเคราะห์รายเครื่องจักร
    for equipment, group in df_raw.groupby('Equipment'):
        # จัดเรียงวันที่และสร้างคอลัมน์ Month_Index (แก้ Error KeyError ตรงนี้)
        group = group.sort_values('Date').copy()
        min_date = group['Date'].min()
        group['Month_Index'] = (group['Date'].dt.year - min_date.year) * 12 + \
                               (group['Date'].dt.month - min_date.month) + 1
        
        latest_rms = group['RMS'].iloc[-1]
        
        # วิเคราะห์สถานะและพยากรณ์
        status = get_iso_status(latest_rms)
        trend, health_ratio, rul, params = calculate_trend_and_failure(group, T_ORANGE)
        
        # วาดกราฟพยากรณ์ (ส่ง group ที่มี Month_Index เข้าไปแล้ว)
        plot_rul_prediction(equipment, group, params, threshold=T_ORANGE)
        
        # คำนวณ Health Index (% ความสมบูรณ์ที่เหลืออยู่)
        health_index = max(0, 100 - health_ratio)
        
        results.append({
            'Machine Asset': equipment,
            'RMS (mm/s)': f"{latest_rms:.3f}",
            'Health Index': f"{health_index:.2f}%",
            'Est. RUL (Mo)': f"{rul}",
            'ISO Status': status,
            'Action Plan': get_recommendation(status)
        })

    # 3. สรุปผลการวิเคราะห์
    final_df = pd.DataFrame(results)
    final_df.to_csv(OUTPUT_FILE, index=False)
    
    print("\n" + "="*100)
    print("                PREDICTIVE MAINTENANCE EXECUTIVE DASHBOARD")
    print("="*100)
    print(final_df.to_string(index=False))
    print("="*100)
    print(f"\n[DONE] System output generated successfully.")

if __name__ == "__main__":
    main()