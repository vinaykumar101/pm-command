from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_uat_cases, add_uat_case
from routes.layout import page
from utils.helpers import badge_class

uat_bp = Blueprint("uat", __name__, url_prefix="/uat")


@uat_bp.route("", methods=["GET", "POST"])
def uat_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "name", "module", "feature", "expected_result", "actual_result",
            "status", "severity", "tester", "test_date", "remarks", "task_id", "prd_link"
        ]}
        uat_id = add_uat_case(form_data)
        
        if request.headers.get("HX-Request"):
            uat_cases = get_uat_cases()
            new_case = uat_cases[-1] if uat_cases else None
            if new_case:
                return render_template_string(
                    """<tr id="uat-temp-{{uat_id}}"><td><b>{{u.name}}</b><br><span class="muted">{{u.feature}}</span></td><td>{{u.module}}</td><td>{{u.expected_result}}</td><td>{{u.actual_result}}</td><td><span class="badge {{ badge_class(u.status) }}">{{u.status}}</span></td><td><span class="badge {{ badge_class(u.severity) }}">{{u.severity}}</span></td><td>{{u.tester}}</td></tr>""",
                    u=new_case, uat_id=uat_id, badge_class=badge_class,
                )
            return ""
        return redirect(url_for("uat.uat_page"))

    uat_cases = get_uat_cases()
    total = len(uat_cases)
    passed = sum(1 for u in uat_cases if u["status"] == "Pass")
    pass_rate = round(passed / total * 100) if total else 0

    content = render_template_string(
        """<h1>UAT Tracker</h1><p class="subtitle">Track test cases, pass/fail status and release readiness.</p>
<div class="grid cards"><div class="card"><div class="muted">Total Test Cases</div><div class="metric-value">{{ total }}</div></div><div class="card"><div class="muted">Passed</div><div class="metric-value">{{ passed }}</div></div><div class="card"><div class="muted">Failed/Blocked</div><div class="metric-value">{{ total-passed }}</div></div><div class="card"><div class="muted">UAT Pass %</div><div class="metric-value">{{ pass_rate }}%</div></div></div>
<button class="btn secondary" onclick="toggleForm('uat-form', 'add-uat-btn')" id="add-uat-btn" style="margin-top:18px">+ Add Test Case</button>
<div id="uat-form" class="card form-section" style="display:none;margin-top:18px"><div class="section-title">Add Test Case</div>
<form class="form-grid" hx-post="{{ url_for('uat.uat_page') }}" hx-target="#uat-table" hx-swap="beforeend" hx-on::before-request="optimisticAddUAT(event)">
<input name="name" placeholder="Test Case Name" required>
<input name="module" placeholder="Module">
<input name="feature" placeholder="Feature">
<input name="expected_result" placeholder="Expected Result">
<input name="actual_result" placeholder="Actual Result">
<input name="status" placeholder="Status" value="Pending">
<input name="severity" placeholder="Severity">
<input name="tester" placeholder="Tester Name">
<input name="test_date" placeholder="Testing Date">
<input name="remarks" placeholder="Remarks">
<input name="task_id" placeholder="Linked Task">
<input name="prd_link" placeholder="Linked PRD">
<button class="wide">Add Test Case</button>
</form>
</div>
<div class="card"><table id="uat-table"><thead><tr><th>Test Case</th><th>Module</th><th>Expected</th><th>Actual</th><th>Status</th><th>Severity</th><th>Tester</th></tr></thead><tbody>{% for u in uat_cases %}<tr id="uat-{{u.id}}"><td><b>{{u.name}}</b><br><span class="muted">{{u.feature}}</span></td><td>{{u.module}}</td><td>{{u.expected_result}}</td><td>{{u.actual_result}}</td><td><span class="badge {{ badge_class(u.status) }}">{{u.status}}</span></td><td><span class="badge {{ badge_class(u.severity) }}">{{u.severity}}</span></td><td>{{u.tester}}</td></tr>{% endfor %}</tbody></table></div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddUAT(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const name = formData.get('name') || 'New Test Case';
    const module = formData.get('module') || '-';
    const feature = formData.get('feature') || '';
    const status = formData.get('status') || 'Pending';
    const severity = formData.get('severity') || '-';
    const tester = formData.get('tester') || '-';
    const id = Date.now();
    const row = document.createElement('tr');
    row.id = 'uat-' + id;
    row.innerHTML = '<td><b>' + name + '</b><br><span class="muted">' + feature + '</span></td><td>' + module + '</td><td>-</td><td>-</td><td><span class="badge neutral">' + status + '</span></td><td><span class="badge neutral">' + severity + '</span></td><td>' + tester + '</td>';
    row.style.opacity = '0.5';
    document.getElementById('uat-table').querySelector('tbody').appendChild(row);
    form.reset();
    toggleForm('uat-form', 'add-uat-btn');
}
</script>""",
        uat_cases=uat_cases, total=total, passed=passed, pass_rate=pass_rate, badge_class=badge_class,
    )
    return page(content)