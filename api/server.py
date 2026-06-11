# api/server.py
"""
Lightweight Flask API consumed by the React dashboard.

Endpoints
---------
GET /api/streaks              → all active streaks across all leagues
GET /api/streaks?league=PL    → streaks filtered to one league code
GET /api/leagues              → list of configured leagues with their codes
GET /api/health               → health-check

Run locally:
    pip install flask flask-cors
    python -m api.server
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from app.analytics.dashboard_service import DashboardService
from app.config.leagues import LEAGUES

app = Flask(__name__)
CORS(app)  # Allow the React dev-server (port 3000) to call this API

@app.route("/")
def home():
    return {
        "service": "Football Streaks API",
        "status": "running",
        "endpoints": [
            "/api/health",
            "/api/leagues",
            "/api/streaks"
        ]
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _streak_to_dict(s) -> dict:
    return {
        "league":               s.league,
        "team":                 s.team,
        "team_id":              s.team_id,
        "crest_url":            s.crest_url,
        "streak_type":          s.streak_type,        # "win" | "draw" | "loss"
        "streak_length":        s.streak_length,
        "last_opponent":        s.last_opponent,
        "last_opponent_crest":  s.last_opponent_crest,
        "match_date":           s.match_date,
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/leagues")
def leagues():
    data = [
        {"name": name, "code": code}
        for name, code in LEAGUES.items()
    ]
    return jsonify(data)


@app.route("/api/streaks")
def streaks():
    league_filter = request.args.get("league")   # optional ?league=PL

    try:
        all_streaks = DashboardService.get_all_streaks()
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    if league_filter:
        # Match on either the short code or the full league name
        all_streaks = [
            s for s in all_streaks
            if s.league == league_filter
            or LEAGUES.get(s.league) == league_filter
        ]

    return jsonify([_streak_to_dict(s) for s in all_streaks])


# ---------------------------------------------------------------------------
# Dev entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
