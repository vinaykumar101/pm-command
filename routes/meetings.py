from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_meetings, get_clients, get_projects, add_meeting
from routes.layout import page
from utils.helpers import badge_class

meetings_bp = Blueprint("meetings", __name__, url_prefix="/meetings")


@meetings_bp.route("", methods=["GET", "POST"])
def meetings_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "title", "meeting_date", "attendees", "discussion_points",
            "decisions", "action_items", "owner", "due_date", "status"
        ]}
        client_name = request.form.get("client", "").strip()
        project_name = request.form.get("project", "").strip()
        clients = get_clients()
        projects = get_projects()
        for c in clients:
            if c["name"] == client_name:
                form_data["client_id"] = c["id"]
                break
        for p in projects:
            if p["name"] == project_name:
                form_data["project_id"] = p["id"]
                break
        add_meeting(form_data)
        return redirect(url_for("meetings.meetings_page"))

    meetings = get_meetings()
    projects = get_projects()
    project_map = {p["id"]: p["name"] for p in projects}
    for m in meetings:
        m["project"] = project_map.get(m.get("project_id"), "Unknown")
    content = render_template_string(
        """<h1>Meetings &amp; Stakeholder Updates</h1><p class="subtitle">Capture meeting decisions, actions and weekly updates.</p>
<div class="card form-section"><div class="section-title">Add Meeting</div><form method="post" class="form-grid">{% for k,label in [('title','Meeting Title'),('client','Client'),('project','Project'),('meeting_date','Date'),('attendees','Attendees'),('owner','Owner'),('due_date','Due Date'),('status','Status')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="discussion_points" placeholder="Discussion Points"></textarea><textarea name="decisions" placeholder="Decisions Taken"></textarea><textarea name="action_items" placeholder="Action Items"></textarea><button>Add Meeting</button></form></div>
<div class="grid two"><div class="card"><div class="section-title">Meetings</div><table><tr><th>Meeting</th><th>Project</th><th>Owner</th><th>Status</th></tr>{% for m in meetings %}<tr><td><b>{{m.title}}</b><br><span class="muted">{{m.meeting_date}}</span></td><td>{{m.project}}</td><td>{{m.owner}}</td><td><span class="badge {{ badge_class(m.status) }}">{{m.status}}</span></td></tr>{% endfor %}</table></div><div class="card"><div class="section-title">Weekly Stakeholder Update Template</div><p><b>Overall Status:</b> <span class="badge warning">Amber</span></p><p><b>Progress This Week:</b> UAT completed, selected users received build.</p><p><b>Planned Next Week:</b> Close P0/P1 issues and validate acceptance.</p><p><b>Risks:</b> Image upload failures and offline sync edge cases.</p><p><b>Decisions Required:</b> Production promotion criteria.</p></div></div>""",
        meetings=meetings, badge_class=badge_class,
    )
    return page(content)