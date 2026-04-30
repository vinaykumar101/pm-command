from flask import Blueprint, render_template_string
from data.store import cohorts
from routes.layout import page
from utils.helpers import badge_class

cohort_bp = Blueprint("cohort", __name__, url_prefix="/cohort")


@cohort_bp.route("")
def cohort_page():
    content = render_template_string(
        """<h1>Cohort Analysis</h1><p class="subtitle">Retention view by signup or activation cohort.</p>
<div class="card"><table><tr><th>Cohort Start Date</th><th>Day 0</th><th>Day 1</th><th>Day 7</th><th>Day 14</th><th>Day 30</th><th>Day 60</th><th>Day 90</th></tr>{% for row in cohorts %}<tr>{% for cell in row %}{% if loop.first %}<td><b>{{cell}}</b></td>{% else %}{% set n = cell.replace('%','')|int if cell!='-' else 0 %}<td class="heat {{ 'h100' if n>=95 else 'h80' if n>=75 else 'h60' if n>=55 else 'h40' if n>=35 else 'h20' if n>0 else '' }}">{{cell}}</td>{% endif %}{% endfor %}</tr>{% endfor %}</table></div>""",
        cohorts=cohorts, badge_class=badge_class,
    )
    return page(content)