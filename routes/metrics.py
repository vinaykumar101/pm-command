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
        metric_id = add_metric(form_data)
        
        if request.headers.get("HX-Request"):
            metrics = get_metrics()
            new_metric = metrics[-1] if metrics else None
            if new_metric:
                return render_template_string(
                    """<div class="card" id="metric-temp-{{metric_id}}"><div class="muted">{{m.name}}</div><div class="metric-value">{{m.current_value}}</div><p class="muted">Target: {{m.target_value}}</p><span class="badge {{ badge_class(m.status) }}">{{m.status}}</span> <span class="badge neutral">{{m.trend}}</span></div>""",
                    m=new_metric, metric_id=metric_id, badge_class=badge_class,
                )
            return ""
        return redirect(url_for("metrics.metrics_page"))

    metrics = get_metrics()
    content = render_template_string(
        """<h1>Product Metrics</h1><p class="subtitle">Track product health, adoption, retention and release performance.</p>
<button class="btn secondary" onclick="toggleForm('metric-form', 'add-metric-btn')" id="add-metric-btn">+ Add Custom Metric</button>
<div id="metric-form" class="card form-section" style="display:none"><div class="section-title">Add Custom Metric</div>
<form class="form-grid" hx-post="{{ url_for('metrics.metrics_page') }}" hx-target="#metrics-grid" hx-swap="beforeend" hx-on::before-request="optimisticAddMetric(event)">
<input name="name" placeholder="Metric Name" required>
<input name="current_value" placeholder="Current Value">
<input name="target_value" placeholder="Target Value">
<input name="status" placeholder="Status">
<input name="trend" placeholder="Trend">
<button class="wide">Add Metric</button>
</form>
</div>
<div class="grid cards" id="metrics-grid">{% for m in metrics %}<div class="card" id="metric-{{m.id}}"><div class="muted">{{m.name}}</div><div class="metric-value">{{m.current_value}}</div><p class="muted">Target: {{m.target_value}}</p><span class="badge {{ badge_class(m.status) }}">{{m.status}}</span> <span class="badge neutral">{{m.trend}}</span></div>{% endfor %}</div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddMetric(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const name = formData.get('name') || 'New Metric';
    const current_value = formData.get('current_value') || '-';
    const target_value = formData.get('target_value') || '-';
    const status = formData.get('status') || '-';
    const trend = formData.get('trend') || '-';
    const id = Date.now();
    const card = document.createElement('div');
    card.className = 'card';
    card.id = 'metric-' + id;
    card.style.opacity = '0.5';
    card.innerHTML = '<div class="muted">' + name + '</div><div class="metric-value">' + current_value + '</div><p class="muted">Target: ' + target_value + '</p><span class="badge neutral">' + status + '</span> <span class="badge neutral">' + trend + '</span>';
    document.getElementById('metrics-grid').appendChild(card);
    form.reset();
    toggleForm('metric-form', 'add-metric-btn');
}
</script>""",
        metrics=metrics, badge_class=badge_class,
    )
    return page(content)