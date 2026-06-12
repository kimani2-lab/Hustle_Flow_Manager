import json
from pathlib import Path

from models import User, Project, Task
from storage import load_data, save_data


def setup_function():
    User._id_counter = 1
    Project._id_counter = 1
    Task._id_counter = 1


def test_save_and_load_data(tmp_path):
    db_file = tmp_path / "db.json"

    users = [User("Alice", "alice@example.com", "Client")]
    projects = [Project("Renovation", "Home renovation project.", users[0].id)]
    users[0].projects.append(projects[0])
    projects[0].tasks.append(Task("Install plumbing", "3000"))

    save_data(users, projects, db_file=str(db_file))
    loaded_users, loaded_projects = load_data(db_file=str(db_file))

    assert len(loaded_users) == 1
    assert loaded_users[0].name == "Alice"
    assert len(loaded_projects) == 1
    assert loaded_projects[0].title == "Renovation"
    assert len(loaded_projects[0].tasks) == 1
    assert loaded_projects[0].tasks[0].title == "Install plumbing"

    with open(db_file, "r", encoding="utf-8") as f:
        content = json.load(f)
    assert content["users"][0]["email"] == "alice@example.com"
