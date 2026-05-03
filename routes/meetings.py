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
        meeting_id = add_meeting(form_data)
        
        if request.headers.get("HX-Request"):
            meetings = get_meetings()
            new_meeting = meetings[-1] if meetings else None
            if new_meeting:
                return render_template_string(
                    """<tr id="meeting-temp-{{meeting_id}}"><td><b>{{m.title}}</b><br><span class="muted">{{m.meeting_date}}</span></td><td>{{project}}</td><td>{{m.owner}}</td><td><span class="badge {{ badge_class(m.status) }}">{{m.status}}</span></td></tr>""",
                    m=new_meeting, project=project_name, meeting_id=meeting_id, badge_class=badge_class,
                )
            return ""
        return redirect(url_for("meetings.meetings_page"))

    meetings = get_meetings()
    projects = get_projects()
    project_map = {p["id"]: p["name"] for p in projects}
    for m in meetings:
        m["project"] = project_map.get(m.get("project_id"), "Unknown")
    content = render_template_string(
        """<h1>Meetings &amp; Stakeholder Updates</h1><p class="subtitle">Capture meeting decisions, actions and weekly updates.</p>
<button class="btn secondary" onclick="toggleForm('meeting-form', 'add-meeting-btn')" id="add-meeting-btn">+ Add Meeting</button>
<div id="meeting-form" class="card form-section" style="display:none"><div class="section-title">Add Meeting</div>
<form class="form-grid" hx-post="{{ url_for('meetings.meetings_page') }}" hx-target="#meetings-table" hx-swap="beforeend" hx-on::before-request="optimisticAddMeeting(event)">
<input name="title" placeholder="Meeting Title" required>
<input name="client" placeholder="Client">
<input name="project" placeholder="Project">
<input name="meeting_date" placeholder="Date">
<input name="attendees" placeholder="Attendees">
<input name="owner" placeholder="Owner">
<input name="due_date" placeholder="Due Date">
<input name="status" placeholder="Status">
<textarea name="discussion_points" placeholder="Discussion Points"></textarea>
<textarea name="decisions" placeholder="Decisions Taken"></textarea>
<textarea name="action_items" placeholder="Action Items"></textarea>
<button class="wide">Add Meeting</button>
</form>
</div>
<div class="grid two"><div class="card"><div class="section-title">Meetings</div><table id="meetings-table"><thead><tr><th>Meeting</th><th>Project</th><th>Owner</th><th>Status</th></tr></thead><tbody>{% for m in meetings %}<tr id="meeting-{{m.id}}"><td><b>{{m.title}}</b><br><span class="muted">{{m.meeting_date}}</span></td><td>{{m.project}}</td><td>{{m.owner}}</td><td><span class="badge {{ badge_class(m.status) }}">{{m.status}}</span></td></tr>{% endfor %}</tbody></table></div><div class="card"><div class="section-title">Weekly Stakeholder Update Template</div><p><b>Overall Status:</b> <span class="badge warning">Amber</span></p><p><b>Progress This Week:</b> UAT completed, selected users received build.</p><p><b>Planned Next Week:</b> Close P0/P1 issues and validate acceptance.</p><p><b>Risks:</b> Image upload failures and offline sync edge cases.</p><p><b>Decisions Required:</b> Production promotion criteria.</p></div></div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddMeeting(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const title = formData.get('title') || 'New Meeting';
    const meeting_date = formData.get('meeting_date') || '-';
    const project = formData.get('project') || '-';
    const owner = formData.get('owner') || '-';
    const status = formData.get('status') || '-';
    const id = Date.now();
    const row = document.createElement('tr');
    row.id = 'meeting-' + id;
    row.innerHTML = '<td><b>' + title + '</b><br><span class="muted">' + meeting_date + '</span></td><td>' + project + '</td><td>' + owner + '</td><td><span class="badge neutral">' + status + '</span></td>';
    row.style.opacity = '0.5';
    document.getElementById('meetings-table').querySelector('tbody').appendChild(row);
    form.reset();
    toggleForm('meeting-form', 'add-meeting-btn');
}
</script>""",
        meetings=meetings, badge_class=badge_class,
    )
    return page(content)