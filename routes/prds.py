from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_prds, get_clients, get_projects, add_prd
from routes.layout import page
from utils.helpers import badge_class

prds_bp = Blueprint("prds", __name__, url_prefix="/prds")

PRD_KEYS = [
    "title", "background", "problem", "objective", "users", "personas", "current_process", "solution", "journey", "functional_req", "nonfunctional_req",
    "rbac", "api_req", "data_req", "edge_cases", "acceptance_criteria", "dependencies", "risks", "metrics", "outscope", "release_plan", "uat_plan", "questions", "status"
]


def get_prds_data():
    from data.store import get_prds
    return get_prds()


@prds_bp.route("", methods=["GET", "POST"])
def prds_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in PRD_KEYS}
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
        add_prd(form_data)
        return redirect(url_for("prds.prds_page"))

    prds = get_prds()
    clients = get_clients()
    projects = get_projects()
    client_map = {c["id"]: c["name"] for c in clients}
    project_map = {p["id"]: p["name"] for p in projects}
    for p in prds:
        p["client"] = client_map.get(p.get("client_id"), "Unknown")
        p["project"] = project_map.get(p.get("project_id"), "Unknown")
    content = render_template_string(
        """<h1>PRD Builder</h1><p class="subtitle">Create structured Product Requirement Documents.</p>
<div class="card form-section"><div class="section-title">Create PRD</div><form method="post" class="form-grid">
    <input name="title" placeholder="PRD Title"><input name="client" placeholder="Client Name"><input name="project" placeholder="Project Name"><input name="status" placeholder="PRD Status">
    {% for k,label in [('background','Background'),('problem','Problem Statement'),('objective','Objective'),('users','Target Users'),('personas','User Personas'),('current_process','Current Process'),('solution','Proposed Solution'),('journey','User Journey'),('functional_req','Functional Requirements'),('nonfunctional_req','Non-Functional Requirements'),('rbac','Role-Based Access Control'),('api_req','API Requirements'),('data_req','Data Requirements'),('edge_cases','Edge Cases'),('acceptance_criteria','Acceptance Criteria'),('dependencies','Dependencies'),('risks','Risks'),('metrics','Success Metrics'),('outscope','Out of Scope'),('release_plan','Release Plan'),('uat_plan','UAT Plan'),('questions','Open Questions')] %}<textarea name="{{k}}" placeholder="{{label}}"></textarea>{% endfor %}
    <div class="wide actions"><button>Save PRD</button><span class="btn secondary">Export PRD</span><span class="btn light">Generate User Stories</span><span class="btn light">Generate Acceptance Criteria</span></div>
</form></div>
<div class="grid two">{% for p in prds %}<div class="card"><h3>{{p.title}}</h3><p class="muted">{{p.client}} &bull; {{p.project}}</p><p>{{p.objective}}</p><span class="badge {{ badge_class(p.status) }}">{{p.status}}</span></div>{% endfor %}</div>""",
        prds=prds, badge_class=badge_class,
    )
    return page(content)