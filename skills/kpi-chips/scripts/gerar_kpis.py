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


def parse_dt(value) -> datetime | None:
    """Parse date strings from the xlsx (dd/mm/yyyy HH:MM:SS or HH:MM)."""
    if value is None:
        return None
    try:
        if isinstance(value, float) and (value != value):  # NaN
            return None
    except Exception:
        pass
    s = str(value).strip()
    for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M'):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None


def _col(df: pd.DataFrame, *candidates: str) -> str:
    """Return first matching column name (handles encoding variants)."""
    for c in candidates:
        if c in df.columns:
            return c
    for c in df.columns:
        for cand in candidates:
            if cand.lower() in c.lower():
                return c
    raise KeyError(f"Column not found: {candidates}")


def load_data(path: str) -> pd.DataFrame:
    """Load xlsx; copies to temp first if OneDrive has it locked."""
    try:
        return pd.read_excel(path, engine='openpyxl')
    except PermissionError:
        tmp = Path(tempfile.mktemp(suffix='.xlsx'))
        shutil.copy2(path, tmp)
        try:
            return pd.read_excel(tmp, engine='openpyxl')
        finally:
            tmp.unlink(missing_ok=True)


def calc_kpis(df: pd.DataFrame) -> dict:
    col_criado  = _col(df, 'Criado em')
    col_fechado = _col(df, 'Fechado em')
    col_status  = _col(df, 'Status')
    col_tent    = _col(df, 'Tentativas')
    col_agenda  = _col(df, 'Cumprimento de Agenda')

    total = len(df)
    concluded = df[df[col_status].str.contains('Conclu', na=False)].copy()
    n_concluded = len(concluded)

    # D+X per order
    def _dx(row):
        c = parse_dt(row[col_criado])
        f = parse_dt(row[col_fechado])
        if c and f:
            return business_days_diff(c, f)
        return None

    concluded['_dx'] = concluded.apply(_dx, axis=1)
    cwd = concluded[concluded['_dx'].notna()]

    d0      = int((cwd['_dx'] == 0).sum())
    d1      = int((cwd['_dx'] == 1).sum())
    d2      = int((cwd['_dx'] == 2).sum())
    d3plus  = int((cwd['_dx'] >= 3).sum())
    sla_ok  = d0 + d1 + d2

    tent = concluded[col_tent].fillna(0)
    avg_tent    = float(tent.mean()) if n_concluded else 0.0
    pct_primeira = float((tent == 1).sum() / n_concluded * 100) if n_concluded else 0.0

    agenda_vals = df[col_agenda]
    has_agenda  = agenda_vals.notna().sum()
    pct_agenda  = float((agenda_vals == 'Sim').sum() / has_agenda * 100) if has_agenda else 0.0

    def pct(n): return round(n / total * 100, 1) if total else 0.0

    return {
        'total': total,
        'n_concluded': n_concluded,
        'taxa_entrega': pct(n_concluded),
        'taxa_sla':     pct(sla_ok),
        'taxa_d0':      pct(d0),
        'taxa_d1':      pct(d1),
        'taxa_d2':      pct(d2),
        'taxa_d3plus':  pct(d3plus),
        'd0': d0, 'd1': d1, 'd2': d2, 'd3plus': d3plus, 'sla_ok': sla_ok,
        'avg_tentativas': round(avg_tent, 2),
        'pct_primeira':   round(pct_primeira, 1),
        'pct_agenda':     round(pct_agenda, 1),
        '_concluded_with_dx': cwd,
    }
