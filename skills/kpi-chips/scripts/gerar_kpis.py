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
LOGO_B64 = "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"


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
    # D+0 = fechado dentro de 24h da criação (datetime real, não datas)
    # D+1+ = dias úteis (business_days_diff), independente do critério 24h
    def _dx(row):
        c = parse_dt(row[col_criado])
        f = parse_dt(row[col_fechado])
        if c and f:
            if (f - c).total_seconds() <= 86400:  # ≤ 24h
                return 0
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


def calc_transporter_kpis(df: pd.DataFrame, cwd: pd.DataFrame) -> list[dict]:
    """Per-transporter KPIs. cwd = concluded rows with _dx column."""
    col_transp = _col(df, 'Transportador')
    col_tent   = _col(df, 'Tentativas')
    col_dist   = _col(df, 'Dist')   # matches 'Distância em KM'

    results = []
    for name, grp in df.groupby(col_transp):
        if pd.isna(name):
            continue
        total_t = len(grp)
        conc_t  = cwd[cwd.index.isin(grp.index)]
        n_conc  = len(conc_t)

        def _pct(n): return round(n / total_t * 100, 1) if total_t else 0.0

        d0_t = int((conc_t['_dx'] == 0).sum())
        d1_t = int((conc_t['_dx'] == 1).sum())
        d2_t = int((conc_t['_dx'] == 2).sum())
        d3_t = int((conc_t['_dx'] >= 3).sum())
        sla_t = d0_t + d1_t + d2_t

        tent = grp[col_tent].fillna(0)
        dist_vals = grp[col_dist].dropna()

        results.append({
            'nome':          str(name),
            'total':         total_t,
            'pct_conclusao': _pct(n_conc),
            'pct_sla':       _pct(sla_t),
            'pct_d0':        _pct(d0_t),
            'pct_d1':        _pct(d1_t),
            'pct_d2':        _pct(d2_t),
            'pct_d3plus':    _pct(d3_t),
            'avg_tentativas': round(float(tent.mean()), 2) if total_t else 0.0,
            'pct_primeira':  round(float((tent == 1).sum() / total_t * 100), 1) if total_t else 0.0,
            'avg_dist_km':   round(float(dist_vals.mean()), 1) if len(dist_vals) else 0.0,
        })

    return sorted(results, key=lambda x: x['pct_sla'], reverse=True)


def calc_city_kpis(df: pd.DataFrame, cwd: pd.DataFrame, min_orders: int = 10) -> list[dict]:
    """Per-city KPIs for cities with >= min_orders."""
    col_cidade = _col(df, 'Destino - Cidade')
    col_tent   = _col(df, 'Tentativas')

    results = []
    for city, grp in df.groupby(col_cidade):
        if pd.isna(city) or len(grp) < min_orders:
            continue
        total_c = len(grp)
        conc_c  = cwd[cwd.index.isin(grp.index)]

        def _pct(n): return round(n / total_c * 100, 1) if total_c else 0.0

        d1_c  = int((conc_c['_dx'] == 1).sum())
        sla_c = int((conc_c['_dx'] <= 2).sum())
        tent  = grp[col_tent].fillna(0)

        results.append({
            'cidade':         str(city),
            'total':          total_c,
            'pct_sla':        _pct(sla_c),
            'pct_d1':         _pct(d1_c),
            'avg_tentativas': round(float(tent.mean()), 2) if total_c else 0.0,
        })

    return sorted(results, key=lambda x: x['total'], reverse=True)

