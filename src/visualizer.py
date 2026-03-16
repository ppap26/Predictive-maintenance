import matplotlib.pyplot as plt
import numpy as np
import os

def plot_trend_comparison(df, output_dir="output_plots"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    plt.figure(figsize=(10, 6))
    
    for equipment, group in df.groupby('Equipment'):
        group = group.sort_values('Date')
        x_labels = group['Date'].dt.strftime('%b') # แปลงเป็นชื่อเดือนแบบย่อ Jun, Sep, Oct
        plt.plot(x_labels, group['RMS'], marker='o', label=equipment)
        
    # วาดเส้น ISO
    plt.axhline(y=4.5, color='red', linestyle='--', label='ISO Restricted limit')
    
    plt.title('Vibration Trend Comparison')
    plt.ylabel('Velocity RMS (mm/s)')
    plt.xlabel('Month')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'Trend_Comparison.png'))
    plt.close()

def plot_rul_prediction(equipment, group_df, model_params, threshold=4.5, output_dir="output_plots"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    plt.figure(figsize=(8, 5))
    
    plt.plot(group_df['Month_Index'], group_df['RMS'], marker='o', label='Actual RMS')
    
    # วาดเส้นพยากรณ์ AI
    if model_params and model_params['slope'] > 0:
        slope = model_params['slope']
        intercept = model_params['intercept']
        
        # วาดกราฟไปข้างหน้าจนกว่าจะชน 4.5
        months_to_failure = (threshold - intercept) / slope
        max_x = max(8, int(months_to_failure) + 2)
        
        x_pred = np.arange(1, max_x)
        y_pred = slope * x_pred + intercept
        
        plt.plot(x_pred, y_pred, linestyle='--', color='orange', label=f'{equipment} prediction')
    else:
        max_x = 8
        
    plt.axhline(y=threshold, color='red', linestyle='--', label='ISO Restricted limit')
    
    plt.title(f'Remaining Useful Life Prediction - {equipment}')
    plt.ylabel('Velocity RMS (mm/s)')
    plt.xlabel('Month index')
    plt.xlim(0, max_x)
    plt.ylim(0, max(group_df['RMS'].max() + 1, threshold + 1))
    plt.legend()
    plt.grid(True)
    
    # เซฟรูปโดยลบช่องว่างในชื่อไฟล์ออก
    safe_name = equipment.replace(" ", "_").replace("(", "").replace(")", "")
    plt.savefig(os.path.join(output_dir, f'RUL_{safe_name}.png'))
    plt.close()