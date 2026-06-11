"""
Defines the Task model representing a specific work order or piece-rate job (Vibarua).
Supports tracking progress status and assigned contributors.
"""

class Task:
    _id_counter = 1

    def __init__(self, title, pay_amount, status="Pending"):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.pay_amount = pay_amount  # e.g., "KSh 1,500 / Day"
        self.status = status  # Pending, In Progress, Completed
        self.contributors = []  # Many-to-Many: Tracks individual Fundi IDs assigned here

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Task title cannot be empty.")
        self._title = value

    def assign_fundi(self, fundi_id):
        """Assigns a worker's User ID to this task piece."""
        if fundi_id not in self.contributors:
            self.contributors.append(fundi_id)

    def __str__(self):
        return f"[Task ID: {self.id}] {self.title} - Budget: {self.pay_amount} Status: {self.status}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "pay_amount": self.pay_amount,
            "status": self.status,
            "contributors": self.contributors
        }