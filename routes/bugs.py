from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_bugs, add_bug
from routes.layout import page
from utils.helpers import badge_class

bugs_bp = Blueprint("bugs", __name__, url_prefix="/bugs")


@bugs_bp.route("", methods=["GET", "POST"])
def bugs_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "title", "description", "steps_to_reproduce", "expected_result", "actual_result",
            "severity", "priority", "assigned_to", "status", "environment", "reported_by", "reported_date"
        ]}
        bug_id = add_bug(form_data)
        
        if request.headers.get("HX-Request"):
            bugs = get_bugs()
            new_bug = bugs[-1] if bugs else None
            if new_bug:
                return render_template_string(
                    """<tr id="bug-temp-{{bug_id}}"><td><b>{{b.title}}</b><br><span class="muted">{{b.description}}</span></td><td><span class="badge {{ badge_class(b.severity) }}">{{b.severity}}</span></td><td><span class="badge {{ badge_class(b.priority) }}">{{b.priority}}</span></td><td>{{b.assigned_to}}</td><td><span class="badge {{ badge_class(b.status) }}">{{b.status}}</span></td><td>{{b.environment}}</td><td>{{b.reported_date}}</td></tr>""",
                    b=new_bug, bug_id=bug_id, badge_class=badge_class,
                )
            return ""
        return redirect(url_for("bugs.bugs_page"))

    bugs = get_bugs()
    content = render_template_string(
        """<h1>Bug Tracker</h1><p class="subtitle">Capture, assign and track bugs across dev, UAT and production.</p>
<button class="btn secondary" onclick="toggleForm('bug-form', 'add-bug-btn')" id="add-bug-btn">+ Add Bug</button>
<div id="bug-form" class="card form-section" style="display:none"><div class="section-title">Add Bug</div>
<form class="form-grid" hx-post="{{ url_for('bugs.bugs_page') }}" hx-target="#bugs-table" hx-swap="beforeend" hx-on::before-request="optimisticAddBug(event)">
<input name="title" placeholder="Bug Title" required>
<input name="severity" placeholder="Severity">
<input name="priority" placeholder="Priority">
<input name="assigned_to" placeholder="Assigned To">
<input name="status" placeholder="Status">
<input name="environment" placeholder="Environment">
<input name="reported_by" placeholder="Reported By">
<input name="reported_date" placeholder="Reported Date">
<textarea name="description" placeholder="Description"></textarea>
<textarea name="steps_to_reproduce" placeholder="Steps to Reproduce"></textarea>
<textarea name="expected_result" placeholder="Expected Result"></textarea>
<textarea name="actual_result" placeholder="Actual Result"></textarea>
<button class="wide">Add Bug</button>
</form>
</div>
<div class="card"><table id="bugs-table"><thead><tr><th>Bug</th><th>Severity</th><th>Priority</th><th>Assigned</th><th>Status</th><th>Environment</th><th>Date</th></tr></thead><tbody>{% for b in bugs %}<tr id="bug-{{b.id}}"><td><b>{{b.title}}</b><br><span class="muted">{{b.description}}</span></td><td><span class="badge {{ badge_class(b.severity) }}">{{b.severity}}</span></td><td><span class="badge {{ badge_class(b.priority) }}">{{b.priority}}</span></td><td>{{b.assigned_to}}</td><td><span class="badge {{ badge_class(b.status) }}">{{b.status}}</span></td><td>{{b.environment}}</td><td>{{b.reported_date}}</td></tr>{% endfor %}</tbody></table></div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddBug(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const title = formData.get('title') || 'New Bug';
    const severity = formData.get('severity') || '-';
    const priority = formData.get('priority') || '-';
    const assigned_to = formData.get('assigned_to') || '-';
    const status = formData.get('status') || '-';
    const environment = formData.get('environment') || '-';
    const reported_date = formData.get('reported_date') || '-';
    const description = formData.get('description') || '';
    const id = Date.now();
    const row = document.createElement('tr');
    row.id = 'bug-' + id;
    row.innerHTML = '<td><b>' + title + '</b><br><span class="muted">' + description + '</span></td><td><span class="badge neutral">' + severity + '</span></td><td><span class="badge neutral">' + priority + '</span></td><td>' + assigned_to + '</td><td><span class="badge neutral">' + status + '</span></td><td>' + environment + '</td><td>' + reported_date + '</td>';
    row.style.opacity = '0.5';
    document.getElementById('bugs-table').querySelector('tbody').appendChild(row);
    form.reset();
    toggleForm('bug-form', 'add-bug-btn');
}
</script>""",
        bugs=bugs, badge_class=badge_class,
    )
    return page(content)