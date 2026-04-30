from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_metrics, add_metric
from routes.layout import page
from utils.helpers import badge_class

metrics_bp = Blueprint("metrics", __name__, url_prefix="/metrics")


@metrics_bp.route("", methods=["GET", "POST"])
def metrics_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "name", "current_value", "target_value", "status", "trend"
        ]}
        add_metric(form_data)
        return redirect(url_for("metrics.metrics_page"))

    metrics = get_metrics()
    content = render_template_string(
        """<h1>Product Metrics</h1><p class="subtitle">Track product health, adoption, retention and release performance.</p>
<div class="card form-section"><div class="section-title">Add Custom Metric</div><form method="post" class="form-grid"><input name="name" placeholder="Metric Name"><input name="current_value" placeholder="Current Value"><input name="target_value" placeholder="Target Value"><input name="status" placeholder="Status"><input name="trend" placeholder="Trend"><button>Add Metric</button></form></div>
<div class="grid cards">{% for m in metrics %}<div class="card"><div class="muted">{{m.name}}</div><div class="metric-value">{{m.current_value}}</div><p class="muted">Target: {{m.target_value}}</p><span class="badge {{ badge_class(m.status) }}">{{m.status}}</span> <span class="badge neutral">{{m.trend}}</span></div>{% endfor %}</div>""",
        metrics=metrics, badge_class=badge_class,
    )
    return page(content)