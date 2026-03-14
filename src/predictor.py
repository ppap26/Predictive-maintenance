import pandas as pd
from sklearn.linear_model import LinearRegression

def calculate_trend_and_failure(group_df, critical_threshold):
    trend = "Stable or Improving"
    est_failure_date = "N/A"
    
    # ต้องมีข้อมูลอย่างน้อย 2 จุดถึงจะหา Trend ได้
    if len(group_df) > 1:
        group_df = group_df.copy()
        group_df['Days'] = (group_df['Date'] - group_df['Date'].min()).dt.days
        
        X = group_df[['Days']].values
        y = group_df['RMS'].values
        
        model = LinearRegression()
        model.fit(X, y)
        slope = model.coef_[0]
        
        if slope > 0:
            trend = "Degrading"
            # คำนวณหาวันที่ค่าทะลุเกณฑ์ Critical
            days_to_failure = (critical_threshold - model.intercept_) / slope
            if days_to_failure > 0:
                future_days = days_to_failure - group_df['Days'].max()
                if future_days > 0:
                    est_date = group_df['Date'].max() + pd.Timedelta(days=future_days)
                    est_failure_date = est_date.strftime('%Y-%m-%d')
                    
    return trend, est_failure_date