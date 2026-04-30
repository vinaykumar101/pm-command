clients = [
    {"name": "DeHaat", "industry": "AgriTech", "contact": "Nikhil", "email": "nikhil@example.om", "phone": "99999999999", "type": "Enterprise",
        "priority": "High", "engagement": "SaaS", "contract": "Active", "start": "2026-04-01", "notes": "Field app and analytics dashboards"},
    {"name": "Govt. Program", "industry": "Public Sector", "contact": "Program Officer", "email": "officer@example.gov", "phone": "88888888888", "type": "Government",
        "priority": "High", "engagement": "Dashboard", "contract": "Signed", "start": "2026-04-08", "notes": "Cluster and farmer lifecycle reporting"},
    {"name": "FreshFoods", "industry": "FMCG", "contact": "Operations Head", "email": "ops@freshfoods.om", "phone": "77777777777", "type": "Partner",
        "priority": "Medium", "engagement": "Integration", "contract": "In Discussion", "start": "2026-04-15", "notes": "Procurement workflow and traceability"},
]

projects = [
    {"name": "AgriPulse 2.0", "client": "DeHaat", "type": "Mobile App", "problem": "Field workflows are fragmented", "objective": "Create offline-first field execution app", "users": "FSP, TOM, Admin",
        "metrics": "Onboarding %, attendance compliance", "owner": "Saksham", "tech": "Kshitij", "qa": "Sampada", "start": "2026-04-01", "release": "2026-05-15", "status": "Development", "priority": "High", "risk": "Medium"},
    {"name": "DigiAcre 2.0", "client": "DeHaat", "type": "Dashboard", "problem": "Reports lack role-based visibility", "objective": "Create RBAC reporting hub", "users": "Admin, TOM, IVR Manager",
        "metrics": "Report usage, access accuracy", "owner": "Saksham", "tech": "Tech Team", "qa": "QA Team", "start": "2026-04-05", "release": "2026-05-30", "status": "Design", "priority": "High", "risk": "High"},
    {"name": "Cluster Monitoring", "client": "Govt. Program", "type": "Data Product", "problem": "Manual progress tracking", "objective": "Automated farmer and activity reporting", "users": "PMU, Govt Officers",
        "metrics": "Data completeness, dashboard refresh", "owner": "Product Team", "tech": "BI Team", "qa": "Data QA", "start": "2026-04-10", "release": "2026-06-01", "status": "Requirement Gathering", "priority": "Medium", "risk": "Medium"},
    {"name": "Traceability API", "client": "FreshFoods", "type": "API", "problem": "Buyer needs farm-to-procurement traceability", "objective": "Expose traceability data through API", "users": "Buyer Ops, Internal Ops",
        "metrics": "API uptime, matched lots", "owner": "Platform PM", "tech": "Backend Team", "qa": "QA Team", "start": "2026-04-20", "release": "2026-06-15", "status": "Discovery", "priority": "Medium", "risk": "Low"},
]

requirements = [
    {"title": "Mandatory attendance before task", "client": "DeHaat", "project": "AgriPulse 2.0", "type": "Feature", "source": "UAT", "description": "FSP must check- in before any task",
        "need": "Improve field discipline", "problem": "Tasks are done without attendance", "outcome": "Attendance- linked task execution", "priority": "P0", "status": "Approved", "by": "Operations", "date": "2026-04-17"},
    {"title": "Transfer farmers between FSPs", "client": "DeHaat", "project": "DigiAcre 2.0", "type": "Feature", "source": "Internal Team", "description": "Admin can transfer farmers from one FSP to another",
        "need": "Correct mapping", "problem": "Manual reassignment is slow", "outcome": "Clean farmer-agent mapping", "priority": "P1", "status": "Under Review", "by": "Ops Team", "date": "2026-04-20"},
    {"title": "Data validation tracker", "client": "Govt. Program", "project": "Cluster Monitoring", "type": "Data Requirement", "source": "Leadership", "description": "Track report mismatches",
        "need": "Improve data trust", "problem": "Manual validation gaps", "outcome": "Resolved data issues", "priority": "P1", "status": "New", "by": "PMO", "date": "2026-04-21"},
]

