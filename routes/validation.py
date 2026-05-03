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
        validation_id = add_validation_issue(form_data)
        
        if request.headers.get("HX-Request"):
            validation_issues = get_validation_issues()
            new_issue = validation_issues[-1] if validation_issues else None
            if new_issue:
                return render_template_string(
                    """<tr id="validation-temp-{{validation_id}}"><td><b>{{i.title}}</b><br><span class="muted">{{i.description}}</span></td><td>{{client}}<br>{{project}}</td><td>{{i.source}}<br><span class="muted">{{i.table_name}}</span></td><td>{{i.expected_data}}</td><td>{{i.actual_data}}</td><td><span class="badge {{ badge_class(i.severity) }}">{{i.severity}}</span></td><td><span class="badge {{ badge_class(i.status) }}">{{i.status}}</span></td><td>{{i.owner}}</td></tr>""",
                    i=new_issue, client=client_name, project=project_name, validation_id=validation_id, badge_class=badge_class,
                )
            return ""
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
<button class="btn secondary" onclick="toggleForm('validation-form', 'add-validation-btn')" id="add-validation-btn">+ Add Validation Issue</button>
<div id="validation-form" class="card form-section" style="display:none"><div class="section-title">Add Validation Issue</div>
<form class="form-grid" hx-post="{{ url_for('validation.validation_page') }}" hx-target="#validation-table" hx-swap="beforeend" hx-on::before-request="optimisticAddValidation(event)">
<input name="title" placeholder="Issue Title" required>
<input name="client" placeholder="Client">
<input name="project" placeholder="Project">
<input name="source" placeholder="Data Source">
<input name="table_name" placeholder="Table / Report / API Name">
<input name="expected_data" placeholder="Expected Data">
<input name="actual_data" placeholder="Actual Data">
<input name="severity" placeholder="Severity">
<input name="owner" placeholder="Owner">
<input name="status" placeholder="Status">
<input name="identified_date" placeholder="Date Identified">
<textarea name="description" placeholder="Issue Description"></textarea>
<textarea name="notes" placeholder="Resolution Notes"></textarea>
<button class="wide">Add Issue</button>
</form>
</div>
<div class="card"><table id="validation-table"><thead><tr><th>Issue</th><th>Client/Project</th><th>Source</th><th>Expected</th><th>Actual</th><th>Severity</th><th>Status</th><th>Owner</th></tr></thead><tbody>{% for i in validation_issues %}<tr id="validation-{{i.id}}"><td><b>{{i.title}}</b><br><span class="muted">{{i.description}}</span></td><td>{{i.client}}<br>{{i.project}}</td><td>{{i.source}}<br><span class="muted">{{i.table_name}}</span></td><td>{{i.expected_data}}</td><td>{{i.actual_data}}</td><td><span class="badge {{ badge_class(i.severity) }}">{{i.severity}}</span></td><td><span class="badge {{ badge_class(i.status) }}">{{i.status}}</span></td><td>{{i.owner}}</td></tr>{% endfor %}</tbody></table></div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddValidation(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const title = formData.get('title') || 'New Issue';
    const client = formData.get('client') || '-';
    const project = formData.get('project') || '-';
    const source = formData.get('source') || '-';
    const table_name = formData.get('table_name') || '';
    const expected_data = formData.get('expected_data') || '-';
    const actual_data = formData.get('actual_data') || '-';
    const severity = formData.get('severity') || '-';
    const owner = formData.get('owner') || '-';
    const status = formData.get('status') || '-';
    const description = formData.get('description') || '';
    const id = Date.now();
    const row = document.createElement('tr');
    row.id = 'validation-' + id;
    row.innerHTML = '<td><b>' + title + '</b><br><span class="muted">' + description + '</span></td><td>' + client + '<br>' + project + '</td><td>' + source + '<br><span class="muted">' + table_name + '</span></td><td>' + expected_data + '</td><td>' + actual_data + '</td><td><span class="badge neutral">' + severity + '</span></td><td><span class="badge neutral">' + status + '</span></td><td>' + owner + '</td>';
    row.style.opacity = '0.5';
    document.getElementById('validation-table').querySelector('tbody').appendChild(row);
    form.reset();
    toggleForm('validation-form', 'add-validation-btn');
}
</script>""",
        validation_issues=validation_issues, badge_class=badge_class,
    )
    return page(content)