from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import bugs
from routes.layout import page
from utils.helpers import badge_class

bugs_bp = Blueprint("bugs", __name__, url_prefix="/bugs")


@bugs_bp.route("", methods=["GET", "POST"])
def bugs_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "title", "description", "steps", "expected", "actual",
            "severity", "priority", "assigned", "status", "env", "by", "date"
        ]}
        bugs.append(form_data)
        return redirect(url_for("bugs.bugs_page"))

    content = render_template_string(
        """<h1>Bug Tracker</h1><p class="subtitle">Capture, assign and track bugs across dev, UAT and production.</p>
<div class="card form-section"><div class="section-title">Add Bug</div><form method="post" class="form-grid">{% for k,label in [('title','Bug Title'),('severity','Severity'),('priority','Priority'),('assigned','Assigned To'),('status','Status'),('env','Environment'),('by','Reported By'),('date','Reported Date')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="description" placeholder="Description"></textarea><textarea name="steps" placeholder="Steps to Reproduce"></textarea><textarea name="expected" placeholder="Expected Result"></textarea><textarea name="actual" placeholder="Actual Result"></textarea><button>Add Bug</button></form></div>
<div class="card"><table><tr><th>Bug</th><th>Severity</th><th>Priority</th><th>Assigned</th><th>Status</th><th>Environment</th><th>Date</th></tr>{% for b in bugs %}<tr><td><b>{{b.title}}</b><br><span class="muted">{{b.description}}</span></td><td><span class="badge {{ badge_class(b.severity) }}">{{b.severity}}</span></td><td><span class="badge {{ badge_class(b.priority) }}">{{b.priority}}</span></td><td>{{b.assigned}}</td><td><span class="badge {{ badge_class(b.status) }}">{{b.status}}</span></td><td>{{b.env}}</td><td>{{b.date}}</td></tr>{% endfor %}</table></div>""",
        bugs=bugs, badge_class=badge_class,
    )
    return page(content)