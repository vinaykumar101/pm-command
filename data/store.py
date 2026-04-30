import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(
    __file__)), "migrations", "pm_command_center.db")


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def query_all(table, order_by=None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table}"
        if order_by:
            query += f" ORDER BY {order_by}"
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]


def query_one(table, where, params):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE {where}", params)
        row = cursor.fetchone()
        return dict(row) if row else None


def insert(table, data):
    with get_db() as conn:
        cursor = conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({
                       placeholders})", list(data.values()))
        conn.commit()
        return cursor.lastrowid


def update(table, data, where, params):
    with get_db() as conn:
        cursor = conn.cursor()
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        cursor.execute(f"UPDATE {table} SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE {
                       where}", list(data.values()) + list(params))
        conn.commit()
        return cursor.rowcount


def delete(table, where, params):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE {where}", params)
        conn.commit()
        return cursor.rowcount


# Clients
def get_clients():
    return query_all("clients")


def get_client(id):
    return query_one("clients", "id = ?", (id,))


def add_client(data):
    return insert("clients", data)


# Projects
def get_projects():
    return query_all("projects")


def get_project(id):
    return query_one("projects", "id = ?", (id,))


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
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT stage_name, user_count FROM funnel_stages ORDER BY display_order")
        return [(row[0], row[1]) for row in cursor.fetchall()]


# Cohorts
def get_cohorts():
    return query_all("cohorts", "cohort_date")


# Reports
def get_reports():
    return query_all("reports")
