from __future__ import annotations

import importlib.util
import os
import sys
from datetime import datetime
from pathlib import Path


def load_index_module():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "00_generate_index.py"
    spec = importlib.util.spec_from_file_location("generate_index", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def touch(path: Path, timestamp: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("placeholder", encoding="utf-8")
    os.utime(path, (timestamp, timestamp))


def test_build_index_html_lists_all_output_sections(tmp_path: Path) -> None:
    module = load_index_module()
    output_dir = tmp_path / "output"
    touch(output_dir / "dashboards" / "yield_curve_dashboard.html", 1_717_171_200)
    touch(output_dir / "excel" / "capital_markets_master.xlsx", 1_717_171_200)
    touch(output_dir / "pdf" / "jpm_sovereign_risk_report.pdf", 1_717_171_200)
    touch(output_dir / "memos" / "gs_gir_weekly_snapshot.txt", 1_717_171_200)

    html = module.build_index_html(
        output_dir,
        generated_at=datetime(2026, 7, 9, 10, 30),
    )

    assert "Capital Markets Intelligence Output Index" in html
    assert "Dashboards" in html
    assert "Excel Workbooks" in html
    assert "PDF Reports" in html
    assert "Research Memos" in html
    assert 'href="dashboards/yield_curve_dashboard.html"' in html
    assert 'href="excel/capital_markets_master.xlsx"' in html
    assert 'href="pdf/jpm_sovereign_risk_report.pdf"' in html
    assert 'href="memos/gs_gir_weekly_snapshot.txt"' in html
    assert datetime.fromtimestamp(1_717_171_200).strftime("%Y-%m-%d") in html


def test_write_index_creates_output_index_file(tmp_path: Path) -> None:
    module = load_index_module()
    output_dir = tmp_path / "output"
    touch(output_dir / "dashboards" / "ipo_analysis_dashboard.html", 1_717_171_200)

    index_path = module.write_index(output_dir, generated_at=datetime(2026, 7, 9, 10, 30))

    assert index_path == output_dir / "index.html"
    assert index_path.exists()
    assert 'href="dashboards/ipo_analysis_dashboard.html"' in index_path.read_text(
        encoding="utf-8"
    )
