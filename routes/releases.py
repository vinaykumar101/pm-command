from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import releases
from routes.layout import page
from utils.helpers import badge_class

releases_bp = Blueprint("releases", __name__, url_prefix="/releases")


@releases_bp.route("", methods=["GET", "POST"])
def releases_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "name", "version", "client", "project", "date", "type",
            "features", "bugs", "known", "deployment", "uat", "approval", "notes"
        ]}
        releases.append(form_data)
        return redirect(url_for("releases.releases_page"))

    content = render_template_string(
        """<h1>Releases</h1><p class="subtitle">Track release readiness, UAT status and deployment notes.</p>
<div class="card form-section"><div class="section-title">Add Release</div><form method="post" class="form-grid">{% for k,label in [('name','Release Name'),('version','Version Number'),('client','Client'),('project','Project'),('date','Release Date'),('type','Release Type'),('deployment','Deployment Status'),('uat','UAT Status'),('approval','Approval Status')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="features" placeholder="Features Included"></textarea><textarea name="bugs" placeholder="Bugs Fixed"></textarea><textarea name="known" placeholder="Known Issues"></textarea><textarea name="notes" placeholder="Release Notes"></textarea><button>Add Release</button></form></div>
<div class="card"><table><tr><th>Release</th><th>Client/Project</th><th>Date</th><th>Type</th><th>Deployment</th><th>UAT</th><th>Approval</th></tr>{% for r in releases %}<tr><td><b>{{r.name}}</b><br><span class="muted">{{r.version}}</span></td><td>{{r.client}}<br>{{r.project}}</td><td>{{r.date}}</td><td>{{r.type}}</td><td><span class="badge {{ badge_class(r.deployment) }}">{{r.deployment}}</span></td><td><span class="badge {{ badge_class(r.uat) }}">{{r.uat}}</span></td><td><span class="badge {{ badge_class(r.approval) }}">{{r.approval}}</span></td></tr>{% endfor %}</table></div>""",
        releases=releases, badge_class=badge_class,
    )
    return page(content)