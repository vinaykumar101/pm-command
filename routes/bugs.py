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
        add_bug(form_data)
        return redirect(url_for("bugs.bugs_page"))

    bugs = get_bugs()
    content = render_template_string(
        """<h1>Bug Tracker</h1><p class="subtitle">Capture, assign and track bugs across dev, UAT and production.</p>
<div class="card form-section"><div class="section-title">Add Bug</div><form method="post" class="form-grid">{% for k,label in [('title','Bug Title'),('severity','Severity'),('priority','Priority'),('assigned_to','Assigned To'),('status','Status'),('environment','Environment'),('reported_by','Reported By'),('reported_date','Reported Date')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="description" placeholder="Description"></textarea><textarea name="steps_to_reproduce" placeholder="Steps to Reproduce"></textarea><textarea name="expected_result" placeholder="Expected Result"></textarea><textarea name="actual_result" placeholder="Actual Result"></textarea><button>Add Bug</button></form></div>
<div class="card"><table><tr><th>Bug</th><th>Severity</th><th>Priority</th><th>Assigned</th><th>Status</th><th>Environment</th><th>Date</th></tr>{% for b in bugs %}<tr><td><b>{{b.title}}</b><br><span class="muted">{{b.description}}</span></td><td><span class="badge {{ badge_class(b.severity) }}">{{b.severity}}</span></td><td><span class="badge {{ badge_class(b.priority) }}">{{b.priority}}</span></td><td>{{b.assigned_to}}</td><td><span class="badge {{ badge_class(b.status) }}">{{b.status}}</span></td><td>{{b.environment}}</td><td>{{b.reported_date}}</td></tr>{% endfor %}</table></div>""",
        bugs=bugs, badge_class=badge_class,
    )
    return page(content)