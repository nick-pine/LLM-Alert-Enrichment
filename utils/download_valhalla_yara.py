"""
Utility script to download YARA rules from Valhalla API (Nextron Systems)
Saves rules to yara_rules/valhalla_rules.yar
"""
import requests
import os

VALHALLA_API_URL = "https://valhalla.nextron-systems.com/api/v1/yara/export"
OUT_DIR = "yara_rules"
OUT_FILE = os.path.join(OUT_DIR, "valhalla_rules.yar")

os.makedirs(OUT_DIR, exist_ok=True)

def download_valhalla_yara_rules():
    print(f"Downloading YARA rules from Valhalla API: {VALHALLA_API_URL}")
    response = requests.get(VALHALLA_API_URL)
    if response.status_code == 200:
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"YARA rules saved to {OUT_FILE}")
    else:
        print(f"Failed to download rules: {response.status_code}")

if __name__ == "__main__":
    download_valhalla_yara_rules()