prds = [
    {"title": "AgriPulse Attendance Control", "client": "DeHaat", "project": "AgriPulse 2.0", "background": "Attendance flow required for task discipline", "problem": "Users can perform work without check-in", "objective": "Block task activity without attendance", "users": "FSP, TOM", "personas": "Field agent, manager", "current": "Open task access", "solution": "Attendance gate before task flow", "journey": "Login > Check- in > Task", "functional": "Check-in validation before task",
        "nonfunctional": "Fast and offline-aware", "rbac": "FSP enforced, Admin override", "api": "Attendance status API", "data": "Check-in timestamp and task logs", "edge": "Offline, device time mismatch", "acceptance": "Task blocked if not checked-in", "dependencies": "Attendance API", "risks": "Offline sync conflict", "metrics": "Attendance compliance", "outscope": "Payroll logic", "release_plan": "Sprint 1", "uat_plan": "Field UAT", "questions": "Device time validation", "status": "Approved"},
]

tasks = [
    {"title": "Create attendance gate API", "client": "DeHaat", "project": "AgriPulse 2.0", "prd": "AgriPulse Attendance Control", "type": "API", "description": "Return active attendance status",
        "acceptance": "API returns checked-in true/false", "assigned": "Backend Team", "priority": "P0", "status": "In Progress", "sprint": "Sprint 1", "due": "2026-05-02", "estimate": "2d", "actual": "1d"},
    {"title": "Update Home UI", "client": "DeHaat", "project": "AgriPulse 2.0", "prd": "AgriPulse Attendance Control", "type": "UI", "description": "Align home with Figma",
        "acceptance": "UI matches approved design", "assigned": "Frontend Team", "priority": "P1", "status": "QA", "sprint": "Sprint 1", "due": "2026-05-05", "estimate": "3d", "actual": "3d"},
    {"title": "Create farmer transfer flow", "client": "DeHaat", "project": "DigiAcre 2.0", "prd": "Farmer Transfer", "type": "Feature", "description": "Admin selects old FSP, new FSP and farmers",
        "acceptance": "Selected farmers move to new FSP", "assigned": "Fullstack Team", "priority": "P1", "status": "Backlog", "sprint": "Sprint 2", "due": "2026-05-12", "estimate": "4d", "actual": "-"},
    {"title": "Validate cohort data", "client": "Govt. Program", "project": "Cluster Monitoring", "prd": "Analytics", "type": "Data", "description": "Check retention values",
        "acceptance": "No null cohort rows", "assigned": "Data QA", "priority": "P2", "status": "To Do", "sprint": "Sprint 2", "due": "2026-05-10", "estimate": "1d", "actual": "-"},
]

bugs = [
    {"title": "Image upload fails on weak network", "description": "Check-in image upload fails", "steps": "Go offline/weak network > upload image", "expected": "Image retries",
        "actual": "Upload failed", "severity": "High", "priority": "P1", "assigned": "Mobile Team", "status": "Open", "env": "UAT", "by": "QA", "date": "2026-04-18"},
    {"title": "Wrong age calculation", "description": "DOB- based age mismatch", "steps": "Open agent profile", "expected": "Correct age", "actual": "Age blank",
        "severity": "Medium", "priority": "P2", "assigned": "Frontend Team", "status": "In Progress", "env": "Dev", "by": "Saksham", "date": "2026-04-19"},
]

uat_cases = [
    {"name": "Login OTP", "module": "Auth", "feature": "OTP auto-fetch", "expected": "OTP auto-detected", "actual": "Works",
        "status": "Pass", "severity": "Low", "tester": "Sampada", "date": "2026-04-17", "remarks": "OK", "task": "Login", "prd": "Auth"},
    {"name": "Offline onboarding", "module": "Farmer", "feature": "Quick onboarding", "expected": "Draft saved offline", "actual": "Saved", "status": "Pass",
        "severity": "Medium", "tester": "QA", "date": "2026-04-17", "remarks": "Needs sync validation", "task": "Onboarding", "prd": "Farmer Onboarding"},
    {"name": "Check-in image", "module": "Attendance", "feature": "Image upload", "expected": "Upload success", "actual": "Failed on weak network",
        "status": "Fail", "severity": "High", "tester": "QA", "date": "2026-04-17", "remarks": "Bug raised", "task": "Attendance", "prd": "Attendance"},
]

