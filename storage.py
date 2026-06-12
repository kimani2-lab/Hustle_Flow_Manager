import json
import os

from models import User, Project, Task

DB_FILENAME = os.path.join(os.path.dirname(__file__), "data", "db.json")


def ensure_db_file(db_file=DB_FILENAME):
    directory = os.path.dirname(db_file)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(db_file) or os.path.getsize(db_file) == 0:
        with open(db_file, "w", encoding="utf-8") as f:
            json.dump({"users": [], "projects": []}, f, indent=4)


def load_data(db_file=DB_FILENAME):
    """Load users and projects from the JSON database file."""
    ensure_db_file(db_file)
    with open(db_file, "r", encoding="utf-8") as f:
        payload = json.load(f)

    users = []
    projects = []

    for u_data in payload.get("users", []):
        user = User(u_data["name"], u_data["email"], u_data.get("role", "Fundi"))
        user.id = u_data["id"]
        users.append(user)
        User._id_counter = max(User._id_counter, user.id + 1)

    for p_data in payload.get("projects", []):
        project = Project(p_data["title"], p_data.get("description", ""), p_data["manager_id"])
        project.id = p_data["id"]
        Project._id_counter = max(Project._id_counter, project.id + 1)

        for t_data in p_data.get("tasks", []):
            task = Task(t_data["title"], t_data["pay_amount"], t_data.get("status", "Pending"))
            task.id = t_data["id"]
            task.contributors = t_data.get("contributors", [])
            Task._id_counter = max(Task._id_counter, task.id + 1)
            project.tasks.append(task)

        projects.append(project)

    for project in projects:
        manager = next((u for u in users if u.id == project.manager_id), None)
        if manager:
            manager.projects.append(project)

    return users, projects


def save_data(users, projects, db_file=DB_FILENAME):
    """Serialize the current state of users and projects to the JSON database file."""
    ensure_db_file(db_file)
    data = {
        "users": [user.to_dict() for user in users],
        "projects": [project.to_dict() for project in projects],
    }
    with open(db_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
