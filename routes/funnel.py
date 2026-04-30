from flask import Blueprint, render_template_string
from data.store import funnel
from services.dashboard import funnel_analysis
from routes.layout import page
from utils.helpers import badge_class

funnel_bp = Blueprint("funnel", __name__, url_prefix="/funnel")


@funnel_bp.route("")
def funnel_page():
    result = funnel_analysis(funnel)
    content = render_template_string(
        """<h1>Funnel Analysis</h1><p class="subtitle">Track conversion and drop-off across product activation stages.</p>
<div class="card"><div class="section-title">Activation Funnel</div>{% for name,num in funnel %}{% set conv = (num/first*100)|round %}<div class="funnel-row"><b>{{name}}</b><div class="bar"><span style="width:{{conv}}%"></span></div><span>{{num}} users</span><span>{{conv}}%</span></div>{% endfor %}</div>
<div class="grid three" style="margin-top:18px"><div class="card"><div class="muted">Overall Conversion</div><div class="metric-value">{{ overall_conversion }}%</div></div><div class="card"><div class="muted">Biggest Drop-off</div><div class="metric-value">{{ biggest[0] }}</div><p class="muted">{{ biggest[1] }} users lost</p></div><div class="card"><div class="muted">Funnel Health</div><div class="metric-value"><span class="badge warning">Amber</span></div></div></div>""",
        funnel=funnel, badge_class=badge_class, **result,
    )
    return page(content)