def get_iso_status(rms_value):
    """จัดกลุ่มสถานะเครื่องจักรตามมาตรฐาน ISO 10816-3"""
    if rms_value < 0.7:
        return "Excellent"
    elif rms_value < 2.8:
        return "Good"
    elif rms_value < 4.5:
        return "Acceptable"
    elif rms_value < 7.1:
        return "Restricted"
    else:
        return "Damage"