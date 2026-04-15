# 🚀 Go Auto Engine

<p align="left">
  <img src="https://img.shields.io/badge/Status-Running-green"/>
  <img src="https://img.shields.io/badge/Automation-GitHub_Actions-blue"/>
  <img src="https://img.shields.io/badge/Cost-100%25_Free-orange"/>
  <img src="https://img.shields.io/github/last-commit/nattapongsindhu/go-auto-engine"/>
</p>

A zero-cost CI/CD automation pipeline that fetches real weather data for Los Angeles every 6 hours, runs analysis logic, generates a live SVG chart, and publishes results to a GitHub Pages dashboard — fully automated with no servers, no secrets, and no spend.

---

## 🌐 Live Dashboard

👉 **[nattapongsindhu.github.io/go-auto-engine](https://nattapongsindhu.github.io/go-auto-engine/)**

---

## 📊 Latest Reading

<img src="./graph.svg" width="500"/>

---

## ⚙️ How It Works

```
GitHub Actions (cron: every 6h)
  └── Fetch → Open-Meteo API (LA weather, no key required)
  └── Analyze → Python: status classification + trend detection
  └── Score → Heat index formula (0–100)
  └── Update → temp.csv, data.json, graph.svg, history.txt
  └── Commit → auto-push to main → GitHub Pages redeploys
```

**Stack:** Bash · Python 3 · jq · Chart.js · GitHub Actions · GitHub Pages

---

## 📁 File Structure

| File | Purpose |
|------|---------|
| `.github/workflows/simulate.yml` | Main automation pipeline |
| `data.json` | Latest sensor snapshot |
| `temp.csv` | Historical temperature log |
| `graph.svg` | Auto-generated SVG chart |
| `index.html` | Live dashboard (Chart.js) |
| `history.txt` | Status history (emoji heatmap) |
| `weather.json` | Raw API response |

---

## 🧠 Analysis Logic

| Condition | Status | Score |
|-----------|--------|-------|
| temp > 30°C | 🔴 HOT | high |
| temp > 20°C | 🟡 WARM | medium |
| temp < 5°C | 🔵 COLD | low |
| otherwise | 🟢 OK | normal |

Trend is calculated by comparing current temp against the previous reading (±1.5°C threshold).

---

## 🔒 Security

- No API keys or secrets required
- Uses [Open-Meteo](https://open-meteo.com/) — free, open, no auth
- Workflow only writes to its own repo
- All data committed in plain text (auditable)

---

## 💡 Why This Exists

Built as a portfolio project demonstrating:
- GitHub Actions scheduling and CI/CD principles
- Data pipeline design (fetch → transform → store → visualize)
- Zero-infrastructure automation
- Python scripting inside shell workflows

---

<p align="center">⚡ Built for Portfolio + Automation Engineering</p>
