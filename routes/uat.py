from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import uat_cases
from routes.layout import page
from utils.helpers import badge_class

uat_bp = Blueprint("uat", __name__, url_prefix="/uat")


@uat_bp.route("", methods=["GET", "POST"])
def uat_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "name", "module", "feature", "expected", "actual",
            "status", "severity", "tester", "date", "remarks", "task", "prd"
        ]}
        uat_cases.append(form_data)
        return redirect(url_for("uat.uat_page"))

    total = len(uat_cases)
    passed = sum(1 for u in uat_cases if u["status"] == "Pass")
    pass_rate = round(passed / total * 100) if total else 0

    content = render_template_string(
        """<h1>UAT Tracker</h1><p class="subtitle">Track test cases, pass/fail status and release readiness.</p>
<div class="grid cards"><div class="card"><div class="muted">Total Test Cases</div><div class="metric-value">{{ total }}</div></div><div class="card"><div class="muted">Passed</div><div class="metric-value">{{ passed }}</div></div><div class="card"><div class="muted">Failed/Blocked</div><div class="metric-value">{{ total-passed }}</div></div><div class="card"><div class="muted">UAT Pass %</div><div class="metric-value">{{ pass_rate }}%</div></div></div>
<div class="card form-section" style="margin-top:18px"><div class="section-title">Add Test Case</div><form method="post" class="form-grid">{% for k,label in [('name','Test Case Name'),('module','Module'),('feature','Feature'),('expected','Expected Result'),('actual','Actual Result'),('status','Status'),('severity','Severity'),('tester','Tester Name'),('date','Testing Date'),('remarks','Remarks'),('task','Linked Task'),('prd','Linked PRD')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<button>Add Test Case</button></form></div>
<div class="card"><table><tr><th>Test Case</th><th>Module</th><th>Expected</th><th>Actual</th><th>Status</th><th>Severity</th><th>Tester</th></tr>{% for u in uat_cases %}<tr><td><b>{{u.name}}</b><br><span class="muted">{{u.feature}}</span></td><td>{{u.module}}</td><td>{{u.expected}}</td><td>{{u.actual}}</td><td><span class="badge {{ badge_class(u.status) }}">{{u.status}}</span></td><td><span class="badge {{ badge_class(u.severity) }}">{{u.severity}}</span></td><td>{{u.tester}}</td></tr>{% endfor %}</table></div>""",
        uat_cases=uat_cases, total=total, passed=passed, pass_rate=pass_rate, badge_class=badge_class,
    )
    return page(content)