# ── HTML template ────────────────────────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Relatório de KPIs — CSS Solutions</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --brand:#F25E3D;--brand-dark:#D44B2C;--page:#F2F2F2;
  --card:#fff;--dark:#0D0D0D;--muted:#6B7080;
  --green:#10B981;--amber:#F59E0B;--red:#EF4444;
  --border:#E5E7EB;
}}
body{{font-family:'Inter',system-ui,sans-serif;background:var(--page);color:var(--dark);min-width:320px}}
.hdr{{background:#fff;border-bottom:3px solid var(--brand);padding:20px 32px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
.hdr-logo{{height:64px;width:auto}}
.hdr-meta{{text-align:right}}
.hdr-title{{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:22px;text-transform:uppercase;letter-spacing:.5px;color:var(--dark)}}
.hdr-sub{{font-size:12px;color:var(--muted);margin-top:2px}}
.main{{max-width:1280px;margin:0 auto;padding:28px 24px 48px}}
.section-title{{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:18px;text-transform:uppercase;letter-spacing:.5px;margin:32px 0 14px;display:flex;align-items:center;gap:8px}}
.section-title::after{{content:'';flex:1;height:2px;background:var(--border)}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:8px}}
.card{{background:var(--card);border-radius:10px;padding:18px 16px 14px;border-top:4px solid var(--border);box-shadow:0 1px 3px rgba(0,0,0,.07)}}
.card.c-brand{{border-top-color:var(--brand)}}.card.c-green{{border-top-color:var(--green)}}.card.c-amber{{border-top-color:var(--amber)}}.card.c-red{{border-top-color:var(--red)}}.card.c-gray{{border-top-color:#9CA3AF}}
.card-val{{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:36px;line-height:1;color:var(--dark)}}
.card-val .unit{{font-size:22px;font-weight:700}}
.card-label{{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-top:6px}}
.card-sub{{font-size:11px;color:#9CA3AF;margin-top:2px}}
.dist-wrap{{background:var(--card);border-radius:10px;padding:20px 24px;box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:8px}}
.dist-row{{display:grid;grid-template-columns:50px 1fr 80px;align-items:center;gap:10px;margin-bottom:10px}}
.dist-row:last-child{{margin-bottom:0}}
.dist-label{{font-size:12px;font-weight:700;color:var(--dark)}}
.dist-bar-track{{background:#F3F4F6;border-radius:4px;height:16px;overflow:hidden}}
.dist-bar-fill{{height:100%;border-radius:4px;transition:width .6s ease}}
.dist-bar-fill.green{{background:var(--green)}}.dist-bar-fill.amber{{background:var(--amber)}}.dist-bar-fill.red{{background:var(--red)}}
.dist-pct{{font-size:12px;font-weight:600;text-align:right}}
.tbl-wrap{{background:var(--card);border-radius:10px;overflow:auto;box-shadow:0 1px 3px rgba(0,0,0,.07)}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
thead th{{background:#F9FAFB;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--muted);padding:10px 14px;text-align:left;cursor:pointer;white-space:nowrap;user-select:none;border-bottom:2px solid var(--border)}}
thead th:hover{{color:var(--dark)}}
thead th.sort-asc::after{{content:' ↑'}}thead th.sort-desc::after{{content:' ↓'}}
tbody tr:nth-child(even){{background:#FAFAFA}}tbody tr:hover{{background:#FFF5F2}}
td{{padding:9px 14px;border-bottom:1px solid var(--border);color:var(--dark)}}
td.num{{font-variant-numeric:tabular-nums;text-align:right}}
.badge{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700}}
.badge-green{{background:#D1FAE5;color:#065F46}}.badge-amber{{background:#FEF3C7;color:#92400E}}.badge-red{{background:#FEE2E2;color:#991B1B}}
.ftr{{text-align:center;font-size:11px;color:var(--muted);padding:24px;border-top:1px solid var(--border);margin-top:32px}}
.ftr strong{{color:var(--brand)}}
</style>
</head>
<body>
<div class="hdr">
  <img class="hdr-logo" src="data:image/jpeg;base64,{logo_b64}" alt="CSS Solutions"/>
  <div class="hdr-meta">
    <div class="hdr-title">Relatório de KPIs — Chips</div>
    <div class="hdr-sub">Período: {periodo} &nbsp;·&nbsp; Gerado em: {gerado_em}</div>
  </div>
</div>
<div class="main">
<div class="section-title">Resumo Geral</div>
<div class="cards">
  <div class="card c-brand"><div class="card-val">{kpi_total}</div><div class="card-label">Total de Pedidos</div></div>
  <div class="card c-gray"><div class="card-val">{kpi_taxa_entrega}<span class="unit">%</span></div><div class="card-label">Taxa de Entrega</div><div class="card-sub">{kpi_n_concluded} concluídos</div></div>
  <div class="card {sla_card_class}"><div class="card-val">{kpi_taxa_sla}<span class="unit">%</span></div><div class="card-label">SLA ≤ D+2</div><div class="card-sub">{kpi_sla_ok} pedidos no prazo</div></div>
  <div class="card c-red"><div class="card-val">{kpi_taxa_d3plus}<span class="unit">%</span></div><div class="card-label">Fora do SLA (D+3+)</div><div class="card-sub">{kpi_d3plus} pedidos atrasados</div></div>
</div>
<div class="cards" style="margin-top:14px">
  <div class="card c-green"><div class="card-val">{kpi_taxa_d0}<span class="unit">%</span></div><div class="card-label">D+0</div><div class="card-sub">{kpi_d0} pedidos</div></div>
  <div class="card c-green"><div class="card-val">{kpi_taxa_d1}<span class="unit">%</span></div><div class="card-label">D+1</div><div class="card-sub">{kpi_d1} pedidos</div></div>
  <div class="card c-amber"><div class="card-val">{kpi_taxa_d2}<span class="unit">%</span></div><div class="card-label">D+2 (aceitável)</div><div class="card-sub">{kpi_d2} pedidos</div></div>
  <div class="card c-gray"><div class="card-val">{kpi_avg_tentativas}</div><div class="card-label">Tentativas Médias</div></div>
  <div class="card c-gray"><div class="card-val">{kpi_pct_primeira}<span class="unit">%</span></div><div class="card-label">1ª Tentativa</div></div>
  <div class="card c-gray"><div class="card-val">{kpi_pct_agenda}<span class="unit">%</span></div><div class="card-label">Cumpr. de Agenda</div></div>
</div>
<div class="section-title" style="margin-top:32px">Distribuição D+X</div>
<div class="dist-wrap">{dist_bars}</div>
<div class="section-title" style="margin-top:32px">🚚 Performance por Transportador</div>
<div class="tbl-wrap">{tabela_transportadores}</div>
<div class="section-title" style="margin-top:32px">🗺️ Performance por Cidade</div>
<div class="tbl-wrap">{tabela_cidades}</div>
</div>
<div class="ftr">Relatório gerado por <strong>CSS Solutions KPI Skill</strong> · Claude Code &nbsp;·&nbsp; {gerado_em}</div>
<script>
document.querySelectorAll('thead th[data-col]').forEach(th => {{
  th.addEventListener('click', () => {{
    const tbl = th.closest('table');
    const tbody = tbl.querySelector('tbody');
    const idx = +th.dataset.col;
    const asc = th.classList.toggle('sort-asc');
    th.classList.toggle('sort-desc', !asc);
    tbl.querySelectorAll('thead th').forEach(t => {{ if(t!==th){{t.classList.remove('sort-asc','sort-desc')}} }});
    const rows = Array.from(tbody.querySelectorAll('tr'));
    rows.sort((a,b) => {{
      const av = a.cells[idx]?.dataset.val ?? a.cells[idx]?.textContent ?? '';
      const bv = b.cells[idx]?.dataset.val ?? b.cells[idx]?.textContent ?? '';
      const an = parseFloat(av), bn = parseFloat(bv);
      if(!isNaN(an)&&!isNaN(bn)) return asc ? an-bn : bn-an;
      return asc ? av.localeCompare(bv,'pt') : bv.localeCompare(av,'pt');
    }});
    rows.forEach(r => tbody.appendChild(r));
  }});
}});
</script>
</body></html>"""


def _badge(val: float, thresholds=(80, 70)) -> str:
    if val >= thresholds[0]:
        return '<span class="badge badge-green">{:.1f}%</span>'.format(val)
    if val >= thresholds[1]:
        return '<span class="badge badge-amber">{:.1f}%</span>'.format(val)
    return '<span class="badge badge-red">{:.1f}%</span>'.format(val)


def _dx_badge(label: str, val: float) -> str:
    if label in ('D+0', 'D+1'):
        cls = 'badge-green'
    elif label == 'D+2':
        cls = 'badge-amber'
    else:
        cls = 'badge-red'
    return f'<span class="badge {cls}">{val:.1f}%</span>'


def _dist_bar(label: str, pct: float, count: int, color: str) -> str:
    width = min(100, round(pct, 1))
    return (
        f'<div class="dist-row">'
        f'<div class="dist-label">{label}</div>'
        f'<div class="dist-bar-track"><div class="dist-bar-fill {color}" style="width:{width}%"></div></div>'
        f'<div class="dist-pct">{pct:.1f}% <span style="font-size:10px;color:#9CA3AF">({count})</span></div>'
        f'</div>'
    )


def _transporter_table(rows: list[dict]) -> str:
    headers = [
        ('Transportador', 0, False),
        ('Pedidos',       1, True),
        ('% Conclusão',   2, True),
        ('SLA ≤D+2',      3, True),
        ('D+1',           4, True),
        ('D+2',           5, True),
        ('D+3+',          6, True),
        ('Tent. Média',   7, True),
        ('1ª Tent.',      8, True),
        ('Dist. Média km',9, True),
    ]
    ths = ''.join(
        f'<th data-col="{i}">{h}</th>' if sortable else f'<th>{h}</th>'
        for h, i, sortable in headers
    )
    trs = []
    for r in rows:
        trs.append(
            f'<tr>'
            f'<td>{r["nome"]}</td>'
            f'<td class="num" data-val="{r["total"]}">{r["total"]}</td>'
            f'<td class="num" data-val="{r["pct_conclusao"]}">{r["pct_conclusao"]:.1f}%</td>'
            f'<td class="num" data-val="{r["pct_sla"]}">{_badge(r["pct_sla"])}</td>'
            f'<td class="num" data-val="{r["pct_d1"]}">{_dx_badge("D+1", r["pct_d1"])}</td>'
            f'<td class="num" data-val="{r["pct_d2"]}">{_dx_badge("D+2", r["pct_d2"])}</td>'
            f'<td class="num" data-val="{r["pct_d3plus"]}">{_dx_badge("D+3+", r["pct_d3plus"])}</td>'
            f'<td class="num" data-val="{r["avg_tentativas"]}">{r["avg_tentativas"]:.2f}</td>'
            f'<td class="num" data-val="{r["pct_primeira"]}">{r["pct_primeira"]:.1f}%</td>'
            f'<td class="num" data-val="{r["avg_dist_km"]}">{r["avg_dist_km"]:.1f} km</td>'
            f'</tr>'
        )
    return f'<table><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'


def _city_table(rows: list[dict]) -> str:
    headers = [
        ('Cidade',      0, False),
        ('Pedidos',     1, True),
        ('SLA ≤D+2',    2, True),
        ('D+1',         3, True),
        ('Tent. Média', 4, True),
    ]
    ths = ''.join(
        f'<th data-col="{i}">{h}</th>' if sortable else f'<th>{h}</th>'
        for h, i, sortable in headers
    )
    trs = []
    for r in rows:
        trs.append(
            f'<tr>'
            f'<td>{r["cidade"].title()}</td>'
            f'<td class="num" data-val="{r["total"]}">{r["total"]}</td>'
            f'<td class="num" data-val="{r["pct_sla"]}">{_badge(r["pct_sla"])}</td>'
            f'<td class="num" data-val="{r["pct_d1"]}">{_dx_badge("D+1", r["pct_d1"])}</td>'
            f'<td class="num" data-val="{r["avg_tentativas"]}">{r["avg_tentativas"]:.2f}</td>'
            f'</tr>'
        )
    return f'<table><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table>'


def render_html(kpis: dict, t_rows: list[dict], c_rows: list[dict],
                periodo: str, gerado_em: str) -> str:
    sla = kpis['taxa_sla']
    sla_class = 'c-green' if sla >= 85 else ('c-amber' if sla >= 70 else 'c-red')
    dist_bars = (
        _dist_bar('D+0',  kpis['taxa_d0'],    kpis['d0'],     'green') +
        _dist_bar('D+1',  kpis['taxa_d1'],    kpis['d1'],     'green') +
        _dist_bar('D+2',  kpis['taxa_d2'],    kpis['d2'],     'amber') +
        _dist_bar('D+3+', kpis['taxa_d3plus'],kpis['d3plus'], 'red')
    )
    return HTML_TEMPLATE.format(
        logo_b64            = LOGO_B64,
        periodo             = periodo,
        gerado_em           = gerado_em,
        kpi_total           = f"{kpis['total']:,}".replace(',', '.'),
        kpi_taxa_entrega    = kpis['taxa_entrega'],
        kpi_n_concluded     = kpis['n_concluded'],
        kpi_taxa_sla        = kpis['taxa_sla'],
        kpi_sla_ok          = kpis['sla_ok'],
        sla_card_class      = sla_class,
        kpi_taxa_d3plus     = kpis['taxa_d3plus'],
        kpi_d3plus          = kpis['d3plus'],
        kpi_taxa_d0         = kpis['taxa_d0'],
        kpi_d0              = kpis['d0'],
        kpi_taxa_d1         = kpis['taxa_d1'],
        kpi_d1              = kpis['d1'],
        kpi_taxa_d2         = kpis['taxa_d2'],
        kpi_d2              = kpis['d2'],
        kpi_avg_tentativas  = kpis['avg_tentativas'],
        kpi_pct_primeira    = kpis['pct_primeira'],
        kpi_pct_agenda      = kpis['pct_agenda'],
        dist_bars           = dist_bars,
        tabela_transportadores = _transporter_table(t_rows),
        tabela_cidades      = _city_table(c_rows),
    )


def main():
    parser = argparse.ArgumentParser(description='Gera relatório HTML de KPIs de entrega de chips.')
    parser.add_argument('xlsx', help='Caminho do arquivo pedidos.xlsx')
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx).expanduser().resolve()
    if not xlsx_path.exists():
        print(f'[ERRO] Arquivo não encontrado: {xlsx_path}', file=sys.stderr)
        sys.exit(1)

    print(f'Carregando dados de {xlsx_path.name}...')
    df = load_data(str(xlsx_path))
    print(f'  {len(df)} pedidos carregados.')

    print('Calculando KPIs...')
    kpis = calc_kpis(df)
    cwd  = kpis.pop('_concluded_with_dx')
    t_rows = calc_transporter_kpis(df, cwd)
    c_rows = calc_city_kpis(df, cwd)

    col_criado = _col(df, 'Criado em')
    datas = df[col_criado].dropna().apply(parse_dt).dropna()
    periodo = (
        f"{datas.min().strftime('%d/%m/%Y')} – {datas.max().strftime('%d/%m/%Y')}"
        if len(datas) else '—'
    )
    gerado_em = datetime.now().strftime('%d/%m/%Y %H:%M')

    print('Gerando HTML...')
    html = render_html(kpis, t_rows, c_rows, periodo, gerado_em)

    out_name = f"relatorio_kpis_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    out_path = xlsx_path.parent / out_name
    out_path.write_text(html, encoding='utf-8')
    print(f'Relatório salvo em: {out_path}')

    try:
        subprocess.Popen(['start', '', str(out_path)], shell=True)
    except Exception:
        pass

    return str(out_path)


if __name__ == '__main__':
    main()
