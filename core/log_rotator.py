# =============================================================================
# =============================================================================

import os
import pandas as pd
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MAX_FILE_SIZE_KB = 500
MAX_ROWS_KEEP = 1000

LOG_FILES = [
    "logs/signal_outcome.csv",
    "logs/signal_timing_summary.csv", 
    "logs/score_log.csv",
    "logs/signal_log.csv",
    "logs/signal_accuracy.csv",
    "logs/threshold_history.csv",
    "logs/buy_log.csv",
    "logs/sell_log.csv",
    "logs/switch_log.csv",
    "logs/trend_shift_signals.csv"
]

def rotate_log_file(file_path):
    """Roterar en loggfil om den är för stor"""
    full_path = os.path.join(project_root, file_path)
    
    if not os.path.exists(full_path):
        return
    
    size_kb = os.path.getsize(full_path) / 1024
    if size_kb <= MAX_FILE_SIZE_KB:
        return
    
    print(f"[LOG_ROTATION] Roterar {file_path} ({size_kb:.1f}KB)")
    
    try:
        df = pd.read_csv(full_path)
        if len(df) > MAX_ROWS_KEEP:
            df_trimmed = df.tail(MAX_ROWS_KEEP)
            
            backup_path = f"{full_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(full_path, backup_path)
            
            df_trimmed.to_csv(full_path, index=False)
            print(f"[LOG_ROTATION] {file_path} trimmad från {len(df)} till {len(df_trimmed)} rader")
        
    except Exception as e:
        print(f"[LOG_ROTATION] Fel vid rotation av {file_path}: {e}")

def rotate_all_logs():
    """Roterar alla loggfiler"""
    print("[LOG_ROTATION] Kontrollerar loggfilsstorlekar...")
    for log_file in LOG_FILES:
        rotate_log_file(log_file)
    print("[LOG_ROTATION] Loggrensning klar")

if __name__ == "__main__":
    rotate_all_logs()
