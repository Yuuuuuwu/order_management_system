import hashlib
  import urllib.parse

  def verify_check_mac_value(data: dict) -> bool:
      """
      驗證 CheckMacValue
      """
      from flask import current_app

      hash_key = current_app.config.get('ECPAY_HASH_KEY')
      hash_iv = current_app.config.get('ECPAY_HASH_IV')

      # 移除 CheckMacValue 後排序參數
      check_data = {k: v for k, v in data.items() if k != 'CheckMacValue'}
      ordered = sorted(check_data.items())
      raw = "&".join(f"{k}={v}" for k, v in ordered)
      raw = f"HashKey={hash_key}&{raw}&HashIV={hash_iv}"

      # URL encode 並轉小寫
      urlenc = urllib.parse.quote_plus(raw).lower()

      # 還原綠界要求的保留字元
      for enc, ch in [
          ('%2d','-'), ('%5f','_'), ('%2e','.'),
          ('%21','!'), ('%2a','*'), ('%28','('), ('%29',')'),
      ]:
          urlenc = urlenc.replace(enc, ch)

      # 使用 SHA256 (和 gen_mac 函數一致)
      calculated_mac = hashlib.sha256(urlenc.encode('utf-8')).hexdigest().upper()

      return calculated_mac == data.get('CheckMacValue')