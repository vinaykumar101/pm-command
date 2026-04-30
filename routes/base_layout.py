from flask import render_template_string

BASE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PM Command Center</title>
<style>
    :root{--bg:#f5f7fb;--card:#fff;--text:#111827;--muted:#6b7280;--line:#e5e7eb;--primary:#2563eb;--shadow:0 12px 30px rgba(15,23,42,.08);--danger:#fee2e2;--danger-text:#991b1b;--warning:#fef3c7;--warning-text:#92400e;--success:#dcfce7;--success-text:#166534;--neutral:#e5e7eb;--neutral-text:#374151;}
    *{box-sizing:border-box}
    body{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:var(--bg);color:var(--text)}
    a{text-decoration:none;color:inherit}
    .app{display:flex;min-height:100vh}
    .sidebar{width:260px;background:#0f172a;color:#e5e7eb;position:fixed;left:0;top:0;bottom:0;padding:22px 16px;overflow:auto}
    .brand{font-size:22px;font-weight:800;margin-bottom:6px;color:#fff}.brand small{display:block;font-size:12px;color:#94a3b8;font-weight:500;margin-top:5px}
    .nav{margin-top:22px}.nav a{display:block;padding:11px 12px;margin:4px 0;border-radius:12px;color:#cbd5e1;font-size:14px}.nav a:hover,.nav a.active{background:#1e293b;color:#fff}
    .main{margin-left:260px;width:calc(100% - 260px);padding:24px}
    .topbar{display:flex;gap:16px;align-items:center;justify-content:space-between;margin-bottom:22px}
    .search{flex:1;max-width:520px}.search input{width:100%;padding:13px 16px;border:1px solid var(--line);border-radius:16px;background:#fff;outline:none}
    .rolebox{display:flex;gap:10px;align-items:center;background:#fff;border:1px solid var(--line);padding:9px 12px;border-radius:16px;box-shadow:0 6px 16px rgba(15,23,42,.04)}
    select,input,textarea{border:1px solid var(--line);border-radius:12px;padding:10px 12px;background:#fff;width:100%;font-family:inherit}textarea{min-height:90px;resize:vertical}
    button,.btn{background:var(--primary);color:#fff;border:none;border-radius:12px;padding:10px 14px;cursor:pointer;font-weight:700;display:inline-block}.btn.secondary{background:#111827}.btn.light{background:#eef2ff;color:#1d4ed8}
    h1{font-size:28px;margin:0 0 6px}.subtitle{color:var(--muted);margin:0 0 22px}
    .grid{display:grid;gap:16px}.cards{grid-template-columns:repeat(4,minmax(0,1fr))}.two{grid-template-columns:repeat(2,minmax(0,1fr))}.three{grid-template-columns:repeat(3,minmax(0,1fr))}
    .card{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:18px;box-shadow:var(--shadow)}
    .metric-value{font-size:28px;font-weight:800;margin-top:8px}.muted{color:var(--muted)}
    .badge{display:inline-flex;align-items:center;border-radius:999px;padding:5px 10px;font-size:12px;font-weight:800;white-space:nowrap}.danger{background:var(--danger);color:var(--danger-text)}.warning{background:var(--warning);color:var(--warning-text)}.success{background:var(--success);color:var(--success-text)}.neutral{background:var(--neutral);color:var(--neutral-text)}
    table{width:100%;border-collapse:collapse;background:#fff;border-radius:18px;overflow:hidden}th,td{padding:13px 12px;border-bottom:1px solid var(--line);text-align:left;font-size:14px;vertical-align:top}th{background:#f8fafc;color:#475569;font-size:12px;text-transform:uppercase;letter-spacing:.04em}tr:last-child td{border-bottom:none}
    .form-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.form-grid .wide{grid-column:1/-1}.form-section{margin-bottom:20px}
    .kanban{display:grid;grid-template-columns:repeat(4,minmax(240px,1fr));gap:14px;overflow:auto}.kanban-col{background:#f8fafc;border:1px solid var(--line);border-radius:18px;padding:12px;min-height:220px}.task-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:12px;margin:10px 0;box-shadow:0 6px 14px rgba(15,23,42,.05)}
    .bar{height:12px;background:#e5e7eb;border-radius:999px;overflow:hidden}.bar span{display:block;height:100%;background:var(--primary);border-radius:999px}.funnel-row{display:grid;grid-template-columns:220px 1fr 110px 110px;gap:12px;align-items:center;margin:14px 0}
    .heat{font-weight:800;text-align:center;border-radius:10px}.h100{background:#14532d;color:#fff}.h80{background:#16a34a;color:#fff}.h60{background:#86efac;color:#064e3b}.h40{background:#fef08a;color:#713f12}.h20{background:#fecaca;color:#7f1d1d}
    .report-card{display:flex;justify-content:space-between;gap:12px;align-items:center}.actions{display:flex;gap:8px;flex-wrap:wrap}.section-title{font-size:18px;font-weight:800;margin:0 0 14px}
    @media(max-width:1100px){.cards,.three,.two,.form-grid{grid-template-columns:1fr 1fr}.kanban{grid-template-columns:repeat(2,minmax(240px,1fr))}}
    @media(max-width:800px){.sidebar{position:relative;width:100%;height:auto}.main{margin-left:0;width:100%}.app{display:block}.cards,.three,.two,.form-grid{grid-template-columns:1fr}.topbar{flex-direction:column;align-items:stretch}.kanban{grid-template-columns:1fr}.funnel-row{grid-template-columns:1fr}}}
</style>
</head>
<body>
<div class="app">
    <aside class="sidebar">
        <div class="brand">PM Command Center<small>Product Manager Workspace</small></div>
        <nav class="nav">
            {% for endpoint, label in NAV %}
            <a class="{{ 'active' if request.endpoint == endpoint else '' }}" href="{{ url_for(endpoint) }}">{{ label }}</a>
            {% endfor %}
        </nav>
    </aside>
    <main class="main">
        <div class="topbar">
            <div class="search"><input placeholder="Search clients, projects, PRDs, tasks, bugs..."></div>
            <form class="rolebox" method="post" action="{{ url_for('set_role') }}">
                <span class="muted">Role</span>
                <select name="role" onchange="this.form.submit()">
                    {% for r in ROLES %}
                    <option value="{{r}}" {{ 'selected' if role==r else '' }}>{{r}}</option>
                    {% endfor %}
                </select>
            </form>
        </div>
        {{ content|safe }}
    </main>
</div>
</body>
</html>"""