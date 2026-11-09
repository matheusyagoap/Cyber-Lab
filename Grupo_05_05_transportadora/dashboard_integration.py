from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from flask import Blueprint, jsonify, render_template, request

def _load_reports(report_dir: Path):
    report_dir = Path(report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    reports = []
    for file in sorted(report_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            data["_file_name"] = file.name
            data["_modified"] = datetime.fromtimestamp(file.stat().st_mtime).isoformat(timespec="seconds")
            reports.append(data)
        except (OSError, json.JSONDecodeError):
            continue
    return reports

def create_local_dashboard(app, report_dir, scenario="00", application="CyberLab"):
    """Registra /dashboard e /dashboard/api/data na aplicação Flask existente."""
    bp = Blueprint(
        "cyberlab_local_dashboard",
        __name__,
        template_folder="templates",
        static_folder="static",
        url_prefix="/dashboard"
    )
    report_dir = Path(report_dir)

    @bp.get("/")
    def dashboard_home():
        return render_template("cyberlab_dashboard.html",
                               mode="local", scenario=scenario, application=application)

    @bp.get("/api/data")
    def dashboard_data():
        reports = _load_reports(report_dir)
        selected = request.args.get("file")
        if selected:
            # Só permite selecionar JSONs que estejam diretamente na pasta autorizada.
            candidate = (report_dir / Path(selected).name)
            reports = [r for r in reports if r.get("_file_name") == candidate.name]
        latest = reports[0] if reports else None
        findings = (latest or {}).get("findings", [])
        counts = {"critico": 0, "alto": 0, "medio": 0, "baixo": 0, "informativo": 0, "outros": 0}
        for item in findings:
            sev = str(item.get("severity", "outros")).lower()
            key = sev if sev in counts else "outros"
            counts[key] += 1
        return jsonify({
            "scenario": scenario, "application": application,
            "reports": [{"file": r.get("_file_name"), "date": r.get("_modified"),
                         "summary": r.get("summary", {})} for r in reports],
            "latest": latest, "severity": counts,
            "history": [{"file": r.get("_file_name"), "date": r.get("_modified"),
                         "indicators": (r.get("summary") or {}).get("indicators",
                             sum(1 for f in r.get("findings", []) if f.get("status") == "indicador_detectado"))}
                        for r in reports]
        })

    app.register_blueprint(bp)
    return bp

def create_professor_dashboard(app, received_dir):
    """Registra painel consolidado em /dashboard e API em /dashboard/api/data."""
    bp = Blueprint(
        "cyberlab_professor_dashboard",
        __name__,
        template_folder="templates",
        static_folder="static",
        url_prefix="/dashboard"
    )
    received_dir = Path(received_dir)

    @bp.get("/")
    def dashboard_home():
        return render_template("cyberlab_dashboard.html",
                               mode="professor", scenario="GERAL",
                               application="Central do Professor")

    @bp.get("/api/data")
    def dashboard_data():
        reports = _load_reports(received_dir)
        teams = []
        totals = {"critico": 0, "alto": 0, "medio": 0, "baixo": 0, "informativo": 0, "outros": 0}
        for report in reports:
            findings = report.get("findings", [])
            counts = dict.fromkeys(totals, 0)
            for item in findings:
                sev = str(item.get("severity", "outros")).lower()
                key = sev if sev in counts else "outros"
                counts[key] += 1
                totals[key] += 1
            meta = report.get("metadata") or {}
            summary = report.get("summary") or {}
            teams.append({
                "scenario": str(meta.get("scenario", "??")),
                "application": meta.get("application", report.get("application", "Aplicação não identificada")),
                "date": report.get("_modified"),
                "file": report.get("_file_name"),
                "checks": summary.get("total_checks", len(findings)),
                "indicators": summary.get("indicators",
                    sum(1 for f in findings if f.get("status") == "indicador_detectado")),
                "severity": counts
            })
        return jsonify({
            "teams": teams, "totals": totals,
            "received": len(teams),
            "pending": max(0, 10 - len({t["scenario"] for t in teams if t["scenario"].isdigit() and 1 <= int(t["scenario"]) <= 10})),
            "indicator_total": sum(t["indicators"] for t in teams)
        })

    app.register_blueprint(bp)
    return bp
