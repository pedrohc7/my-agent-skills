import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from gerar_kpis import business_days_diff

def test_same_day_is_d0():
    start = datetime(2026, 5, 12, 8, 0)
    end   = datetime(2026, 5, 12, 18, 0)
    assert business_days_diff(start, end) == 0

def test_next_business_day_is_d1():
    start = datetime(2026, 5, 11, 8, 0)
    end   = datetime(2026, 5, 12, 15, 0)
    assert business_days_diff(start, end) == 1

def test_skips_weekend():
    start = datetime(2026, 5, 8, 8, 0)
    end   = datetime(2026, 5, 11, 15, 0)
    assert business_days_diff(start, end) == 1

def test_skips_friday_to_tuesday():
    start = datetime(2026, 5, 8, 8, 0)
    end   = datetime(2026, 5, 12, 15, 0)
    assert business_days_diff(start, end) == 2

def test_skips_national_holiday():
    start = datetime(2025, 12, 29, 8, 0)
    end   = datetime(2026, 1, 2, 15, 0)
    assert business_days_diff(start, end) == 3

def test_end_before_start_returns_zero():
    start = datetime(2026, 5, 12, 15, 0)
    end   = datetime(2026, 5, 11, 8, 0)
    assert business_days_diff(start, end) == 0
