import argparse
import base64
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

import holidays
import pandas as pd

# ── brand ────────────────────────────────────────────────────
BRAND_PRIMARY = "#F25E3D"
BRAND_PRIMARY_DARK = "#D44B2C"
BRAND_DARK    = "#0D0D0D"
BRAND_LIGHT   = "#F2F2F2"

# ── holidays ─────────────────────────────────────────────────
_BR_HOLIDAYS = holidays.Brazil(years=range(2020, 2032))

# ── logo base64 (filled in Task 6) ──────────────────────────
LOGO_B64 = ""


def business_days_diff(start: datetime, end: datetime) -> int:
    """Úteis entre start e end (Mon–Fri, excluindo feriados nacionais BR)."""
    s = start.date()
    e = end.date()
    if s >= e:
        return 0
    count = 0
    cur = s
    while cur < e:
        if cur.weekday() < 5 and cur not in _BR_HOLIDAYS:
            count += 1
        cur += timedelta(days=1)
    return count
