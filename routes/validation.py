from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_validation_issues, get_clients, get_projects, add_validation_issue
from routes.layout import page
from utils.helpers import badge_class

validation_bp = Blueprint("validation", __name__, url_prefix="/validation")


@validation_bp.route("", methods=["GET", "POST"])
def validation_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "title", "source", "table_name", "description", "expected_data", "actual_data",
            "severity", "owner", "status", "identified_date", "notes"
        ]}
        client_name = request.form.get("client", "").strip()
        project_name = request.form.get("project", "").strip()
        clients = get_clients()
        projects = get_projects()
        for c in clients:
            if c["name"] == client_name:
                form_data["client_id"] = c["id"]
                break
        for p in projects:
            if p["name"] == project_name:
                form_data["project_id"] = p["id"]
                break
        add_validation_issue(form_data)
        return redirect(url_for("validation.validation_page"))

    validation_issues = get_validation_issues()
    clients = get_clients()
    projects = get_projects()
    client_map = {c["id"]: c["name"] for c in clients}
    project_map = {p["id"]: p["name"] for p in projects}
    for i in validation_issues:
        i["client"] = client_map.get(i.get("client_id"), "Unknown")
        i["project"] = project_map.get(i.get("project_id"), "Unknown")
    content = render_template_string(
        """<h1>Data Validation</h1><p class="subtitle">Track data quality, dashboard mismatches and API/report issues.</p>
<div class="card form-section"><div class="section-title">Add Validation Issue</div><form method="post" class="form-grid">{% for k,label in [('title','Issue Title'),('client','Client'),('project','Project'),('source','Data Source'),('table_name','Table / Report / API Name'),('expected_data','Expected Data'),('actual_data','Actual Data'),('severity','Severity'),('owner','Owner'),('status','Status'),('identified_date','Date Identified')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="description" placeholder="Issue Description"></textarea><textarea name="notes" placeholder="Resolution Notes"></textarea><button>Add Issue</button></form></div>
<div class="card"><table><tr><th>Issue</th><th>Client/Project</th><th>Source</th><th>Expected</th><th>Actual</th><th>Severity</th><th>Status</th><th>Owner</th></tr>{% for i in validation_issues %}<tr><td><b>{{i.title}}</b><br><span class="muted">{{i.description}}</span></td><td>{{i.client}}<br>{{i.project}}</td><td>{{i.source}}<br><span class="muted">{{i.table_name}}</span></td><td>{{i.expected_data}}</td><td>{{i.actual_data}}</td><td><span class="badge {{ badge_class(i.severity) }}">{{i.severity}}</span></td><td><span class="badge {{ badge_class(i.status) }}">{{i.status}}</span></td><td>{{i.owner}}</td></tr>{% endfor %}</table></div>""",
        validation_issues=validation_issues, badge_class=badge_class,
    )
    return page(content)