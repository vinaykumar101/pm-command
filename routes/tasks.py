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
        task_id = add_task(form_data)
        
        if request.headers.get("HX-Request"):
            tasks = get_tasks()
            new_task = tasks[-1] if tasks else None
            if new_task:
                project_map = {p["id"]: p["name"] for p in projects}
                new_task["project"] = project_map.get(new_task.get("project_id"), "Unknown")
                return render_template_string(
                    """<div class="task-card" id="task-temp-{{task_id}}"><b>{{t.title}}</b><p class="muted">{{project}} &bull; {{t.assigned_to}}</p><span class="badge {{ badge_class(t.priority) }}">{{t.priority}}</span><p>{{t.description}}</p><small>Due: {{t.due_date}}</small></div>""",
                    t=new_task, project=project_name, task_id=task_id, badge_class=badge_class,
                )
            return ""
        return redirect(url_for("tasks.tasks_page"))

    tasks = get_tasks()
    projects = get_projects()
    project_map = {p["id"]: p["name"] for p in projects}
    for t in tasks:
        t["project"] = project_map.get(t.get("project_id"), "Unknown")
    content = render_template_string(
        """<h1>Tasks</h1><p class="subtitle">Kanban board for PRD execution and sprint tracking.</p>
<button class="btn secondary" onclick="toggleForm('task-form', 'add-task-btn')" id="add-task-btn">+ Add Task</button>
<div id="task-form" class="card form-section" style="display:none"><div class="section-title">Add Task</div>
<form class="form-grid" hx-post="{{ url_for('tasks.tasks_page') }}" hx-target="#tasks-kanban" hx-swap="beforeend" hx-on::before-request="optimisticAddTask(event)">
<input name="title" placeholder="Task Title" required>
<input name="project" placeholder="Project">
<input name="prd" placeholder="Linked PRD">
<input name="type" placeholder="Task Type">
<input name="assigned_to" placeholder="Assigned To">
<input name="priority" placeholder="Priority">
<input name="status" placeholder="Status" value="Backlog">
<input name="sprint" placeholder="Sprint">
<input name="due_date" placeholder="Due Date">
<input name="estimate" placeholder="Estimated Effort">
<input name="actual_effort" placeholder="Actual Effort">
<textarea name="description" placeholder="Description"></textarea>
<textarea name="acceptance_criteria" placeholder="Acceptance Criteria"></textarea>
<button class="wide">Add Task</button>
</form>
</div>
<div class="kanban" id="tasks-kanban">{% for col in cols %}<div class="kanban-col"><b>{{col}}</b>{% for t in tasks if t.status == col %}<div class="task-card" id="task-{{t.id}}"><b>{{t.title}}</b><p class="muted">{{t.project}} &bull; {{t.assigned_to}}</p><span class="badge {{ badge_class(t.priority) }}">{{t.priority}}</span><p>{{t.description}}</p><small>Due: {{t.due_date}}</small></div>{% endfor %}</div>{% endfor %}</div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') { f.style.display = 'block'; b.style.display = 'none'; }
    else { f.style.display = 'none'; b.style.display = 'inline-block'; }
}
function optimisticAddTask(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const title = formData.get('title') || 'New Task';
    const project = formData.get('project') || 'Unknown';
    const assigned_to = formData.get('assigned_to') || '-';
    const priority = formData.get('priority') || '-';
    const description = formData.get('description') || '';
    const due_date = formData.get('due_date') || '-';
    const status = formData.get('status') || 'Backlog';
    const id = Date.now();
    const card = document.createElement('div');
    card.className = 'task-card';
    card.id = 'task-' + id;
    card.style.opacity = '0.5';
    card.innerHTML = '<b>' + title + '</b><p class="muted">' + project + ' &bull; ' + assigned_to + '</p><span class="badge neutral">' + priority + '</span><p>' + description + '</p><small>Due: ' + due_date + '</small>';
    const kanban = document.getElementById('tasks-kanban');
    const kanbanCols = kanban.querySelectorAll('.kanban-col');
    kanbanCols.forEach(col => {
        if (col.querySelector('b').textContent === status) { col.appendChild(card); }
    });
    form.reset();
    toggleForm('task-form', 'add-task-btn');
}
</script>""",
        tasks=tasks, cols=TASK_COLUMNS, badge_class=badge_class,
    )
    return page(content)