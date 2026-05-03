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
        release_id = add_release(form_data)
        
        if request.headers.get("HX-Request"):
            releases = get_releases()
            new_release = releases[-1] if releases else None
            if new_release:
                return render_template_string(
                    """<tr id="release-temp-{{release_id}}"><td><b>{{r.name}}</b><br><span class="muted">{{r.version}}</span></td><td>{{client}}<br>{{project}}</td><td>{{r.release_date}}</td><td>{{r.release_type}}</td><td><span class="badge {{ badge_class(r.deployment_status) }}">{{r.deployment_status}}</span></td><td><span class="badge {{ badge_class(r.uat_status) }}">{{r.uat_status}}</span></td><td><span class="badge {{ badge_class(r.approval_status) }}">{{r.approval_status}}</span></td></tr>""",
                    r=new_release, client=client_name, project=project_name, release_id=release_id, badge_class=badge_class,
                )
            return ""
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
<button class="btn secondary" onclick="toggleForm('release-form', 'add-release-btn')" id="add-release-btn">+ Add Release</button>
<div id="release-form" class="card form-section" style="display:none"><div class="section-title">Add Release</div>
<form class="form-grid" hx-post="{{ url_for('releases.releases_page') }}" hx-target="#releases-table" hx-swap="beforeend" hx-on::before-request="optimisticAddRelease(event)">
<input name="name" placeholder="Release Name" required>
<input name="version" placeholder="Version Number">
<input name="client" placeholder="Client">
<input name="project" placeholder="Project">
<input name="release_date" placeholder="Release Date">
<input name="release_type" placeholder="Release Type">
<input name="deployment_status" placeholder="Deployment Status">
<input name="uat_status" placeholder="UAT Status">
<input name="approval_status" placeholder="Approval Status">
<textarea name="features" placeholder="Features Included"></textarea>
<textarea name="bugs_fixed" placeholder="Bugs Fixed"></textarea>
<textarea name="known_issues" placeholder="Known Issues"></textarea>
<textarea name="notes" placeholder="Release Notes"></textarea>
<button class="wide">Add Release</button>
</form>
</div>
<div class="card"><table id="releases-table"><thead><tr><th>Release</th><th>Client/Project</th><th>Date</th><th>Type</th><th>Deployment</th><th>UAT</th><th>Approval</th></tr></thead><tbody>{% for r in releases %}<tr id="release-{{r.id}}"><td><b>{{r.name}}</b><br><span class="muted">{{r.version}}</span></td><td>{{r.client}}<br>{{r.project}}</td><td>{{r.release_date}}</td><td>{{r.release_type}}</td><td><span class="badge {{ badge_class(r.deployment_status) }}">{{r.deployment_status}}</span></td><td><span class="badge {{ badge_class(r.uat_status) }}">{{r.uat_status}}</span></td><td><span class="badge {{ badge_class(r.approval_status) }}">{{r.approval_status}}</span></td></tr>{% endfor %}</tbody></table></div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddRelease(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const name = formData.get('name') || 'New Release';
    const version = formData.get('version') || '';
    const client = formData.get('client') || '-';
    const project = formData.get('project') || '-';
    const release_date = formData.get('release_date') || '-';
    const release_type = formData.get('release_type') || '-';
    const deployment_status = formData.get('deployment_status') || '-';
    const uat_status = formData.get('uat_status') || '-';
    const approval_status = formData.get('approval_status') || '-';
    const id = Date.now();
    const row = document.createElement('tr');
    row.id = 'release-' + id;
    row.innerHTML = '<td><b>' + name + '</b><br><span class="muted">' + version + '</span></td><td>' + client + '<br>' + project + '</td><td>' + release_date + '</td><td>' + release_type + '</td><td><span class="badge neutral">' + deployment_status + '</span></td><td><span class="badge neutral">' + uat_status + '</span></td><td><span class="badge neutral">' + approval_status + '</span></td>';
    row.style.opacity = '0.5';
    document.getElementById('releases-table').querySelector('tbody').appendChild(row);
    form.reset();
    toggleForm('release-form', 'add-release-btn');
}
</script>""",
        releases=releases, badge_class=badge_class,
    )
    return page(content)