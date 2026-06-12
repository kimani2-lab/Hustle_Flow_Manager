import argparse
import sys

from models import User, Project, Task
from storage import load_data, save_data

try:
    from tabulate import tabulate
except Exception:
    def tabulate(rows, headers=None, tablefmt=None):
        lines = []
        if headers:
            lines.append(" | ".join(str(h) for h in headers))
            lines.append("-" * max(10, len(lines[0])))
        for row in rows:
            lines.append(" | ".join(str(item) for item in row))
        return "\n".join(lines)


def print_table(rows, headers=None, tablefmt="grid"):
    if not rows:
        print("(No records found)")
        return
    print(tabulate(rows, headers=headers, tablefmt=tablefmt))


def list_users(users):
    print_table([[u.id, u.name, u.email, u.role] for u in users], headers=["ID", "Name", "Email", "Role"], tablefmt="simple")


def list_projects(projects, users):
    rows = []
    for project in projects:
        manager = next((u.name for u in users if u.id == project.manager_id), "Unknown")
        rows.append([project.id, project.title, project.description, manager, len(project.tasks)])
    print_table(rows, headers=["ID", "Project", "Description", "Manager", "Tasks"], tablefmt="grid")


def list_tasks(projects):
    rows = []
    for project in projects:
        for task in project.tasks:
            rows.append([task.id, project.id, task.title, task.pay_amount, task.status, task.contributors])
    print_table(rows, headers=["Task ID", "Project ID", "Title", "Pay", "Status", "Contributors"], tablefmt="grid")


def search_projects_by_user(projects, user_id):
    return [project for project in projects if project.manager_id == user_id]


def find_project(projects, project_id):
    return next((project for project in projects if project.id == project_id), None)


def find_task(projects, task_id):
    for project in projects:
        for task in project.tasks:
            if task.id == task_id:
                return task
    return None


def find_user(users, user_id):
    return next((user for user in users if user.id == user_id), None)


def create_user(users, name, email, role="Fundi"):
    new_user = User(name, email, role)
    users.append(new_user)
    return new_user


def create_project(projects, users, manager_id, title, description):
    manager = find_user(users, manager_id)
    if manager is None:
        raise ValueError("Manager ID not found.")
    project = Project(title, description, manager.id)
    projects.append(project)
    manager.projects.append(project)
    return project


def create_task(projects, project_id, title, pay_amount):
    project = find_project(projects, project_id)
    if project is None:
        raise ValueError("Project ID not found.")
    task = Task(title, pay_amount)
    project.tasks.append(task)
    return task


def assign_fundi_to_task(projects, users, task_id, fundi_id):
    task = find_task(projects, task_id)
    if task is None:
        raise ValueError("Task ID not found.")
    fundi = find_user(users, fundi_id)
    if fundi is None or fundi.role.lower() != "fundi":
        raise ValueError("Fundi ID not found or is not a Fundi.")
    task.assign_fundi(fundi.id)
    task.status = "In Progress"
    return task


def mark_task_complete(projects, task_id):
    task = find_task(projects, task_id)
    if task is None:
        raise ValueError("Task ID not found.")
    task.status = "Completed"
    return task


def view_dashboard(users, projects):
    print("\n=== HUSTLEFLOW DASHBOARD ===\n")
    print("Registered Users:")
    list_users(users)
    print("\nActive Projects:")
    list_projects(projects, users)
    print("\nAll Tasks:")
    list_tasks(projects)


