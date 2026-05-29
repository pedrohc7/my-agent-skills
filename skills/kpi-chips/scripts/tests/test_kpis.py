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


import pandas as pd
from gerar_kpis import calc_kpis, parse_dt

def _make_df(rows):
    """Helper: create minimal orders dataframe."""
    return pd.DataFrame(rows)

def test_calc_kpis_all_d1():
    df = _make_df([
        {'Status': 'Concluído', 'Criado em': '12/05/2026 08:00:00',
         'Fechado em': '13/05/2026 15:00:00', 'Tentativas': 1,
         'Cumprimento de Agenda': 'Sim', 'Distância em KM': 25.0,
         'Transportador': 'João', 'Destino - Cidade': 'RIO DE JANEIRO'},
        {'Status': 'Concluído', 'Criado em': '12/05/2026 08:00:00',
         'Fechado em': '13/05/2026 16:00:00', 'Tentativas': 1,
         'Cumprimento de Agenda': 'Sim', 'Distância em KM': 30.0,
         'Transportador': 'João', 'Destino - Cidade': 'RIO DE JANEIRO'},
    ])
    k = calc_kpis(df)
    assert k['total'] == 2
    assert k['n_concluded'] == 2
    assert k['taxa_entrega'] == 100.0
    assert k['taxa_d1'] == 100.0
    assert k['taxa_sla'] == 100.0
    assert k['taxa_d3plus'] == 0.0

def test_calc_kpis_pa_nao_identificado_counts_as_undelivered():
    df = _make_df([
        {'Status': 'Concluído',          'Criado em': '12/05/2026 08:00:00',
         'Fechado em': '13/05/2026 15:00:00', 'Tentativas': 1,
         'Cumprimento de Agenda': 'Sim', 'Distância em KM': 25.0,
         'Transportador': 'João', 'Destino - Cidade': 'RIO DE JANEIRO'},
        {'Status': 'PA não Identificado', 'Criado em': '12/05/2026 08:00:00',
         'Fechado em': None,              'Tentativas': 0,
         'Cumprimento de Agenda': None,   'Distância em KM': None,
         'Transportador': None,           'Destino - Cidade': 'NITEROI'},
    ])
    k = calc_kpis(df)
    assert k['total'] == 2
    assert k['taxa_entrega'] == 50.0
    assert k['taxa_sla'] == 50.0

def test_parse_dt_formats():
    assert parse_dt('13/05/2026 15:12:04') == datetime(2026, 5, 13, 15, 12, 4)
    assert parse_dt('13/05/2026 15:12')    == datetime(2026, 5, 13, 15, 12, 0)
    assert parse_dt(None) is None
    assert parse_dt(float('nan')) is None


from gerar_kpis import calc_transporter_kpis, calc_city_kpis

def _full_df():
    return pd.DataFrame([
        {'Status': 'Concluído', 'Criado em': '12/05/2026 08:00:00',
         'Fechado em': '13/05/2026 15:00:00', 'Tentativas': 1,
         'Cumprimento de Agenda': 'Sim', 'Distância em KM': 25.0,
         'Transportador': 'João', 'Destino - Cidade': 'RIO DE JANEIRO'},
        {'Status': 'Concluído', 'Criado em': '12/05/2026 08:00:00',
         'Fechado em': '14/05/2026 15:00:00', 'Tentativas': 2,
         'Cumprimento de Agenda': 'Não', 'Distância em KM': 30.0,
         'Transportador': 'Maria', 'Destino - Cidade': 'NITEROI'},
    ])

def test_calc_transporter_kpis_returns_one_row_per_transporter():
    df = _full_df()
    kpis = calc_kpis(df)
    rows = calc_transporter_kpis(df, kpis['_concluded_with_dx'])
    names = [r['nome'] for r in rows]
    assert 'João' in names
    assert 'Maria' in names

def test_calc_transporter_kpis_joao_is_d1():
    df = _full_df()
    kpis = calc_kpis(df)
    rows = calc_transporter_kpis(df, kpis['_concluded_with_dx'])
    joao = next(r for r in rows if r['nome'] == 'João')
    assert joao['pct_d1'] == 100.0
    assert joao['pct_sla'] == 100.0

def test_calc_city_kpis_min_10_filter():
    df = _full_df()
    kpis = calc_kpis(df)
    rows = calc_city_kpis(df, kpis['_concluded_with_dx'], min_orders=1)
    cities = [r['cidade'] for r in rows]
    assert 'RIO DE JANEIRO' in cities
