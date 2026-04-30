from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import validation_issues
from routes.layout import page
from utils.helpers import badge_class

validation_bp = Blueprint("validation", __name__, url_prefix="/validation")


@validation_bp.route("", methods=["GET", "POST"])
def validation_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "title", "client", "project", "source", "table",
            "description", "expected", "actual", "severity", "owner", "status", "date", "notes"
        ]}
        validation_issues.append(form_data)
        return redirect(url_for("validation.validation_page"))

    content = render_template_string(
        """<h1>Data Validation</h1><p class="subtitle">Track data quality, dashboard mismatches and API/report issues.</p>
<div class="card form-section"><div class="section-title">Add Validation Issue</div><form method="post" class="form-grid">{% for k,label in [('title','Issue Title'),('client','Client'),('project','Project'),('source','Data Source'),('table','Table / Report / API Name'),('expected','Expected Data'),('actual','Actual Data'),('severity','Severity'),('owner','Owner'),('status','Status'),('date','Date Identified')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="description" placeholder="Issue Description"></textarea><textarea name="notes" placeholder="Resolution Notes"></textarea><button>Add Issue</button></form></div>
<div class="card"><table><tr><th>Issue</th><th>Client/Project</th><th>Source</th><th>Expected</th><th>Actual</th><th>Severity</th><th>Status</th><th>Owner</th></tr>{% for i in validation_issues %}<tr><td><b>{{i.title}}</b><br><span class="muted">{{i.description}}</span></td><td>{{i.client}}<br>{{i.project}}</td><td>{{i.source}}<br><span class="muted">{{i.table}}</span></td><td>{{i.expected}}</td><td>{{i.actual}}</td><td><span class="badge {{ badge_class(i.severity) }}">{{i.severity}}</span></td><td><span class="badge {{ badge_class(i.status) }}">{{i.status}}</span></td><td>{{i.owner}}</td></tr>{% endfor %}</table></div>""",
        validation_issues=validation_issues, badge_class=badge_class,
    )
    return page(content)