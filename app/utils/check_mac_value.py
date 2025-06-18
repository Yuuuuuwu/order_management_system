import hashlib
import urllib.parse

def verify_check_mac_value(data: dict) -> bool:
    """
    驗證 CheckMacValue
    """
    hash_key = 'YourHashKey'
    hash_iv = 'YourHashIV'

    # 排序參數
    sorted_data = sorted(data.items())
    encoded_str = urllib.parse.urlencode(sorted_data)

    # 加入 HashKey 和 HashIV
    raw_str = f'HashKey={hash_key}&{encoded_str}&HashIV={hash_iv}'

    # 轉換為大寫 MD5
    check_mac_value = hashlib.md5(raw_str.encode('utf-8')).hexdigest().upper()

    return check_mac_value == data.get('CheckMacValue')
