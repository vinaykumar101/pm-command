from flask import Flask, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from utils.helpers import badge_class
from routes.layout import page as render_page, NAV, ROLES
from routes.dashboard import dashboard_bp
from routes.clients import clients_bp
from routes.projects import projects_bp
from routes.requirements import requirements_bp
from routes.prds import prds_bp
from routes.tasks import tasks_bp
from routes.funnel import funnel_bp
from routes.cohort import cohort_bp
from routes.metrics import metrics_bp
from routes.validation import validation_bp
from routes.uat import uat_bp
from routes.bugs import bugs_bp
from routes.releases import releases_bp
from routes.meetings import meetings_bp
from routes.reports import reports_bp
from routes.settings import settings_bp


app = Flask(__name__)
app.secret_key = "pm-command-center-demo-key"
CORS(app)

app.jinja_env.globals["badge_class"] = badge_class
app.jinja_env.globals["NAV"] = NAV


@app.context_processor
def inject_helpers():
    return dict(badge_class=badge_class, role=session.get("role", "Product Manager"))


@app.route("/set-role", methods=["POST"])
def set_role():
    session["role"] = request.form.get("role", "Product Manager")
    return redirect(request.referrer or url_for("dashboard.dashboard"))


app.register_blueprint(dashboard_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(requirements_bp)
app.register_blueprint(prds_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(funnel_bp)
app.register_blueprint(cohort_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(validation_bp)
app.register_blueprint(uat_bp)
app.register_blueprint(bugs_bp)
app.register_blueprint(releases_bp)
app.register_blueprint(meetings_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(settings_bp)


@app.route("/api/dashboard")
def api_dashboard():
    from data.store import (get_clients, get_projects, get_prds, get_tasks, get_bugs,
                            get_uat_cases, get_releases, get_validation_issues, get_funnel)
    from services.dashboard import dashboard_stats

    clients = get_clients()
    projects = get_projects()
    prds = get_prds()
    tasks = get_tasks()
    bugs = get_bugs()
    uat_cases = get_uat_cases()
    releases = get_releases()
    validation_issues = get_validation_issues()
    funnel = get_funnel()

    stats = dashboard_stats(clients, projects, prds, tasks, bugs, uat_cases, releases, validation_issues, funnel)

    return jsonify({
        "cards": stats["cards"],
        "project_counts": stats["project_counts"],
        "task_counts": stats["task_counts"],
        "bug_counts": stats["bug_counts"],
        "funnel": [{"name": name, "count": num} for name, num in funnel],
        "recent_activity": [
            {"activity": "AgriPulse UAT build shared", "status": "Pending Acceptance", "date": "2026-04-17"},
            {"activity": "DigiAcre RBAC development started", "status": "In Progress", "date": "2026-04-20"},
            {"activity": "Dashboard count mismatch logged", "status": "Open", "date": "2026-04-22"},
        ]
    })


@app.route("/api/clients", methods=["GET", "POST"])
def api_clients():
    from data.store import get_clients, add_client
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "name", "industry", "contact", "email", "phone",
            "type", "priority", "engagement", "contract", "start_date", "notes"
        ]}
        client_id = add_client(form_data)
        return jsonify({"id": client_id, "success": True})
    clients = get_clients()
    return jsonify(clients)


@app.route("/api/projects", methods=["GET", "POST"])
def api_projects():
    from data.store import get_projects, get_clients, add_project
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "name", "type", "problem", "objective", "users",
            "metrics", "owner", "tech_owner", "qa_owner", "start_date", "release_date", "status", "priority", "risk"
        ]}
        client_name = request.json.get("client", "").strip() if request.json.get("client") else ""
        clients = get_clients()
        for c in clients:
            if c["name"] == client_name:
                form_data["client_id"] = c["id"]
                break
        project_id = add_project(form_data)
        return jsonify({"id": project_id, "success": True})
    projects = get_projects()
    clients = get_clients()
    client_map = {c["id"]: c["name"] for c in clients}
    for p in projects:
        p["client"] = client_map.get(p.get("client_id"), "Unknown")
    return jsonify(projects)


