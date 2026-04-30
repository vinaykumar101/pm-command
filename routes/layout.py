from flask import render_template_string, session
from routes.base_layout import BASE

NAV = [
    ("dashboard.dashboard", "Dashboard"),
    ("clients.clients_page", "Clients"),
    ("projects.projects_page", "Projects"),
    ("requirements.requirements_page", "Requirements"),
    ("prds.prds_page", "PRDs"),
    ("tasks.tasks_page", "Tasks"),
    ("funnel.funnel_page", "Funnel Analysis"),
    ("cohort.cohort_page", "Cohort Analysis"),
    ("metrics.metrics_page", "Product Metrics"),
    ("validation.validation_page", "Data Validation"),
    ("uat.uat_page", "UAT"),
    ("bugs.bugs_page", "Bugs"),
    ("releases.releases_page", "Releases"),
    ("meetings.meetings_page", "Meetings"),
    ("reports.reports_page", "Reports"),
    ("settings.settings_page", "Settings"),
]
ROLES = ["Admin", "Product Manager", "Tech Lead", "Designer", "QA", "Business User", "Client Viewer"]


def page(content, role=None):
    if role is None:
        role = session.get("role", "Product Manager")
    return render_template_string(BASE, content=content, NAV=NAV, ROLES=ROLES, role=role)