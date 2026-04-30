from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_requirements, get_clients, get_projects, add_requirement
from routes.layout import page
from utils.helpers import badge_class

requirements_bp = Blueprint("requirements", __name__, url_prefix="/requirements")


@requirements_bp.route("", methods=["GET", "POST"])
def requirements_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "title", "type", "source", "description", "need", "problem", "outcome", "priority", "status", "requested_by", "request_date"
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
        add_requirement(form_data)
        return redirect(url_for("requirements.requirements_page"))

    requirements = get_requirements()
    clients = get_clients()
    projects = get_projects()
    client_map = {c["id"]: c["name"] for c in clients}
    project_map = {p["id"]: p["name"] for p in projects}
    for r in requirements:
        r["client"] = client_map.get(r.get("client_id"), "Unknown")
        r["project"] = project_map.get(r.get("project_id"), "Unknown")
    content = render_template_string(
        """<h1>Requirements</h1><p class="subtitle">Capture raw requirements and convert them into PRDs.</p>
<div class="card form-section"><div class="section-title">Add Requirement</div><form method="post" class="form-grid">{% for k,label in [('title','Requirement Title'),('client','Client'),('project','Project'),('type','Requirement Type'),('source','Source'),('priority','Priority'),('status','Status'),('requested_by','Requested By'),('request_date','Date Requested')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="description" placeholder="Description"></textarea><textarea name="need" placeholder="Business Need"></textarea><textarea name="problem" placeholder="User Problem"></textarea><textarea name="outcome" placeholder="Expected Outcome"></textarea><button>Add Requirement</button></form></div>
<div class="card"><table><tr><th>Requirement</th><th>Client/Project</th><th>Type</th><th>Source</th><th>Priority</th><th>Status</th><th>Actions</th></tr>{% for r in requirements %}<tr><td><b>{{r.title}}</b><br><span class="muted">{{r.description}}</span></td><td>{{r.client}}<br><span class="muted">{{r.project}}</span></td><td>{{r.type}}</td><td>{{r.source}}</td><td><span class="badge {{ badge_class(r.priority) }}">{{r.priority}}</span></td><td><span class="badge {{ badge_class(r.status) }}">{{r.status}}</span></td><td><div class="actions"><span class="btn light">Approve</span><span class="btn light">Reject</span><span class="btn light">Convert to PRD</span></div></td></tr>{% endfor %}</table></div>""",
        requirements=requirements, badge_class=badge_class,
    )
    return page(content)