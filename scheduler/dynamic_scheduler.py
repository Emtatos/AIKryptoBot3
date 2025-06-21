# =============================================================================
# dynamic_scheduler.py – Kör AIKryptoBot3 i loop med dynamiska intervall
# =============================================================================

import time
import datetime
import os

# Justera sökvägen om nödvändigt
RUN_COMMAND = "python ../start_all.py"

# Intervall i minuter baserat på timme
def get_interval():
    now = datetime.datetime.now().time()
    hour = now.hour

    if 8 <= hour < 22:
        return 15  # Aktiv handelstid
    elif 22 <= hour or hour < 2:
        return 30  # Kväll/natt
    else:
        return 60  # Tidig morgon (02–08)

print("[SCHEDULER] AIKryptoBot3 Autonomous Scheduler startad")
print("[SCHEDULER] Systemet kommer att köra automatiskt 24/7")

while True:
    now = datetime.datetime.now()
    print(f"\n[START] Körning startad {now.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        result = os.system(RUN_COMMAND)
        if result != 0:
            print(f"[WARNING] Körning avslutades med kod {result}")
            
        if now.hour % 6 == 0 and now.minute < 30:
            try:
                import sys
                import os
                project_root = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(project_root)
                sys.path.insert(0, parent_dir)
                from reporting.status_report import send_status_report
                send_status_report()
                print("[OK] Status rapport skickad")
            except Exception as e:
                print(f"[WARNING] Status rapport misslyckades: {e}")
                
    except Exception as e:
        print(f"[X] Fel under körning: {e}")
        print("[RECOVERY] Fortsätter med nästa körning...")

    interval = get_interval()
    next_run = datetime.datetime.now() + datetime.timedelta(minutes=interval)
    print(f"[INFO] Nästa körning: {next_run.strftime('%H:%M')} (om {interval} min)")
    print("[AUTONOMOUS] Systemet kör automatiskt utan manuell intervention")
    time.sleep(interval * 60)
