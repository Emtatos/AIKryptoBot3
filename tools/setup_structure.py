import os

base_path = r"C:\AIKryptoBot3"
folders = [
    "config",
    "core",
    "reporting",
    "broker",
    "scheduler",
    "learning",
    "data",
    "logs"
]

for folder in folders:
    path = os.path.join(base_path, folder)
    os.makedirs(path, exist_ok=True)
    print(f"[OK] Skapat: {path}")
