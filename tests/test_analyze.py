"""
tests/test_analyze.py
Unit tests for scripts/analyze.py
Run: python3 -m pytest tests/ -v
"""
import sys, os, tempfile, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from analyze import classify_status, detect_trend, detect_anomaly, heat_index_score


# --- classify_status ---

def test_status_hot():
    assert classify_status(31.0) == "HOT"

def test_status_warm():
    assert classify_status(25.0) == "WARM"

def test_status_ok():
    assert classify_status(15.0) == "OK"

def test_status_cold():
    assert classify_status(3.0) == "COLD"

def test_status_boundary_warm():
    assert classify_status(20.1) == "WARM"

def test_status_boundary_ok():
    assert classify_status(20.0) == "OK"


# --- detect_trend ---

def _make_csv(rows: list) -> str:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
    writer = csv.writer(f)
    writer.writerow(["timestamp", "temperature", "wind"])
    for r in rows:
        writer.writerow(r)
    f.close()
    return f.name

def test_trend_rising():
    path = _make_csv([["2026-01-01T00:00", "10.0", "5"]])
    assert detect_trend(12.0, path) == "Rising"
    os.unlink(path)

def test_trend_falling():
    path = _make_csv([["2026-01-01T00:00", "15.0", "5"]])
    assert detect_trend(12.0, path) == "Falling"
    os.unlink(path)

def test_trend_stable():
    path = _make_csv([["2026-01-01T00:00", "13.0", "5"]])
    assert detect_trend(13.5, path) == "Stable"
    os.unlink(path)

def test_trend_no_csv():
    assert detect_trend(13.0, "/nonexistent/path.csv") == "Stable"


# --- detect_anomaly ---

def test_no_anomaly_normal():
    rows = [["2026-01-01T00:00", str(13.0 + i * 0.1), "5"] for i in range(15)]
    path = _make_csv(rows)
    result = detect_anomaly(13.5, path)
    assert result == ""
    os.unlink(path)

def test_anomaly_detected():
    rows = [["2026-01-01T00:00", "13.0", "5"] for _ in range(15)]
    path = _make_csv(rows)
    # 13.0 avg, SD≈0, but force SD > 0 by adding one outlier in history
    rows2 = [["2026-01-01T00:00", str(10.0 + i), "5"] for i in range(15)]
    path2 = _make_csv(rows2)
    result = detect_anomaly(30.0, path2)
    assert result == "ANOMALY"
    os.unlink(path)
    os.unlink(path2)

def test_anomaly_insufficient_data():
    rows = [["2026-01-01T00:00", "13.0", "5"] for _ in range(5)]
    path = _make_csv(rows)
    result = detect_anomaly(99.0, path)
    assert result == ""  # not enough data
    os.unlink(path)


# --- heat_index_score ---

def test_score_normal():
    assert heat_index_score(13.0, 5.0) == 28

def test_score_max():
    assert heat_index_score(100.0, 100.0) == 100

def test_score_min():
    assert heat_index_score(-10.0, 0.0) == 0

def test_score_formula():
    assert heat_index_score(20.0, 10.0) == 45  # 20*2 + 10*0.5 = 45
