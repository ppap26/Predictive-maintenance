def get_iso_status(rms_value, threshold_yellow, threshold_orange, threshold_red):
    if rms_value >= threshold_red:
        return "Zone D (Red) - DAMAGE OCCURS"
    elif rms_value >= threshold_orange:
        return "Zone C (Orange) - WARNING"
    elif rms_value >= threshold_yellow:
        return "Zone B (Yellow) - ALARM"
    else:
        return "Zone A (Green) - GOOD"