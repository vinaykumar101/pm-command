from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import projects
from routes.layout import page
from utils.helpers import badge_class

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")


@projects_bp.route("", methods=["GET", "POST"])
def projects_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "name", "client", "type", "problem", "objective", "users",
            "metrics", "owner", "tech", "qa", "start", "release", "status", "priority", "risk"
        ]}
        projects.append(form_data)
        return redirect(url_for("projects.projects_page"))

    content = render_template_string(
        """<h1>Projects</h1><p class="subtitle">Create projects under clients and track delivery status.</p>
<div class="card form-section"><div class="section-title">Add Project</div><form method="post" class="form-grid">{% for k,label in [('name','Project Name'),('client','Client'),('type','Project Type'),('owner','Project Owner'),('tech','Tech Owner'),('qa','QA Owner'),('start','Start Date'),('release','Target Release Date'),('status','Status'),('priority','Priority'),('risk','Risk Level'),('users','Target Users'),('metrics','Success Metrics')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="problem" placeholder="Problem Statement"></textarea><textarea name="objective" placeholder="Business Objective"></textarea><button>Add Project</button></form></div>
<div class="card"><table><tr><th>Project</th><th>Client</th><th>Type</th><th>Owner</th><th>Status</th><th>Priority</th><th>Risk</th><th>Release</th></tr>{% for p in projects %}<tr><td><b>{{p.name}}</b><br><span class="muted">{{p.problem}}</span></td><td>{{p.client}}</td><td>{{p.type}}</td><td>{{p.owner}}</td><td><span class="badge {{ badge_class(p.status) }}">{{p.status}}</span></td><td><span class="badge {{ badge_class(p.priority) }}">{{p.priority}}</span></td><td><span class="badge {{ badge_class(p.risk) }}">{{p.risk}}</span></td><td>{{p.release}}</td></tr>{% endfor %}</table></div>""",
        projects=projects, badge_class=badge_class,
    )
    return page(content)