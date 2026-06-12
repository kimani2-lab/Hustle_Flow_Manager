import pytest

from models import User, Project, Task


def setup_function():
    User._id_counter = 1
    Project._id_counter = 1
    Task._id_counter = 1


def test_user_validation():
    user = User("Alice", "alice@example.com", "Client")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.role == "Client"
    with pytest.raises(ValueError):
        User("", "alice@example.com")
    with pytest.raises(ValueError):
        User("Alice", "invalid-email")


def test_project_and_task_relations():
    user = User("Bob", "bob@example.com", "Client")
    project = Project("Build site", "Construct a new office.", user.id)
    user.projects.append(project)
    task = Task("Lay foundation", "5000")
    project.tasks.append(task)

    assert task.status == "Pending"
    task.assign_fundi(1)
    assert 1 in task.contributors
    assert project in user.projects


def test_task_complete():
    task = Task("Paint wall", "1200")
    task.status = "In Progress"
    task.assign_fundi(2)
    task.status = "Completed"
    assert task.status == "Completed"
    assert task.contributors == [2]
