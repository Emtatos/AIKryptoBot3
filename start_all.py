# =============================================================================
# start_all.py – Initierar och kör hela AIKryptoBot3-flödet stegvis
# =============================================================================

import sys
import os
import traceback

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.price_updater import update_price_history
from core.price_logger import log_live_prices
from core.momentum_generator import generate_momentum
from reporting.top5_report import send_top5
from reporting.portfolio_report import send_portfolio_report
from core.score_logger import log_top_scores
from core.signal_logger import log_signals
from core.signal_outcome_tracker import log_signal_outcomes
from core.signal_accuracy_analyzer import analyze_signal_accuracy
from core.signal_timing_analyzer import analyze_signal_timing
from core.adaptive_switch_threshold import adjust_switch_threshold
from core.adaptive_buy_score import adjust_min_buy_score
from core.trend_shift_detector import detect_trend_shifts
from reporting.runtime_info import generate_runtime_info
from reporting.telegram import send_telegram

print("\n=== AIKryptoBot3 – Startar full körning ===")

# Skicka datum/tid först
try:
    msg = generate_runtime_info()
    send_telegram(msg)
except Exception as e:
    print("[X] Fel vid runtime_info:")
    traceback.print_exc()

# Logga livepris med timestamp
try:
    log_live_prices()
except Exception as e:
    print("[X] Fel vid log_live_prices:")
    traceback.print_exc()

# Identifiera snabba trendskiften
try:
    detect_trend_shifts()
except Exception as e:
    print("[X] Fel vid trend_shift_detector:")
    traceback.print_exc()

try:
    update_price_history()
except Exception as e:
    print("[X] Fel vid update_price_history:")
    traceback.print_exc()

try:
    generate_momentum()
except Exception as e:
    print("[X] Fel vid generate_momentum:")
    traceback.print_exc()

try:
    log_top_scores()
except Exception as e:
    print("[X] Fel vid score_logger:")
    traceback.print_exc()

try:
    log_signals()
except Exception as e:
    print("[X] Fel vid signal_logger:")
    traceback.print_exc()

try:
    log_signal_outcomes()
except Exception as e:
    print("[X] Fel vid signal_outcome_tracker:")
    traceback.print_exc()

try:
    analyze_signal_accuracy()
except Exception as e:
    print("[X] Fel vid signal_accuracy_analyzer:")
    traceback.print_exc()

try:
    analyze_signal_timing()
except Exception as e:
    print("[X] Fel vid signal_timing_analyzer:")
    traceback.print_exc()

try:
    adjust_switch_threshold()
except Exception as e:
    print("[X] Fel vid adaptive_switch_threshold:")
    traceback.print_exc()

try:
    adjust_min_buy_score()
except Exception as e:
    print("[X] Fel vid adaptive_buy_score:")
    traceback.print_exc()

try:
    send_top5()
except Exception as e:
    print("[X] Fel vid send_top5:")
    traceback.print_exc()

try:
    send_portfolio_report()
except Exception as e:
    print("[X] Fel vid send_portfolio_report:")
    traceback.print_exc()

try:
    import tools.recommendation_engine
except Exception as e:
    print("[X] Fel i recommendation_engine:")
    traceback.print_exc()
