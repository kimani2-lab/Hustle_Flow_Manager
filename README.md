# HustleFlowManager

HustleFlowManager is a Python command-line application for managing users, projects, and tasks in a small team.

## Features

- Register users as `Client` or `Fundi`
- Create projects and associate them with a manager
- Add tasks to projects and assign contributors
- Mark tasks as complete
- Search projects by manager
- Persist data locally in `data/db.json`
- Supports both an interactive menu and command-line commands

## Installation

Recommended: create a virtual environment and install dependencies locally.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the app interactively:

```bash
.venv/bin/python main.py
```

Or use the CLI directly:

```bash
.venv/bin/python main.py dashboard
.venv/bin/python main.py list-users
.venv/bin/python main.py add-user --name "Alice" --email alice@example.com --role Client
.venv/bin/python main.py add-project --manager-id 1 --title "Build Office" --description "Office renovation"
.venv/bin/python main.py add-task --project-id 1 --title "Install wiring" --pay "5000"
.venv/bin/python main.py assign-task --task-id 1 --fundi-id 2
.venv/bin/python main.py complete-task --task-id 1
.venv/bin/python main.py search-projects --user-id 1
```

## Testing

Run tests with pytest:

```bash
.venv/bin/python -m pytest -q
```

## Data Persistence

Data is stored in `data/db.json`. The storage layer initializes the file if it is missing or empty.

## Files

- `main.py` — application entrypoint
- `cli.py` — user and project command logic plus interactive menu
- `storage.py` — JSON persistence helper functions
- `models/` — domain models for `User`, `Project`, and `Task`
- `tests/` — unit tests
## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

