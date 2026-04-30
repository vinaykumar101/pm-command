from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_releases, get_clients, get_projects, add_release
from routes.layout import page
from utils.helpers import badge_class

releases_bp = Blueprint("releases", __name__, url_prefix="/releases")


@releases_bp.route("", methods=["GET", "POST"])
def releases_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "name", "version", "release_date", "release_type",
            "features", "bugs_fixed", "known_issues", "deployment_status", "uat_status", "approval_status", "notes"
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
        add_release(form_data)
        return redirect(url_for("releases.releases_page"))

    releases = get_releases()
    clients = get_clients()
    projects = get_projects()
    client_map = {c["id"]: c["name"] for c in clients}
    project_map = {p["id"]: p["name"] for p in projects}
    for r in releases:
        r["client"] = client_map.get(r.get("client_id"), "Unknown")
        r["project"] = project_map.get(r.get("project_id"), "Unknown")
    content = render_template_string(
        """<h1>Releases</h1><p class="subtitle">Track release readiness, UAT status and deployment notes.</p>
<div class="card form-section"><div class="section-title">Add Release</div><form method="post" class="form-grid">{% for k,label in [('name','Release Name'),('version','Version Number'),('client','Client'),('project','Project'),('release_date','Release Date'),('release_type','Release Type'),('deployment_status','Deployment Status'),('uat_status','UAT Status'),('approval_status','Approval Status')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="features" placeholder="Features Included"></textarea><textarea name="bugs_fixed" placeholder="Bugs Fixed"></textarea><textarea name="known_issues" placeholder="Known Issues"></textarea><textarea name="notes" placeholder="Release Notes"></textarea><button>Add Release</button></form></div>
<div class="card"><table><tr><th>Release</th><th>Client/Project</th><th>Date</th><th>Type</th><th>Deployment</th><th>UAT</th><th>Approval</th></tr>{% for r in releases %}<tr><td><b>{{r.name}}</b><br><span class="muted">{{r.version}}</span></td><td>{{r.client}}<br>{{r.project}}</td><td>{{r.release_date}}</td><td>{{r.release_type}}</td><td><span class="badge {{ badge_class(r.deployment_status) }}">{{r.deployment_status}}</span></td><td><span class="badge {{ badge_class(r.uat_status) }}">{{r.uat_status}}</span></td><td><span class="badge {{ badge_class(r.approval_status) }}">{{r.approval_status}}</span></td></tr>{% endfor %}</table></div>""",
        releases=releases, badge_class=badge_class,
    )
    return page(content)