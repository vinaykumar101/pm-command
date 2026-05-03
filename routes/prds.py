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
        prd_id = add_prd(form_data)
        
        if request.headers.get("HX-Request"):
            prds = get_prds()
            new_prd = prds[-1] if prds else None
            if new_prd:
                return render_template_string(
                    """<div class="card" id="prd-temp-{{prd_id}}"><h3>{{p.title}}</h3><p class="muted">{{client}} &bull; {{project}}</p><p>{{p.objective}}</p><span class="badge {{ badge_class(p.status) }}">{{p.status}}</span></div>""",
                    p=new_prd, client=client_name, project=project_name, prd_id=prd_id, badge_class=badge_class,
                )
            return ""
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
<button class="btn secondary" onclick="toggleForm('prd-form', 'add-prd-btn')" id="add-prd-btn">+ Create PRD</button>
<div id="prd-form" class="card form-section" style="display:none"><div class="section-title">Create PRD</div>
<form class="form-grid" hx-post="{{ url_for('prds.prds_page') }}" hx-target="#prds-grid" hx-swap="beforeend" hx-on::before-request="optimisticAddPRD(event)">
    <input name="title" placeholder="PRD Title" required>
    <input name="client" placeholder="Client Name">
    <input name="project" placeholder="Project Name">
    <input name="status" placeholder="PRD Status">
    <textarea name="background" placeholder="Background"></textarea>
    <textarea name="problem" placeholder="Problem Statement"></textarea>
    <textarea name="objective" placeholder="Objective"></textarea>
    <textarea name="users" placeholder="Target Users"></textarea>
    <textarea name="solution" placeholder="Proposed Solution"></textarea>
    <textarea name="functional_req" placeholder="Functional Requirements"></textarea>
    <textarea name="acceptance_criteria" placeholder="Acceptance Criteria"></textarea>
    <div class="wide actions"><button class="wide">Save PRD</button></div>
</form>
</div>
<div class="grid two" id="prds-grid">{% for p in prds %}<div class="card" id="prd-{{p.id}}"><h3>{{p.title}}</h3><p class="muted">{{p.client}} &bull; {{p.project}}</p><p>{{p.objective}}</p><span class="badge {{ badge_class(p.status) }}">{{p.status}}</span></div>{% endfor %}</div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddPRD(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const title = formData.get('title') || 'New PRD';
    const client = formData.get('client') || 'Unknown';
    const project = formData.get('project') || 'Unknown';
    const status = formData.get('status') || '-';
    const objective = formData.get('objective') || '';
    const id = Date.now();
    const card = document.createElement('div');
    card.className = 'card';
    card.id = 'prd-' + id;
    card.style.opacity = '0.5';
    card.innerHTML = '<h3>' + title + '</h3><p class="muted">' + client + ' &bull; ' + project + '</p><p>' + objective + '</p><span class="badge neutral">' + status + '</span>';
    document.getElementById('prds-grid').appendChild(card);
    form.reset();
    toggleForm('prd-form', 'add-prd-btn');
}
</script>""",
        prds=prds, badge_class=badge_class,
    )
    return page(content)