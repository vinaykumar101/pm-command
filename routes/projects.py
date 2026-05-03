from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_projects, get_clients, add_project
from routes.layout import page
from utils.helpers import badge_class

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")


@projects_bp.route("", methods=["GET", "POST"])
def projects_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "name", "type", "problem", "objective", "users",
            "metrics", "owner", "tech_owner", "qa_owner", "start_date", "release_date", "status", "priority", "risk"
        ]}
        client_name = request.form.get("client", "").strip()
        clients = get_clients()
        for c in clients:
            if c["name"] == client_name:
                form_data["client_id"] = c["id"]
                break
        project_id = add_project(form_data)
        
        if request.headers.get("HX-Request"):
            projects = get_projects()
            new_project = projects[-1] if projects else None
            if new_project:
                return render_template_string(
                    """<tr id="project-temp-{{project_id}}"><td><b>{{p.name}}</b><br><span class="muted">{{p.problem}}</span></td><td>{{client}}</td><td>{{p.type}}</td><td>{{p.owner}}</td><td><span class="badge {{ badge_class(p.status) }}">{{p.status}}</span></td><td><span class="badge {{ badge_class(p.priority) }}">{{p.priority}}</span></td><td><span class="badge {{ badge_class(p.risk) }}">{{p.risk}}</span></td><td>{{p.release_date}}</td></tr>""",
                    p=new_project, client=client_name, project_id=project_id, badge_class=badge_class,
                )
            return ""
        return redirect(url_for("projects.projects_page"))

    projects = get_projects()
    clients = get_clients()
    client_map = {c["id"]: c["name"] for c in clients}
    for p in projects:
        p["client"] = client_map.get(p.get("client_id"), "Unknown")
    content = render_template_string(
        """<h1>Projects</h1><p class="subtitle">Create projects under clients and track delivery status.</p>
<button class="btn secondary" onclick="toggleForm('project-form', 'add-project-btn')" id="add-project-btn">+ Add Project</button>
<div id="project-form" class="card form-section" style="display:none"><div class="section-title">Add Project</div>
<form class="form-grid" hx-post="{{ url_for('projects.projects_page') }}" hx-target="#projects-table" hx-swap="beforeend" hx-on::before-request="optimisticAddProject(event)">
<input name="name" placeholder="Project Name" required>
<input name="client" placeholder="Client">
<input name="type" placeholder="Project Type">
<input name="owner" placeholder="Project Owner">
<input name="tech_owner" placeholder="Tech Owner">
<input name="qa_owner" placeholder="QA Owner">
<input name="start_date" placeholder="Start Date">
<input name="release_date" placeholder="Target Release Date">
<input name="status" placeholder="Status">
<input name="priority" placeholder="Priority">
<input name="risk" placeholder="Risk Level">
<input name="users" placeholder="Target Users">
<input name="metrics" placeholder="Success Metrics">
<textarea name="problem" placeholder="Problem Statement"></textarea>
<textarea name="objective" placeholder="Business Objective"></textarea>
<button class="wide">Add Project</button>
</form>
</div>
<div class="card"><table id="projects-table"><thead><tr><th>Project</th><th>Client</th><th>Type</th><th>Owner</th><th>Status</th><th>Priority</th><th>Risk</th><th>Release</th></tr></thead><tbody>{% for p in projects %}<tr id="project-{{p.id}}"><td><b>{{p.name}}</b><br><span class="muted">{{p.problem}}</span></td><td>{{p.client}}</td><td>{{p.type}}</td><td>{{p.owner}}</td><td><span class="badge {{ badge_class(p.status) }}">{{p.status}}</span></td><td><span class="badge {{ badge_class(p.priority) }}">{{p.priority}}</span></td><td><span class="badge {{ badge_class(p.risk) }}">{{p.risk}}</span></td><td>{{p.release_date}}</td></tr>{% endfor %}</tbody></table></div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddProject(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const name = formData.get('name') || 'New Project';
    const client = formData.get('client') || '-';
    const type = formData.get('type') || '-';
    const owner = formData.get('owner') || '-';
    const status = formData.get('status') || '-';
    const priority = formData.get('priority') || '-';
    const risk = formData.get('risk') || '-';
    const release_date = formData.get('release_date') || '-';
    const problem = formData.get('problem') || '';
    const id = Date.now();
    const row = document.createElement('tr');
    row.id = 'project-' + id;
    row.innerHTML = '<td><b>' + name + '</b><br><span class="muted">' + problem + '</span></td><td>' + client + '</td><td>' + type + '</td><td>' + owner + '</td><td><span class="badge neutral">' + status + '</span></td><td><span class="badge neutral">' + priority + '</span></td><td><span class="badge neutral">' + risk + '</span></td><td>' + release_date + '</td>';
    row.style.opacity = '0.5';
    document.getElementById('projects-table').querySelector('tbody').appendChild(row);
    form.reset();
    toggleForm('project-form', 'add-project-btn');
}
</script>""",
        projects=projects, badge_class=badge_class,
    )
    return page(content)