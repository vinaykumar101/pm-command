from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import prds
from routes.layout import page
from utils.helpers import badge_class

prds_bp = Blueprint("prds", __name__, url_prefix="/prds")

PRD_KEYS = [
    "title", "client", "project", "background", "problem", "objective", "users", "personas", "current", "solution", "journey", "functional", "nonfunctional",
    "rbac", "api", "data", "edge", "acceptance", "dependencies", "risks", "metrics", "outscope", "release_plan", "uat_plan", "questions", "status"
]


@prds_bp.route("", methods=["GET", "POST"])
def prds_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in PRD_KEYS}
        prds.append(form_data)
        return redirect(url_for("prds.prds_page"))

    content = render_template_string(
        """<h1>PRD Builder</h1><p class="subtitle">Create structured Product Requirement Documents.</p>
<div class="card form-section"><div class="section-title">Create PRD</div><form method="post" class="form-grid">
    <input name="title" placeholder="PRD Title"><input name="client" placeholder="Client Name"><input name="project" placeholder="Project Name"><input name="status" placeholder="PRD Status">
    {% for k,label in [('background','Background'),('problem','Problem Statement'),('objective','Objective'),('users','Target Users'),('personas','User Personas'),('current','Current Process'),('solution','Proposed Solution'),('journey','User Journey'),('functional','Functional Requirements'),('nonfunctional','Non-Functional Requirements'),('rbac','Role-Based Access Control'),('api','API Requirements'),('data','Data Requirements'),('edge','Edge Cases'),('acceptance','Acceptance Criteria'),('dependencies','Dependencies'),('risks','Risks'),('metrics','Success Metrics'),('outscope','Out of Scope'),('release_plan','Release Plan'),('uat_plan','UAT Plan'),('questions','Open Questions')] %}<textarea name="{{k}}" placeholder="{{label}}"></textarea>{% endfor %}
    <div class="wide actions"><button>Save PRD</button><span class="btn secondary">Export PRD</span><span class="btn light">Generate User Stories</span><span class="btn light">Generate Acceptance Criteria</span></div>
</form></div>
<div class="grid two">{% for p in prds %}<div class="card"><h3>{{p.title}}</h3><p class="muted">{{p.client}} &bull; {{p.project}}</p><p>{{p.objective}}</p><span class="badge {{ badge_class(p.status) }}">{{p.status}}</span></div>{% endfor %}</div>""",
        prds=prds, badge_class=badge_class,
    )
    return page(content)