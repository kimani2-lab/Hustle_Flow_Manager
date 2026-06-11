"""
Defines the User model representing a Client or Fundi in the system.
Fulfills requirements for encapsulation, property decorators, and auto-incrementing IDs.
"""

class User:
    _id_counter = 1  # Class attribute for auto-incrementing unique IDs

    def __init__(self, name, email, role="Fundi"):
        self.id = User._id_counter
        User._id_counter += 1
        self.name = name
        self.email = email
        self.role = role  # Can be 'Client' or 'Fundi'
        self.projects = []  # One-to-Many: Tracks projects managed by this user

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("User name must be a valid non-empty string.")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email format.")
        self._email = value

    def __str__(self):
        return f"[User ID: {self.id}] {self.name} ({self.role}) - {self.email}"

    def to_dict(self):
        """Converts object state to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }