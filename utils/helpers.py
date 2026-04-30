def badge_class(value):
    v = str(value).lower()
    if v in ["high", "critical", "p0", "red", "fail", "open", "blocked"]:
        return "danger"
    if v in ["medium", "p1", "p2", "amber", "pending", "in progress", "under review", "uat", "qa"]:
        return "warning"
    if v in ["low", "p3", "green", "pass", "approved", "done", "closed", "released", "deployed", "active", "signed"]:
        return "success"
    return "neutral"