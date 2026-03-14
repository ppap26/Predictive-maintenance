import os
import glob
import pandas as pd
from dotenv import load_dotenv

from src.data_handler import parse_file
from src.iso_analyzer import get_iso_status
from src.predictor import calculate_trend_and_failure

load_dotenv()
DATA_DIR = os.getenv('DATA_DIR', './data')
OUTPUT_FILE = os.getenv('OUTPUT_FILE', 'predictive_maintenance_results.csv')
THRESHOLD_YELLOW = float(os.getenv('THRESHOLD_YELLOW', 2.8))
THRESHOLD_ORANGE = float(os.getenv('THRESHOLD_ORANGE', 4.5))
THRESHOLD_RED = float(os.getenv('THRESHOLD_RED', 7.1))

def main():
    file_list = glob.glob(os.path.join(DATA_DIR, '*.txt'))
    
    if not file_list:
        print(f"No text files found in {DATA_DIR}.")
        return

    parsed_data = [parse_file(f) for f in file_list]
    df_raw = pd.DataFrame(parsed_data)

    results = []
    grouped = df_raw.groupby('Equipment')
    
    for equipment, group in grouped:
        group = group.sort_values('Date')
        latest_rms = group['RMS'].iloc[-1]
        
        # คลีนชื่อแก้ปัญหา (CHPP)
        clean_equipment = equipment.replace("(CHPP) ", "").strip()
        
        status = get_iso_status(latest_rms, THRESHOLD_YELLOW, THRESHOLD_ORANGE, THRESHOLD_RED)
        trend, est_failure = calculate_trend_and_failure(group, THRESHOLD_RED)
        
        results.append({
            'Equipment': clean_equipment,
            'Latest_RMS': round(latest_rms, 2),
            'Current_Status': status,
            'Trend': trend,
            'Est_Failure_Date': est_failure
        })

    # รวมข้อมูลที่ชื่อซ้ำกันหลังคลีนแล้ว (ลบแถวที่ซ้ำซ้อน)
    final_df = pd.DataFrame(results).drop_duplicates(subset=['Equipment'], keep='last')
    
    final_df.to_csv(OUTPUT_FILE, index=False)
    print("=== Predictive Maintenance Report ===")
    print(final_df.to_string(index=False))

if __name__ == "__main__":
    main()