@app.route("/api/tasks", methods=["GET", "POST"])
def api_tasks():
    from data.store import get_tasks, get_projects, get_prds, add_task
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "title", "type", "description", "acceptance_criteria", "assigned_to", "priority", "status", "sprint", "due_date", "estimate", "actual_effort"
        ]}
        project_name = request.json.get("project", "").strip() if request.json.get("project") else ""
        prd_title = request.json.get("prd", "").strip() if request.json.get("prd") else ""
        projects = get_projects()
        prds_data = get_prds()
        for p in projects:
            if p["name"] == project_name:
                form_data["project_id"] = p["id"]
                form_data["client_id"] = p.get("client_id")
                break
        for p in prds_data:
            if p["title"] == prd_title:
                form_data["prd_id"] = p["id"]
                break
        task_id = add_task(form_data)
        return jsonify({"id": task_id, "success": True})
    tasks = get_tasks()
    projects = get_projects()
    project_map = {p["id"]: p["name"] for p in projects}
    for t in tasks:
        t["project"] = project_map.get(t.get("project_id"), "Unknown")
    return jsonify(tasks)


@app.route("/api/bugs", methods=["GET", "POST"])
def api_bugs():
    from data.store import get_bugs, add_bug
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "title", "severity", "status", "priority", "assigned_to", "reported_by", "module", "description", "steps_to_reproduce"
        ]}
        bug_id = add_bug(form_data)
        return jsonify({"id": bug_id, "success": True})
    bugs = get_bugs()
    return jsonify(bugs)


@app.route("/api/prds", methods=["GET", "POST"])
def api_prds():
    from data.store import get_prds, add_prd
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "title", "version", "status", "owner", "client", "problem", "objective", "target_users", "success_metrics", "timeline", "budget"
        ]}
        prd_id = add_prd(form_data)
        return jsonify({"id": prd_id, "success": True})
    prds = get_prds()
    return jsonify(prds)


@app.route("/api/requirements", methods=["GET", "POST"])
def api_requirements():
    from data.store import get_requirements, add_requirement
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "title", "module", "type", "status", "priority", "assigned_to", "description"
        ]}
        req_id = add_requirement(form_data)
        return jsonify({"id": req_id, "success": True})
    requirements = get_requirements()
    return jsonify(requirements)


@app.route("/api/releases", methods=["GET", "POST"])
def api_releases():
    from data.store import get_releases, add_release
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "name", "version", "status", "release_type", "deployment", "deployment_status", "environment", "release_date", "description"
        ]}
        release_id = add_release(form_data)
        return jsonify({"id": release_id, "success": True})
    releases = get_releases()
    return jsonify(releases)


@app.route("/api/uat", methods=["GET", "POST"])
def api_uat():
    from data.store import get_uat_cases, add_uat_case
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "title", "module", "status", "assigned_to", "test_steps", "expected_result", "actual_result"
        ]}
        uat_id = add_uat_case(form_data)
        return jsonify({"id": uat_id, "success": True})
    uat_cases = get_uat_cases()
    return jsonify(uat_cases)


@app.route("/api/validation", methods=["GET", "POST"])
def api_validation():
    from data.store import get_validation_issues, add_validation_issue
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "title", "entity_type", "entity_id", "issue_type", "severity", "description", "status"
        ]}
        issue_id = add_validation_issue(form_data)
        return jsonify({"id": issue_id, "success": True})
    issues = get_validation_issues()
    return jsonify(issues)


@app.route("/api/funnel", methods=["GET"])
def api_funnel():
    from data.store import get_funnel
    funnel = get_funnel()
    return jsonify([{"name": name, "count": count} for name, count in funnel])


@app.route("/api/cohort", methods=["GET"])
def api_cohort():
    from data.store import get_cohorts
    cohorts = get_cohorts()
    return jsonify(cohorts)


@app.route("/api/metrics", methods=["GET"])
def api_metrics():
    from data.store import get_metrics
    metrics = get_metrics()
    return jsonify(metrics)


@app.route("/api/meetings", methods=["GET", "POST"])
def api_meetings():
    from data.store import get_meetings, add_meeting
    if request.method == "POST":
        form_data = {k: request.json.get(k, "").strip() if request.json.get(k) else "" for k in [
            "title", "date", "time", "attendees", "agenda", "notes", "action_items"
        ]}
        meeting_id = add_meeting(form_data)
        return jsonify({"id": meeting_id, "success": True})
    meetings = get_meetings()
    return jsonify(meetings)


@app.route("/api/reports", methods=["GET"])
def api_reports():
    from data.store import get_reports
    reports = get_reports()
    return jsonify(reports)


@app.route("/api/clients/<int:client_id>", methods=["DELETE"])
def api_delete_client(client_id):
    return jsonify({"success": True})


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def api_delete_project(project_id):
    return jsonify({"success": True})


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    return jsonify({"success": True})


@app.route("/api/bugs/<int:bug_id>", methods=["DELETE"])
def api_delete_bug(bug_id):
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
