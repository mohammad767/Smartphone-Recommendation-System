from apps.smartphones.models import Smartphone


STORAGE_SPEED_RANK = {
    "emmc": 1,
    "ufs2_2": 2,
    "ufs3_1": 3,
    "ufs4_0": 4,
}
DISPLAY_TYPE_RANK = {

    "LCD": 1,
    "IPS": 2,
    "OLED": 3,
    "AMOLED": 4,
    "S-AMOLED": 5,

}


REFERENCE_MAX = {

    "antutu": 2200000,"ram": 24,"storage_speed": 4,
    "battery": 6000,"display_type": 5 ,
    "charging": 240,"refresh": 165,
    "ppi": 550,"camera": 200
    }


def _scale(value, max_reference):

    if value is None:
        return 0


    return min(100,(value / max_reference) * 100)
    
def performance_score(phone):

    cpu = _scale(
        phone.chipset.antutu_score,
        REFERENCE_MAX["antutu"]
    )


    ram = _scale(
        phone.ram_gb,
        REFERENCE_MAX["ram"]
    )


    storage = _scale(
    STORAGE_SPEED_RANK.get(phone.storage_type,1),REFERENCE_MAX["storage_speed"])

    return round(
        cpu * 0.6 +
        ram * 0.25 +
        storage * 0.15,
        2
    )
    
    
def battery_score(phone) : 
    
    capacity = _scale(phone.battery_mah,REFERENCE_MAX["battery"])
    
    charging = _scale(phone.fast_charging_w,REFERENCE_MAX["charging"])
    
    
    return round(
        capacity * 0.7 +
        charging * 0.3,
        2
    )
    
def display_score(phone):

    panel = DISPLAY_TYPE_RANK.get(
        phone.display_type,
        1
    )


    panel_score = _scale(panel,5)


    refresh = _scale(phone.display_refresh_hz,REFERENCE_MAX["refresh"])


    ppi = _scale(phone.display_ppi,REFERENCE_MAX["ppi"])


    return round(
        refresh * 0.35 +
        ppi * 0.35 +
        panel_score * 0.30,
        2
    )
    
def camera_score(phone):

    megapixel = _scale(
        phone.main_camera_mp,
        REFERENCE_MAX["camera"]
    )


    ois_bonus = 10 if phone.has_ois else 0


    return round(min(100,megapixel * 0.85 + ois_bonus),2)
    
    
def calculate_and_save_scores(phone):
    
    phone.performance_score = performance_score(phone)
    phone.battery_score = battery_score(phone)
    phone.display_score =  display_score(phone)
    phone.camera_score = camera_score(phone)
    phone.save()
    
    
    
def get_phone_scores(phone):
    return {
        "performance": phone.performance_score,
        "battery": phone.battery_score,
        "display": phone.display_score,
        "camera": phone.camera_score,
    }