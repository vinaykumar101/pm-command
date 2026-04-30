from flask import Flask, request, redirect, url_for, session
from utils.helpers import badge_class
from routes. layout import page as render_page, NAV, ROLES
from routes. dashboard import dashboard_bp
from routes. clients import clients_bp
from routes. projects import projects_bp
from routes. requirements import requirements_bp
from routes. prds import prds_bp
from routes. tasks import tasks_bp
from routes. funnel import funnel_bp
from routes. cohort import cohort_bp
from routes. metrics import metrics_bp
from routes. validation import validation_bp
from routes. uat import uat_bp
from routes. bugs import bugs_bp
from routes. releases import releases_bp
from routes. meetings import meetings_bp
from routes. reports import reports_bp
from routes. settings import settings_bp

app = Flask(__name__)
app.secret_key = "pm-command-center-demo-key"

app.jinja_env.globals["badge_class"] = badge_class
app.jinja_env.globals["NAV"] = NAV


@app.context_processor
def inject_helpers():
    return dict(badge_class=badge_class, role=session.get("role", "Product Manager"))


@app.route("/set-role", methods=["POST"])
def set_role():
    session["role"] = request.form.get("role", "Product Manager")
    return redirect(request.referrer or url_for("dashboard.dashboard"))


app.register_blueprint(dashboard_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(requirements_bp)
app.register_blueprint(prds_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(funnel_bp)
app.register_blueprint(cohort_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(validation_bp)
app.register_blueprint(uat_bp)
app.register_blueprint(bugs_bp)
app.register_blueprint(releases_bp)
app.register_blueprint(meetings_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(settings_bp)


if __name__ == "__main__":
    app.run(debug=True)