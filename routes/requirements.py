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
        req_id = add_requirement(form_data)
        
        if request.headers.get("HX-Request"):
            requirements = get_requirements()
            new_req = requirements[-1] if requirements else None
            if new_req:
                return render_template_string(
                    """<tr id="req-temp-{{req_id}}"><td><b>{{r.title}}</b><br><span class="muted">{{r.description}}</span></td><td>{{client}}<br><span class="muted">{{project}}</span></td><td>{{r.type}}</td><td>{{r.source}}</td><td><span class="badge {{ badge_class(r.priority) }}">{{r.priority}}</span></td><td><span class="badge {{ badge_class(r.status) }}">{{r.status}}</span></td><td><div class="actions"><span class="btn light">Approve</span><span class="btn light">Reject</span><span class="btn light">Convert to PRD</span></div></td></tr>""",
                    r=new_req, client=client_name, project=project_name, req_id=req_id, badge_class=badge_class,
                )
            return ""
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
<button class="btn secondary" onclick="toggleForm('req-form', 'add-req-btn')" id="add-req-btn">+ Add Requirement</button>
<div id="req-form" class="card form-section" style="display:none"><div class="section-title">Add Requirement</div>
<form class="form-grid" hx-post="{{ url_for('requirements.requirements_page') }}" hx-target="#req-table" hx-swap="beforeend" hx-on::before-request="optimisticAddReq(event)">
<input name="title" placeholder="Requirement Title" required>
<input name="client" placeholder="Client">
<input name="project" placeholder="Project">
<input name="type" placeholder="Requirement Type">
<input name="source" placeholder="Source">
<input name="priority" placeholder="Priority">
<input name="status" placeholder="Status">
<input name="requested_by" placeholder="Requested By">
<input name="request_date" placeholder="Date Requested">
<textarea name="description" placeholder="Description"></textarea>
<textarea name="need" placeholder="Business Need"></textarea>
<textarea name="problem" placeholder="User Problem"></textarea>
<textarea name="outcome" placeholder="Expected Outcome"></textarea>
<button class="wide">Add Requirement</button>
</form>
</div>
<div class="card"><table id="req-table"><thead><tr><th>Requirement</th><th>Client/Project</th><th>Type</th><th>Source</th><th>Priority</th><th>Status</th><th>Actions</th></tr></thead><tbody>{% for r in requirements %}<tr id="req-{{r.id}}"><td><b>{{r.title}}</b><br><span class="muted">{{r.description}}</span></td><td>{{r.client}}<br><span class="muted">{{r.project}}</span></td><td>{{r.type}}</td><td>{{r.source}}</td><td><span class="badge {{ badge_class(r.priority) }}">{{r.priority}}</span></td><td><span class="badge {{ badge_class(r.status) }}">{{r.status}}</span></td><td><div class="actions"><span class="btn light">Approve</span><span class="btn light">Reject</span><span class="btn light">Convert to PRD</span></div></td></tr>{% endfor %}</tbody></table></div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddReq(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const title = formData.get('title') || 'New Requirement';
    const client = formData.get('client') || '-';
    const project = formData.get('project') || '-';
    const type = formData.get('type') || '-';
    const source = formData.get('source') || '-';
    const priority = formData.get('priority') || '-';
    const status = formData.get('status') || '-';
    const description = formData.get('description') || '';
    const id = Date.now();
    const row = document.createElement('tr');
    row.id = 'req-' + id;
    row.innerHTML = '<td><b>' + title + '</b><br><span class="muted">' + description + '</span></td><td>' + client + '<br><span class="muted">' + project + '</span></td><td>' + type + '</td><td>' + source + '</td><td><span class="badge neutral">' + priority + '</span></td><td><span class="badge neutral">' + status + '</span></td><td><div class="actions"><span class="btn light">Approve</span><span class="btn light">Reject</span><span class="btn light">Convert to PRD</span></div></td>';
    row.style.opacity = '0.5';
    document.getElementById('req-table').querySelector('tbody').appendChild(row);
    form.reset();
    toggleForm('req-form', 'add-req-btn');
}
</script>""",
        requirements=requirements, badge_class=badge_class,
    )
    return page(content)