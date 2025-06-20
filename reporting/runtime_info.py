# =============================================================================
# runtime_info.py – Skapar en textsträng med datum, tid och nästa körning
# Anpassar tiden beroende på tid på dygnet
# =============================================================================

from datetime import datetime, timedelta

def get_dynamic_interval():
    now = datetime.now()
    hour = now.hour

    if 8 <= hour <= 18:
        return 15  # dagtid = 15 min
    elif 6 <= hour < 8 or 18 < hour <= 22:
        return 30  # morgon/kväll = 30 min
    else:
        return 60  # natt = 60 min

def generate_runtime_info():
    now = datetime.now()
    interval = get_dynamic_interval()
    next_time = now + timedelta(minutes=interval)

    lines = [
        f"📅 Datum: {now.date()}",
        f"⏰ Tid: {now.strftime('%H:%M')}",
        f"\n⏳ Nästa körning: {next_time.strftime('%H:%M')}"
    ]
    return "\n".join(lines)

# TEST
if __name__ == "__main__":
    print(generate_runtime_info())

