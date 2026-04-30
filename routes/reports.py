from flask import Blueprint, render_template_string
from data.store import reports
from routes.layout import page
from utils.helpers import badge_class

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("")
def reports_page():
    content = render_template_string(
        """<h1>Reports</h1><p class="subtitle">Leadership-ready reporting cards for PM reviews.</p>
<div class="grid two">{% for name,desc,updated in reports %}<div class="card report-card"><div><h3>{{name}}</h3><p class="muted">{{desc}}</p><small>Last updated: {{updated}}</small></div><div class="actions"><span class="btn light">View</span><span class="btn secondary">Export</span></div></div>{% endfor %}</div>""",
        reports=reports, badge_class=badge_class,
    )
    return page(content)