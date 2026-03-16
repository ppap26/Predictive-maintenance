import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_trend_and_failure(group_df, threshold_limit=4.5):
    latest_rms = group_df['RMS'].iloc[-1]
    health_ratio = (latest_rms / threshold_limit) * 100
    
    trend = "Stable"
    rul_months = "N/A"
    model_params = None
    
    if len(group_df) > 1:
        # ตรวจสอบว่ามี Month_Index หรือยัง ถ้าไม่มีค่อยสร้าง
        if 'Month_Index' not in group_df.columns:
            min_date = group_df['Date'].min()
            group_df['Month_Index'] = (group_df['Date'].dt.year - min_date.year) * 12 + \
                                      (group_df['Date'].dt.month - min_date.month) + 1
        
        X = group_df[['Month_Index']].values
        y = group_df['RMS'].values
        
        model = LinearRegression()
        model.fit(X, y)
        slope = model.coef_[0]
        intercept = model.intercept_
        model_params = {'slope': slope, 'intercept': intercept}
        
        if slope > 0.001: # กำหนด threshold เล็กน้อยเพื่อให้ไม่ไวต่อการแกว่งเล็กๆ
            trend = "Degrading"
            # พยากรณ์เดือนที่จะถึงขีดจำกัด
            total_months = (threshold_limit - intercept) / slope
            remaining = total_months - group_df['Month_Index'].max()
            rul_months = round(max(0, remaining), 1)
        else:
            trend = "Stable"

    return trend, health_ratio, rul_months, model_params