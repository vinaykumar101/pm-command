from flask import Blueprint, request, redirect, url_for, render_template_string
from data.store import clients
from routes.layout import page
from utils.helpers import badge_class

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


@clients_bp.route("", methods=["GET", "POST"])
def clients_page():
    if request.method == "POST":
        form_data = {k: request.form.get(k, "").strip() for k in [
            "name", "industry", "contact", "email", "phone",
            "type", "priority", "engagement", "contract", "start", "notes"
        ]}
        clients.append(form_data)
        return redirect(url_for("clients.clients_page"))

    content = render_template_string(
        """<h1>Clients</h1><p class="subtitle">Onboard and manage client accounts.</p>
<div class="card form-section"><div class="section-title">Add Client</div><form method="post" class="form-grid">{% for k,label in [('name','Client Name'),('industry','Industry'),('contact','Contact Person'),('email','Email'),('phone','Phone'),('type','Client Type'),('priority','Priority'),('engagement','Engagement Type'),('contract','Contract Status'),('start','Start Date')] %}<input name="{{k}}" placeholder="{{label}}">{% endfor %}<textarea class="wide" name="notes" placeholder="Notes"></textarea><button>Add Client</button></form></div>
<div class="card"><table><tr><th>Client</th><th>Industry</th><th>Contact</th><th>Type</th><th>Priority</th><th>Contract</th><th>Start</th></tr>{% for c in clients %}<tr><td><b>{{c.name}}</b><br><span class="muted">{{c.notes}}</span></td><td>{{c.industry}}</td><td>{{c.contact}}<br><span class="muted">{{c.email}}</span></td><td>{{c.type}}</td><td><span class="badge {{ badge_class(c.priority) }}">{{c.priority}}</span></td><td><span class="badge {{ badge_class(c.contract) }}">{{c.contract}}</span></td><td>{{c.start}}</td></tr>{% endfor %}</table></div>""",
        clients=clients, badge_class=badge_class,
    )
    return page(content)