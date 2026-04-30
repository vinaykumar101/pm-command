from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import tasks
from routes.layout import page
from utils.helpers import badge_class

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
TASK_COLUMNS = ["Backlog", "To Do", "In Progress", "In Review", "QA", "UAT", "Done", "Blocked"]


@tasks_bp.route("", methods=["GET", "POST"])
def tasks_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "title", "client", "project", "prd", "type", "description",
            "acceptance", "assigned", "priority", "status", "sprint", "due", "estimate", "actual"
        ]}
        tasks.append(form_data)
        return redirect(url_for("tasks.tasks_page"))

    content = render_template_string(
        """<h1>Tasks</h1><p class="subtitle">Kanban board for PRD execution and sprint tracking.</p>
<div class="card form-section"><div class="section-title">Add Task</div><form method="post" class="form-grid">{% for k,label in [('title','Task Title'),('client','Client'),('project','Project'),('prd','Linked PRD'),('type','Task Type'),('assigned','Assigned To'),('priority','Priority'),('status','Status'),('sprint','Sprint'),('due','Due Date'),('estimate','Estimated Effort'),('actual','Actual Effort')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea name="description" placeholder="Description"></textarea><textarea name="acceptance" placeholder="Acceptance Criteria"></textarea><button>Add Task</button></form></div>
<div class="kanban">{% for col in cols %}<div class="kanban-col"><b>{{col}}</b>{% for t in tasks if t.status == col %}<div class="task-card"><b>{{t.title}}</b><p class="muted">{{t.project}} &bull; {{t.assigned}}</p><span class="badge {{ badge_class(t.priority) }}">{{t.priority}}</span><p>{{t.description}}</p><small>Due: {{t.due}}</small></div>{% endfor %}</div>{% endfor %}</div>""",
        tasks=tasks, cols=TASK_COLUMNS, badge_class=badge_class,
    )
    return page(content)