validation_issues = [
    {"title": "Dashboard count mismatch", "client": "DeHaat", "project": "DigiAcre 2.0", "source": "Metabase", "table": "farmer_program", "description": "Active farmer count mismatch",
        "expected": "10,000", "actual": "9,742", "severity": "High", "owner": "Data Team", "status": "Open", "date": "2026-04-22", "notes": "Check duplicate filters"},
    {"title": "Missing district filter values", "client": "Govt. Program", "project": "Cluster Monitoring", "source": "Tableau", "table": "district dimension", "description": "Empty districts showing",
        "expected": "Only districts with data", "actual": "All districts", "severity": "Medium", "owner": "BI Team", "status": "In Progress", "date": "2026-04-23", "notes": "Filter data source"},
]

releases = [
    {"name": "AgriPulse UAT Build", "version": "v0.9.1", "client": "DeHaat", "project": "AgriPulse 2.0", "date": "2026-04-17", "type": "Minor", "features": "Attendance, onboarding, KPI",
        "bugs": "Login fixes", "known": "Image upload weak network", "deployment": "Deployed", "uat": "Pending", "approval": "Pending", "notes": "Shared for selected user acceptance"},
    {"name": "DigiAcre RBAC Alpha", "version": "v0.5.0", "client": "DeHaat", "project": "DigiAcre 2.0", "date": "2026-05-05", "type": "Major", "features": "Role-based dashboards",
        "bugs": "-", "known": "Report latency", "deployment": "Planned", "uat": "Pending", "approval": "Pending", "notes": "Internal testing planned"},
]

meetings = [
    {"title": "UAT Readiness Review", "client": "DeHaat", "project": "AgriPulse 2.0", "date": "2026-04-17", "attendees": "Product, Tech, QA", "points": "Module readiness and defects",
        "decisions": "Share build with selected users", "actions": "Close P0 bugs", "owner": "Product", "due": "2026-04-22", "status": "Closed"},
]

metrics = [
    {"name": "DAU", "current": "1,240", "target": "1,500",
        "status": "Amber", "trend": "Up"},
    {"name": "WAU", "current": "5,980", "target": "6,500",
        "status": "Amber", "trend": "Up"},
    {"name": "MAU", "current": "18,400", "target": "20,000",
        "status": "Amber", "trend": "Stable"},
    {"name": "Activation Rate", "current": "62%",
        "target": "70%", "status": "Amber", "trend": "Up"},
    {"name": "Retention Rate", "current": "54%",
        "target": "60%", "status": "Amber", "trend": "Stable"},
    {"name": "Churn Rate", "current": "8%",
        "target": "5%", "status": "Red", "trend": "Down"},
    {"name": "Feature Adoption", "current": "71%",
        "target": "75%", "status": "Green", "trend": "Up"},
    {"name": "Task Completion", "current": "84%",
        "target": "90%", "status": "Amber", "trend": "Up"},
    {"name": "Error Rate", "current": "3.2%",
        "target": "1%", "status": "Red", "trend": "Down"},
    {"name": "UAT Pass %", "current": "67%",
        "target": "90%", "status": "Red", "trend": "Stable"},
]

funnel = [
    ("User Registered", 10000),
    ("Profile Completed", 8200),
    ("First Action Performed", 6100),
    ("Feature Used", 4700),
    ("Task Completed", 3900),
    ("Activated", 2800),
]

cohorts = [
    ["2026-04-01", "100%", "78%", "61%", "52%", "44%", "36%", "29%"],
    ["2026-04-08", "100%", "82%", "64%", "55%", "46%", "38%", "-"],
    ["2026-04-15", "100%", "75%", "58%", "49%", "-", "-", "-"],
    ["2026-04-22", "100%", "69%", "-", "-", "-", "-", "-"],
]

reports = [
    ("Client-wise Project Status Report", "Shows project progress by client", "2026-04-25"),
    ("PRD Progress Report", "Tracks PRDs by status", "2026-04-24"),
    ("Task Completion Report", "Sprint and owner-wise task completion", "2026-04-24"),
    ("Funnel Drop-off Report", "Stage-wise funnel drop-off", "2026-04-23"),
    ("Cohort Retention Report", "Retention cohort performance", "2026-04-23"),
    ("Data Validation Report", "Open and resolved data issues", "2026-04-22"),
    ("Release Readiness Report", "UAT, bugs and deployment readiness", "2026-04-21"),
]