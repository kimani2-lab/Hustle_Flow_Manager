"""
Defines the Project model representing a major job site contract.
Manages relationships with a supervising User and tracks associated tasks.
"""

class Project:
    _id_counter = 1

    def __init__(self, title, description, manager_id):
        self.id = Project._id_counter
        Project._id_counter += 1
        self.title = title
        self.description = description
        self.manager_id = manager_id  # Links back to a User ID (One-to-Many)
        self.tasks = []  # Tracks individual daily tasks assigned to this project

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Project title cannot be empty.")
        self._title = value

    def __str__(self):
        return f"[Project ID: {self.id}] {self.title} (Managed by User: {self.manager_id})"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "manager_id": self.manager_id,
            "tasks": [task.to_dict() for task in self.tasks]
        }