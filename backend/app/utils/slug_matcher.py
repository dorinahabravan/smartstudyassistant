# Maps user input to GitHub roadmap slugs
ROADMAP_MATCHES = {
    "frontend": "frontend-developer",
    "frontend developer": "frontend-developer",
    "backend": "backend-developer",
    "backend developer": "backend-developer",
    "devops": "devops",
    "qa": "qa",
    "python": "python-developer",
    "python developer": "python-developer",
    "react": "react",
    "react developer": "react",
    "vue": "vue",
    "vue developer": "vue",
    "ai": "ai",
    "ai engineer": "ai",
    "cyber security": "cyber-security",
    "docker": "docker",
    "node": "nodejs",
    "nodejs": "nodejs"
}


def match_goal_to_slug(goal: str) -> str | None:
    goal = goal.strip().lower()
    return ROADMAP_MATCHES.get(goal)
