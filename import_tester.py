# =============================================================================
# import_tester.py – Verifierar att alla kärnmoduler i AIKryptoBot3 kan importeras
# =============================================================================

import traceback

print("=== Importtest AIKryptoBot3 ===")

modules = [
    "config.coin_config",
    "config.telegram_config",
    "core.momentum_generator",
    "reporting.top5_report",
    "reporting.telegram",
    "start_all"
]

for mod in modules:
    try:
        __import__(mod)
        print(f"[OK] {mod}")
    except Exception:
        print(f"[X] FEL i: {mod}")
        traceback.print_exc()

print("=== Importtest färdig ===")
