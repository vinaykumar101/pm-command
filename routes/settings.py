from flask import Blueprint, render_template_string
from routes.layout import page
from utils.helpers import badge_class

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("")
def settings_page():
    content = render_template_string(
        """<h1>Settings</h1><p class="subtitle">Prototype settings for profile, roles and configurations.</p>
<div class="grid two"><div class="card"><div class="section-title">User Profile</div><input placeholder="Name" value="Product Manager"><br><br><input placeholder="Email" value="pm@example.com"><br><br><button>Save Profile</button></div><div class="card"><div class="section-title">Configuration</div><p>Status Configuration</p><p>Priority Configuration</p><p>Metric Configuration</p><p>Notification Preferences</p><span class="badge neutral">Placeholder settings</span></div><div class="card"><div class="section-title">Role Permissions</div><table><tr><th>Role</th><th>Permission</th></tr><tr><td>Admin</td><td>Full access</td></tr><tr><td>Product Manager</td><td>Create and edit all product modules</td></tr><tr><td>QA</td><td>Update UAT and bugs</td></tr><tr><td>Client Viewer</td><td>View approved dashboard and reports</td></tr></table></div></div>""",
        badge_class=badge_class,
    )
    return page(content)