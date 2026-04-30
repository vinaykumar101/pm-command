-- PM Command Center Database Schema
-- SQLite Migration: Create Tables

-- Clients table
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    industry TEXT,
    contact TEXT,
    email TEXT,
    phone TEXT,
    type TEXT,
    priority TEXT,
    engagement TEXT,
    contract TEXT,
    start_date TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Projects table (linked to clients)
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    client_id INTEGER,
    type TEXT,
    problem TEXT,
    objective TEXT,
    users TEXT,
    metrics TEXT,
    owner TEXT,
    tech_owner TEXT,
    qa_owner TEXT,
    start_date TEXT,
    release_date TEXT,
    status TEXT,
    priority TEXT,
    risk TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Requirements table (linked to projects)
CREATE TABLE IF NOT EXISTS requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    client_id INTEGER,
    project_id INTEGER,
    type TEXT,
    source TEXT,
    description TEXT,
    need TEXT,
    problem TEXT,
    outcome TEXT,
    priority TEXT,
    status TEXT,
    requested_by TEXT,
    request_date TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- PRDs table (linked to projects)
CREATE TABLE IF NOT EXISTS prds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    client_id INTEGER,
    project_id INTEGER,
    background TEXT,
    problem TEXT,
    objective TEXT,
    users TEXT,
    personas TEXT,
    current_process TEXT,
    solution TEXT,
    journey TEXT,
    functional_req TEXT,
    nonfunctional_req TEXT,
    rbac TEXT,
    api_req TEXT,
    data_req TEXT,
    edge_cases TEXT,
    acceptance_criteria TEXT,
    dependencies TEXT,
    risks TEXT,
    metrics TEXT,
    outscope TEXT,
    release_plan TEXT,
    uat_plan TEXT,
    questions TEXT,
    status TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Tasks table (linked to projects and PRDs)
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    client_id INTEGER,
    project_id INTEGER,
    prd_id INTEGER,
    type TEXT,
    description TEXT,
    acceptance_criteria TEXT,
    assigned_to TEXT,
    priority TEXT,
    status TEXT,
    sprint TEXT,
    due_date TEXT,
    estimate TEXT,
    actual_effort TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (prd_id) REFERENCES prds(id)
);

-- Bugs table
CREATE TABLE IF NOT EXISTS bugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    steps_to_reproduce TEXT,
    expected_result TEXT,
    actual_result TEXT,
    severity TEXT,
    priority TEXT,
    assigned_to TEXT,
    status TEXT,
    environment TEXT,
    reported_by TEXT,
    reported_date TEXT,
    project_id INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- UAT Cases table (linked to tasks)
CREATE TABLE IF NOT EXISTS uat_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    module TEXT,
    feature TEXT,
    expected_result TEXT,
    actual_result TEXT,
    status TEXT,
    severity TEXT,
    tester TEXT,
    test_date TEXT,
    remarks TEXT,
    task_id INTEGER,
    prd_link TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

-- Validation Issues table (linked to projects)
CREATE TABLE IF NOT EXISTS validation_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    client_id INTEGER,
    project_id INTEGER,
    source TEXT,
    table_name TEXT,
    description TEXT,
    expected_data TEXT,
    actual_data TEXT,
    severity TEXT,
    owner TEXT,
    status TEXT,
    identified_date TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Releases table (linked to projects)
CREATE TABLE IF NOT EXISTS releases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    version TEXT,
    client_id INTEGER,
    project_id INTEGER,
    release_date TEXT,
    release_type TEXT,
    features TEXT,
    bugs_fixed TEXT,
    known_issues TEXT,
    deployment_status TEXT,
    uat_status TEXT,
    approval_status TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Meetings table (linked to projects)
CREATE TABLE IF NOT EXISTS meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    client_id INTEGER,
    project_id INTEGER,
    meeting_date TEXT,
    attendees TEXT,
    discussion_points TEXT,
    decisions TEXT,
    action_items TEXT,
    owner TEXT,
    due_date TEXT,
    status TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Product Metrics table
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    current_value TEXT,
    target_value TEXT,
    status TEXT,
    trend TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Funnel Stages table
CREATE TABLE IF NOT EXISTS funnel_stages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage_name TEXT NOT NULL,
    user_count INTEGER NOT NULL,
    display_order INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Cohort Retention table
CREATE TABLE IF NOT EXISTS cohorts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cohort_date TEXT NOT NULL,
    day0 TEXT,
    day1 TEXT,
    day7 TEXT,
    day14 TEXT,
    day30 TEXT,
    day60 TEXT,
    day90 TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    last_updated TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);