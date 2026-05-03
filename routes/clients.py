from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import get_clients, add_client
from routes.layout import page
from utils.helpers import badge_class

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


@clients_bp.route("", methods=["GET", "POST"])
def clients_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "name", "industry", "contact", "email", "phone",
            "type", "priority", "engagement", "contract", "start_date", "notes"
        ]}
        client_id = add_client(form_data)
        
        if request.headers.get("HX-Request"):
            clients = get_clients()
            new_client = clients[-1] if clients else None
            if new_client:
                return render_template_string(
                    """<tr id="client-temp-{{client_id}}"><td><b>{{c.name}}</b><br><span class="muted">{{c.notes}}</span></td><td>{{c.industry}}</td><td>{{c.contact}}<br><span class="muted">{{c.email}}</span></td><td>{{c.type}}</td><td><span class="badge {{ badge_class(c.priority) }}">{{c.priority}}</span></td><td><span class="badge {{ badge_class(c.contract) }}">{{c.contract}}</span></td><td>{{c.start_date}}</td></tr>""",
                    c=new_client, client_id=client_id, badge_class=badge_class,
                )
            return ""
        return redirect(url_for("clients.clients_page"))

    clients = get_clients()
    content = render_template_string(
        """<h1>Clients</h1><p class="subtitle">Onboard and manage client accounts.</p>
<button class="btn secondary" onclick="toggleForm('client-form', 'add-client-btn')" id="add-client-btn">+ Add Client</button>
<div id="client-form" class="card form-section" style="display:none"><div class="section-title">Add Client</div>
<form class="form-grid" hx-post="{{ url_for('clients.clients_page') }}" hx-target="#clients-table" hx-swap="beforeend" hx-on::before-request="optimisticAddClient(event)">
<input name="name" placeholder="Client Name" required>
<input name="industry" placeholder="Industry">
<input name="contact" placeholder="Contact Person">
<input name="email" placeholder="Email">
<input name="phone" placeholder="Phone">
<input name="type" placeholder="Client Type">
<input name="priority" placeholder="Priority">
<input name="engagement" placeholder="Engagement Type">
<input name="contract" placeholder="Contract Status">
<input name="start_date" placeholder="Start Date">
<textarea class="wide" name="notes" placeholder="Notes"></textarea>
<button class="wide">Add Client</button>
</form>
</div>
<div class="card"><table id="clients-table"><thead><tr><th>Client</th><th>Industry</th><th>Contact</th><th>Type</th><th>Priority</th><th>Contract</th><th>Start</th></tr></thead><tbody>{% for c in clients %}<tr id="client-{{c.id}}"><td><b>{{c.name}}</b><br><span class="muted">{{c.notes}}</span></td><td>{{c.industry}}</td><td>{{c.contact}}<br><span class="muted">{{c.email}}</span></td><td>{{c.type}}</td><td><span class="badge {{ badge_class(c.priority) }}">{{c.priority}}</span></td><td><span class="badge {{ badge_class(c.contract) }}">{{c.contract}}</span></td><td>{{c.start_date}}</td></tr>{% endfor %}</tbody></table></div>
<script>
function toggleForm(id, btnId) {
    const f = document.getElementById(id);
    const b = document.getElementById(btnId);
    if (f.style.display === 'none') {
        f.style.display = 'block';
        b.style.display = 'none';
    } else {
        f.style.display = 'none';
        b.style.display = 'inline-block';
    }
}
function optimisticAddClient(e) {
    const form = e.detail.form;
    const formData = new FormData(form);
    const name = formData.get('name') || 'New Client';
    const industry = formData.get('industry') || '-';
    const contact = formData.get('contact') || '-';
    const email = formData.get('email') || '';
    const type = formData.get('type') || '-';
    const priority = formData.get('priority') || '-';
    const contract = formData.get('contract') || '-';
    const start_date = formData.get('start_date') || '-';
    const notes = formData.get('notes') || '';
    
    const id = Date.now();
    const row = document.createElement('tr');
    row.id = 'client-' + id;
    row.innerHTML = '<td><b>' + name + '</b><br><span class="muted">' + notes + '</span></td><td>' + industry + '</td><td>' + contact + '<br><span class="muted">' + email + '</span></td><td>' + type + '</td><td><span class="badge neutral">' + priority + '</span></td><td><span class="badge neutral">' + contract + '</span></td><td>' + start_date + '</td>';
    row.style.opacity = '0.5';
    document.getElementById('clients-table').querySelector('tbody').appendChild(row);
    form.reset();
    toggleForm('client-form', 'add-client-btn');
}
</script>""",
        clients=clients, badge_class=badge_class,
    )
    return page(content)