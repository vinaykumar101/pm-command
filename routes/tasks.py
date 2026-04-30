from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_tasks, get_projects, get_prds, add_task
from routes.layout import page
from utils.helpers import badge_class

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
TASK_COLUMNS = ["Backlog", "To Do", "In Progress", "In Review", "QA", "UAT", "Done", "Blocked"]


@tasks_bp.route("", methods=["GET", "POST"])
def tasks_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "title", "type", "description", "acceptance_criteria", "assigned_to", "priority", "status", "sprint", "due_date", "estimate", "actual_effort"
        ]}
        project_name = request.form.get("project", "").strip()
        prd_title = request.form.get("prd", "").strip()
        projects = get_projects()
        prds_data = get_prds()
        for p in projects:
            if p["name"] == project_name:
                form_data["project_id"] = p["id"]
                form_data["client_id"] = p.get("client_id")
                break
        for p in prds_data:
            if p["title"] == prd_title:
                form_data["prd_id"] = p["id"]
                break
        add_task(form_data)
        return redirect(url_for("tasks.tasks_page"))

    tasks = get_tasks()
    projects = get_projects()
    project_map = {p["id"]: p["name"] for p in projects}
    for t in tasks:
        t["project"] = project_map.get(t.get("project_id"), "Unknown")
    content = render_template_string(
        """<h1>Tasks</h1><p class="subtitle">Kanban board for PRD execution and sprint tracking.</p>
<div class="card form-section"><div class="section-title">Add Task</div><form method="post" class="form-grid">{% for k,label in [('title','Task Title'),('client','Client'),('project','Project'),('prd','Linked PRD'),('type','Task Type'),('assigned_to','Assigned To'),('priority','Priority'),('status','Status'),('sprint','Sprint'),('due_date','Due Date'),('estimate','Estimated Effort'),('actual_effort','Actual Effort')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="description" placeholder="Description"></textarea><textarea name="acceptance_criteria" placeholder="Acceptance Criteria"></textarea><button>Add Task</button></form></div>
<div class="kanban">{% for col in cols %}<div class="kanban-col"><b>{{col}}</b>{% for t in tasks if t.status == col %}<div class="task-card"><b>{{t.title}}</b><p class="muted">{{t.project}} &bull; {{t.assigned_to}}</p><span class="badge {{ badge_class(t.priority) }}">{{t.priority}}</span><p>{{t.description}}</p><small>Due: {{t.due_date}}</small></div>{% endfor %}</div>{% endfor %}</div>""",
        tasks=tasks, cols=TASK_COLUMNS, badge_class=badge_class,
    )
    return page(content)