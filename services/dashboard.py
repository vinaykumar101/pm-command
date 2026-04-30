def dashboard_stats(clients, projects, prds, tasks, bugs, uat_cases, releases, validation_issues, funnel):
    from collections import Counter

    task_counts = Counter(t['status'] for t in tasks)
    bug_counts = Counter(b['severity'] for b in bugs)
    project_counts = Counter(p['status'] for p in projects)
    uat_pending = sum(1 for u in uat_cases if u['status'] != 'Pass')

    return {
        "cards": [
            ("Total Clients", len(clients)),
            ("Active Projects", len(projects)),
            ("PRDs Created", len(prds)),
            ("Pending Tasks", task_counts.get('To Do', 0) + task_counts.get('Backlog', 0)),
            ("Tasks In Progress", task_counts.get('In Progress', 0)),
            ("Tasks Completed", task_counts.get('Done', 0)),
            ("Open Bugs", sum(1 for b in bugs if b['status'] != 'Closed')),
            ("UAT Pending", uat_pending),
            ("Data Validation Issues", len(validation_issues)),
            ("Upcoming Releases", sum(1 for r in releases if r['deployment'] != 'Deployed')),
            ("Product Health Score", "72%"),
        ],
        "project_counts": dict(project_counts),
        "task_counts": dict(task_counts),
        "bug_counts": dict(bug_counts),
        "funnel": funnel,
        "uat_pending": uat_pending,
    }


def funnel_analysis(funnel_data):
    first = funnel_data[0][1]
    drops = [(funnel_data[i][0], funnel_data[i-1][1] - funnel_data[i][1]) for i in range(1, len(funnel_data))]
    biggest = max(drops, key=lambda x: x[1])
    overall_conversion = round(funnel_data[-1][1] / first * 100)
    return {
        "first": first,
        "biggest": biggest,
        "overall_conversion": overall_conversion,
    }


def uat_stats(uat_cases):
    total = len(uat_cases)
    passed = sum(1 for u in uat_cases if u['status'] == 'Pass')
    pass_rate = round(passed / total * 100) if total else 0
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": pass_rate,
    }