# HustleFlowManager

HustleFlowManager is a simple command-line application for managing construction and service contract projects, users, and daily task assignments.

## Features

- Register users as `Client` or `Fundi`
- Create contract projects and assign a manager
- Add daily tasks (`Vibarua`) to projects
- Assign Fundis to tasks and update task status
- View a live dashboard of users, projects, and task assignments

## Project Structure

- `main.py` - CLI application entry point and workflow logic
- `models/` - Domain models used by the app
  - `models/user.py` - `User` model
  - `models/project.py` - `Project` model
  - `models/task.py` - `Task` model
  - `models/__init__.py` - Exports models for easy import
- `data/db.json` - JSON file used for persistent storage
- `requirements.txt` - dependencies (currently optional)

## Installation

1. Ensure you have Python 3 installed.
2. (Optional) Install `tabulate` for nicer tables:

```bash
pip install tabulate
```

## Usage

Run the application from the project root:

```bash
python3 main.py
```

Choose from the menu to:

1. Register a new user
2. Create a new project
3. Add a task to a project
4. Assign a Fundi to a task
5. View the live dashboard
6. Exit

## Data Persistence

The app stores data in `data/db.json`. If the file does not exist or is empty, it is initialized automatically.

## Notes

- `models/__init__.py` exports the `User`, `Project`, and `Task` classes so `main.py` can import them cleanly.
- User roles are expected to be `Client` or `Fundi`.
- Task assignment is recorded by storing Fundi IDs in the task `contributors` list.
