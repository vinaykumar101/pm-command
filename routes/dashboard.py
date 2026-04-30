from flask import Blueprint, render_template_string, session
from data.store import clients, projects, prds, tasks, bugs, uat_cases, releases, validation_issues, funnel
from services.dashboard import dashboard_stats
from routes.layout import page

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    stats = dashboard_stats(clients, projects, prds, tasks, bugs, uat_cases, releases, validation_issues, funnel)
    role = session.get("role", "Product Manager")
    content = render_template_string(
        """<h1>Dashboard</h1><p class="subtitle">Single source of truth for clients, requirements, PRDs, delivery, analytics and release readiness.</p>
<div class="grid cards">
    {% for title, value in cards %}<div class="card"><div class="muted">{{title}}</div><div class="metric-value">{{value}}</div></div>{% endfor %}
</div>
<div class="grid two" style="margin-top:18px">
    <div class="card"><div class="section-title">Project Status Summary</div>{% for k,v in project_counts.items() %}<p>{{k}} <span class="badge {{ badge_class(k) }}">{{v}}</span></p>{% endfor %}</div>
    <div class="card"><div class="section-title">Task Status Summary</div>{% for k,v in task_counts.items() %}<p>{{k}} <span class="badge {{ badge_class(k) }}">{{v}}</span></p>{% endfor %}</div>
    <div class="card"><div class="section-title">Bug Severity Summary</div>{% for k,v in bug_counts.items() %}<p>{{k}} <span class="badge {{ badge_class(k) }}">{{v}}</span></p>{% endfor %}</div>
    <div class="card"><div class="section-title">Funnel Conversion Snapshot</div>{% for name,num in funnel %}<div class="funnel-row" style="grid-template-columns:150px 1fr 70px"><b>{{name}}</b><div class="bar"><span style="width:{{ (num/funnel[0][1]*100)|round }}%"></span></div><span>{{num}}</span></div>{% endfor %}</div>
</div>
<div class="card" style="margin-top:18px"><div class="section-title">Recent Activity</div><table><tr><th>Activity</th><th>Status</th><th>Date</th></tr><tr><td>AgriPulse UAT build shared</td><td><span class="badge warning">Pending Acceptance</span></td><td>2026-04-17</td></tr><tr><td>DigiAcre RBAC development started</td><td><span class="badge warning">In Progress</span></td><td>2026-04-20</td></tr><tr><td>Dashboard count mismatch logged</td><td><span class="badge danger">Open</span></td><td>2026-04-22</td></tr></table></div>""",
        cards=stats["cards"],
        funnel=funnel,
        role=role,
        project_counts=stats["project_counts"],
        task_counts=stats["task_counts"],
        bug_counts=stats["bug_counts"],
    )
    return page(content, role=role)