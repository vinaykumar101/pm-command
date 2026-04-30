import os
import libsql

TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

# Use synchronous libsql client
def get_db():
    return libsql.connect(
        database=TURSO_DATABASE_URL,
        auth_token=TURSO_AUTH_TOKEN
    )


def query_all(table, order_by=None):
    client = get_db()
    query = f"SELECT * FROM {table}"
    if order_by:
        query += f" ORDER BY {order_by}"
    result = client.execute(query)
    rows = result.fetchall()
    if not rows:
        return []
    # Get column names from description
    columns = [desc[0] for desc in result.description] if result.description else list(range(len(rows[0])))
    return [dict(zip(columns, row)) for row in rows]


def query_one(table, where, params):
    client = get_db()
    result = client.execute(f"SELECT * FROM {table} WHERE {where}", params)
    row = result.fetchone()
    if not row:
        return None
    columns = [desc[0] for desc in result.description] if result.description else list(range(len(row)))
    return dict(zip(columns, row))


def insert(table, data):
    client = get_db()
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    client.execute(
        f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
        list(data.values())
    )
    client.commit()
    return client.execute("SELECT last_insert_rowid()").fetchone()[0]


# Clients
def get_clients():
    return query_all("clients")

def add_client(data):
    return insert("clients", data)


# Projects
def get_projects():
    return query_all("projects")

def add_project(data):
    return insert("projects", data)


# Requirements
def get_requirements():
    return query_all("requirements")

def add_requirement(data):
    return insert("requirements", data)


# PRDs
def get_prds():
    return query_all("prds")

def add_prd(data):
    return insert("prds", data)


# Tasks
def get_tasks():
    return query_all("tasks")

def add_task(data):
    return insert("tasks", data)


# Bugs
def get_bugs():
    return query_all("bugs")

def add_bug(data):
    return insert("bugs", data)


# UAT Cases
def get_uat_cases():
    return query_all("uat_cases")

def add_uat_case(data):
    return insert("uat_cases", data)


# Validation Issues
def get_validation_issues():
    return query_all("validation_issues")

def add_validation_issue(data):
    return insert("validation_issues", data)


# Releases
def get_releases():
    return query_all("releases")

def add_release(data):
    return insert("releases", data)


# Meetings
def get_meetings():
    return query_all("meetings")

def add_meeting(data):
    return insert("meetings", data)


# Metrics
def get_metrics():
    return query_all("metrics")

def add_metric(data):
    return insert("metrics", data)


# Funnel
def get_funnel():
    client = get_db()
    result = client.execute("SELECT stage_name, user_count FROM funnel_stages ORDER BY display_order")
    rows = result.fetchall()
    return [(row[0], row[1]) for row in rows] if rows else []


# Cohorts
def get_cohorts():
    return query_all("cohorts", "cohort_date")


# Reports
def get_reports():
    return query_all("reports")
