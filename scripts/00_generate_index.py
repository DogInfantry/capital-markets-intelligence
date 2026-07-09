"""
Generate a unified landing page for locally generated platform outputs.

Run after the dashboard, Excel, PDF, and memo scripts:

    python scripts/00_generate_index.py

Output:
    output/index.html
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OutputSection:
    title: str
    folder: str
    pattern: str
    descriptions: dict[str, str]


SECTIONS = [
    OutputSection(
        title="Dashboards",
        folder="dashboards",
        pattern="*.html",
        descriptions={
            "yield_curve_dashboard.html": "Term structure animation, curve regimes, and slope decomposition.",
            "sovereign_risk_dashboard.html": "Country risk tiers, macro indicators, and stress views.",
            "market_regime_dashboard.html": "Cross-asset risk regime signals and market context.",
            "ipo_analysis_dashboard.html": "IPO event-study performance, pricing, and sector views.",
            "mna_screening_dashboard.html": "M&A screening matrix and completion feature importance.",
        },
    ),
    OutputSection(
        title="Excel Workbooks",
        folder="excel",
        pattern="*.xlsx",
        descriptions={
            "capital_markets_master.xlsx": "Executive workbook spanning IPO, M&A, sovereign, and macro outputs.",
            "ipo_analysis_workbook.xlsx": "IPO database, event study, and underwriter summary tables.",
            "mna_analysis_workbook.xlsx": "Deal database, case studies, and screening model output.",
            "sovereign_risk_workbook.xlsx": "Risk index, macro panel, stress tests, and issuance tracker.",
        },
    ),
    OutputSection(
        title="PDF Reports",
        folder="pdf",
        pattern="*.pdf",
        descriptions={
            "gs_gir_capital_markets_snapshot.pdf": "Capital markets weekly snapshot in a GIR-style format.",
            "jpm_sovereign_risk_report.pdf": "Sovereign risk and issuance report.",
            "de_shaw_ipo_dashboard.pdf": "Quantitative IPO performance dashboard report.",
            "pwc_db_mna_case_studies.pdf": "M&A strategic rationale and case-study report.",
        },
    ),
    OutputSection(
        title="Research Memos",
        folder="memos",
        pattern="*.txt",
        descriptions={
            "gs_gir_weekly_snapshot.txt": "Cross-asset capital markets memo.",
            "jpm_sovereign_risk_model.txt": "Sovereign risk model memo.",
            "de_shaw_ipo_dashboard.txt": "IPO event-study research memo.",
            "pwc_db_mna_case_studies.txt": "M&A strategy and case-study memo.",
        },
    ),
]


def file_timestamp(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def display_name(path: Path) -> str:
    stem = path.stem.replace("_", " ").replace("-", " ")
    return stem.title()


def relative_href(path: Path, output_dir: Path) -> str:
    relative = path.relative_to(output_dir).as_posix()
    return quote(relative, safe="/")


def collect_files(output_dir: Path, section: OutputSection) -> list[Path]:
    directory = output_dir / section.folder
    if not directory.exists():
        return []
    return sorted(directory.glob(section.pattern), key=lambda path: path.name.lower())


def render_section(output_dir: Path, section: OutputSection) -> str:
    files = collect_files(output_dir, section)
    if not files:
        return f"""
        <section>
          <h2>{escape(section.title)}</h2>
          <p class="empty">No generated files found in <code>{escape(section.folder)}/</code>.</p>
        </section>
        """

    rows = []
    for path in files:
        description = section.descriptions.get(path.name, "Generated platform output.")
        rows.append(
            "            <tr>"
            f'<td><a href="{relative_href(path, output_dir)}">{escape(display_name(path))}</a></td>'
            f"<td>{escape(description)}</td>"
            f"<td>{escape(file_timestamp(path))}</td>"
            "</tr>"
        )

    return f"""
        <section>
          <div class="section-heading">
            <h2>{escape(section.title)}</h2>
            <span>{len(files)} files</span>
          </div>
          <table>
            <thead>
              <tr>
                <th>Output</th>
                <th>Description</th>
                <th>Last generated</th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </section>
        """


def build_index_html(output_dir: Path = OUTPUT_DIR, generated_at: datetime | None = None) -> str:
    generated_at = generated_at or datetime.now()
    sections_html = "\n".join(render_section(output_dir, section) for section in SECTIONS)

    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Capital Markets Intelligence Output Index</title>
    <style>
      :root {{
        color-scheme: dark;
        --bg: #0b1118;
        --panel: #111b27;
        --panel-alt: #162334;
        --text: #e6edf3;
        --muted: #9fb0c3;
        --accent: #58a6ff;
        --border: #263648;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        background: var(--bg);
        color: var(--text);
        font-family: Arial, Helvetica, sans-serif;
        line-height: 1.5;
      }}
      main {{
        width: min(1180px, calc(100% - 40px));
        margin: 0 auto;
        padding: 36px 0 48px;
      }}
      header {{
        margin-bottom: 28px;
      }}
      h1 {{
        margin: 0 0 8px;
        font-size: 32px;
        font-weight: 700;
      }}
      .subtitle {{
        margin: 0;
        color: var(--muted);
        max-width: 780px;
      }}
      .generated {{
        margin-top: 12px;
        color: var(--muted);
        font-size: 14px;
      }}
      section {{
        margin-top: 22px;
        padding: 20px;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 8px;
      }}
      .section-heading {{
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: baseline;
        margin-bottom: 14px;
      }}
      h2 {{
        margin: 0;
        font-size: 20px;
      }}
      .section-heading span,
      .empty {{
        color: var(--muted);
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
        overflow: hidden;
      }}
      th, td {{
        padding: 12px 10px;
        border-bottom: 1px solid var(--border);
        text-align: left;
        vertical-align: top;
      }}
      th {{
        background: var(--panel-alt);
        color: var(--muted);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0;
      }}
      tr:last-child td {{
        border-bottom: 0;
      }}
      a {{
        color: var(--accent);
        text-decoration: none;
        font-weight: 700;
      }}
      a:hover {{
        text-decoration: underline;
      }}
      code {{
        color: var(--text);
      }}
      @media (max-width: 720px) {{
        main {{
          width: min(100% - 24px, 1180px);
          padding-top: 24px;
        }}
        h1 {{
          font-size: 26px;
        }}
        th, td {{
          display: block;
          width: 100%;
        }}
        thead {{
          display: none;
        }}
        tr {{
          display: block;
          padding: 8px 0;
          border-bottom: 1px solid var(--border);
        }}
        tr:last-child {{
          border-bottom: 0;
        }}
        td {{
          border-bottom: 0;
          padding: 6px 0;
        }}
      }}
    </style>
  </head>
  <body>
    <main>
      <header>
        <h1>Capital Markets Intelligence Output Index</h1>
        <p class="subtitle">A local landing page for dashboards, Excel workbooks, PDF reports, and research memos generated by the platform pipeline.</p>
        <p class="generated">Index generated: {escape(generated_at.strftime("%Y-%m-%d %H:%M"))}</p>
      </header>
{sections_html}
    </main>
  </body>
</html>
"""
    return "\n".join(line.rstrip() for line in html.splitlines()) + "\n"


def write_index(output_dir: Path = OUTPUT_DIR, generated_at: datetime | None = None) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    index_path = output_dir / "index.html"
    index_path.write_text(build_index_html(output_dir, generated_at), encoding="utf-8")
    return index_path


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    index_path = write_index()
    logger.info("Generated %s", index_path)


if __name__ == "__main__":
    main()