def interactive_menu():
    users, projects = load_data()
    while True:
        print("\n=== HustleFlow Manager CLI ===")
        print("1. Register a New User")
        print("2. Create a New Project")
        print("3. Add a Task to a Project")
        print("4. Assign a Fundi to a Task")
        print("5. Mark Task Complete")
        print("6. Search Projects by User")
        print("7. View Dashboard")
        print("8. Exit")
        choice = input("Select an option (1-8): ").strip()

        try:
            if choice == "1":
                name = input("Enter name: ").strip()
                email = input("Enter email: ").strip()
                role = input("Enter role (Client/Fundi) [Fundi]: ").strip() or "Fundi"
                create_user(users, name, email, role)
                save_data(users, projects)
                print("User registered successfully.")
            elif choice == "2":
                list_users(users)
                manager_id = int(input("Enter manager User ID: ").strip())
                title = input("Enter project title: ").strip()
                description = input("Enter project description: ").strip()
                create_project(projects, users, manager_id, title, description)
                save_data(users, projects)
                print("Project created successfully.")
            elif choice == "3":
                list_projects(projects, users)
                project_id = int(input("Enter project ID: ").strip())
                title = input("Enter task title: ").strip()
                pay_amount = input("Enter pay amount: ").strip()
                create_task(projects, project_id, title, pay_amount)
                save_data(users, projects)
                print("Task added successfully.")
            elif choice == "4":
                list_tasks(projects)
                task_id = int(input("Enter task ID: ").strip())
                list_users([u for u in users if u.role.lower() == "fundi"])
                fundi_id = int(input("Enter fundi ID: ").strip())
                assign_fundi_to_task(projects, users, task_id, fundi_id)
                save_data(users, projects)
                print("Fundi assigned successfully.")
            elif choice == "5":
                list_tasks(projects)
                task_id = int(input("Enter task ID to mark complete: ").strip())
                mark_task_complete(projects, task_id)
                save_data(users, projects)
                print("Task marked complete.")
            elif choice == "6":
                list_users(users)
                user_id = int(input("Enter user ID to search projects for: ").strip())
                found = search_projects_by_user(projects, user_id)
                print_table([[p.id, p.title, p.description] for p in found], headers=["ID", "Title", "Description"], tablefmt="grid")
            elif choice == "7":
                view_dashboard(users, projects)
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1-8.")
        except ValueError as exc:
            print(f"Error: {exc}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="HustleFlowManager command-line project tracker")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("dashboard", help="View the dashboard")
    sub.add_parser("list-users", help="List all registered users")
    sub.add_parser("list-projects", help="List all projects")
    sub.add_parser("list-tasks", help="List all tasks")

    add_user = sub.add_parser("add-user", help="Create a new user")
    add_user.add_argument("--name", required=True)
    add_user.add_argument("--email", required=True)
    add_user.add_argument("--role", default="Fundi")

    add_project = sub.add_parser("add-project", help="Create a new project")
    add_project.add_argument("--manager-id", type=int, required=True)
    add_project.add_argument("--title", required=True)
    add_project.add_argument("--description", required=True)

    add_task = sub.add_parser("add-task", help="Add a task to a project")
    add_task.add_argument("--project-id", type=int, required=True)
    add_task.add_argument("--title", required=True)
    add_task.add_argument("--pay", required=True)

    assign = sub.add_parser("assign-task", help="Assign a fundi to a task")
    assign.add_argument("--task-id", type=int, required=True)
    assign.add_argument("--fundi-id", type=int, required=True)

    complete = sub.add_parser("complete-task", help="Mark a task complete")
    complete.add_argument("--task-id", type=int, required=True)

    search = sub.add_parser("search-projects", help="List projects managed by a user")
    search.add_argument("--user-id", type=int, required=True)

    sub.add_parser("interactive", help="Start the interactive menu")

    args = parser.parse_args(argv)
    users, projects = load_data()

    if args.command in (None, "interactive"):
        interactive_menu()
        return

    if args.command == "dashboard":
        view_dashboard(users, projects)
    elif args.command == "list-users":
        list_users(users)
    elif args.command == "list-projects":
        list_projects(projects, users)
    elif args.command == "list-tasks":
        list_tasks(projects)
    elif args.command == "add-user":
        create_user(users, args.name, args.email, args.role)
        save_data(users, projects)
        print("User created.")
    elif args.command == "add-project":
        create_project(projects, users, args.manager_id, args.title, args.description)
        save_data(users, projects)
        print("Project created.")
    elif args.command == "add-task":
        create_task(projects, args.project_id, args.title, args.pay)
        save_data(users, projects)
        print("Task created.")
    elif args.command == "assign-task":
        assign_fundi_to_task(projects, users, args.task_id, args.fundi_id)
        save_data(users, projects)
        print("Task assignment saved.")
    elif args.command == "complete-task":
        mark_task_complete(projects, args.task_id)
        save_data(users, projects)
        print("Task marked complete.")
    elif args.command == "search-projects":
        found = search_projects_by_user(projects, args.user_id)
        print_table([[p.id, p.title, p.description] for p in found], headers=["ID", "Title", "Description"], tablefmt="grid")
    else:
        parser.print_help()

