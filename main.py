#!/usr/bin/env python3
"""
HustleFlowManager CLI Application"""



import json
import os
try:
    from tabulate import tabulate
except ImportError:
    # Minimal fallback if 'tabulate' is not installed.
    def tabulate(rows, headers=None, tablefmt=None):
        out_lines = []
        if headers:
            out_lines.append(" | ".join(str(h) for h in headers))
            out_lines.append("-" * max(10, len(out_lines[0])))
        for r in rows:
            out_lines.append(" | ".join(str(c) for c in r))
        return "\n".join(out_lines)

# Importing our custom models
from models import User, Project, Task

DB_FILE = "data/db.json"

# In-memory storage lists tracking active instances
users_list = []
projects_list = []


def load_database():
    """Reads data from data/db.json and reconstructs Python Object models."""
    global users_list, projects_list
    users_list.clear()
    projects_list.clear()

    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        # Initialize an empty file if it doesn't exist
        with open(DB_FILE, "w") as f:
            json.dump({"users": [], "projects": []}, f)
        return

    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)

        # 1. Reconstruct Users
        for u_data in data.get("users", []):
            user = User(u_data["name"], u_data["email"], u_data["role"])
            user.id = u_data["id"]  # Match historical ID
            users_list.append(user)
            # Adjust the class counter so next IDs don't overlap
            User._id_counter = max(User._id_counter, user.id + 1)

        # 2. Reconstruct Projects & Nested Tasks
        for p_data in data.get("projects", []):
            project = Project(p_data["title"], p_data["description"], p_data["manager_id"])
            project.id = p_data["id"]
            Project._id_counter = max(Project._id_counter, project.id + 1)

            # Reconstruct Tasks inside this Project
            for t_data in p_data.get("tasks", []):
                task = Task(t_data["title"], t_data["pay_amount"], t_data["status"])
                task.id = t_data["id"]
                task.contributors = t_data.get("contributors", [])
                Task._id_counter = max(Task._id_counter, task.id + 1)
                project.tasks.append(task)

            projects_list.append(project)

        # 3. Associate One-to-Many Relationships
        for project in projects_list:
            manager = next((u for u in users_list if u.id == project.manager_id), None)
            if manager:
                manager.projects.append(project)

    except Exception as e:
        print(f"\n[Warning] Database read error, starting fresh: {e}")


def save_database():
    """Serializes in-memory object arrays to dictionary format and saves to file via File I/O."""
    data = {
        "users": [user.to_dict() for user in users_list],
        "projects": [project.to_dict() for project in projects_list]
    }
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data to file: {e}")


def add_new_user():
    print("\n--- Register a New User (Client / Fundi) ---")
    name = input("Enter Name: ").strip()
    email = input("Enter Email: ").strip()
    role = input("Enter Role (Client/Fundi) [Default: Fundi]: ").strip() or "Fundi"
    
    try:
        new_user = User(name, email, role)
        users_list.append(new_user)
        save_database()
        print(f"\n[Success] Registered: {new_user}")
    except ValueError as e:
        print(f"\n[Error] Verification failed: {e}")


def create_new_project():
    print("\n--- Create a New Site Project ---")
    if not users_list:
        print("Please register a user first to act as a manager/client.")
        return

    # Display users to select a manager
    headers = ["ID", "Name", "Role"]
    table_data = [[u.id, u.name, u.role] for u in users_list]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    try:
        manager_id = int(input("\nEnter the User ID of the managing Client: "))
        manager = next((u for u in users_list if u.id == manager_id), None)
        
        if not manager:
            print("User ID not found.")
            return

        title = input("Enter Project Title (e.g., Kimana Renovation): ").strip()
        description = input("Enter Brief Project Scope: ").strip()

        new_project = Project(title, description, manager.id)
        projects_list.append(new_project)
        manager.projects.append(new_project)  # Linking relationship
        save_database()
        print(f"\n[Success] Created Project: {new_project}")
    except ValueError:
        print("\n[Error] Invalid Input. ID must be an integer.")


def add_task_to_project():
    print("\n--- Add a Daily Kibaru (Task) to a Project ---")
    if not projects_list:
        print("No active projects found. Create a project first.")
        return

    headers = ["Project ID", "Title", "Manager ID"]
    table_data = [[p.id, p.title, p.manager_id] for p in projects_list]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    try:
        proj_id = int(input("\nEnter Project ID to attach this task to: "))
        project = next((p for p in projects_list if p.id == proj_id), None)

        if not project:
            print("Project not found.")
            return

        title = input("Enter Task Title (e.g., Floor Tiling): ").strip()
        pay = input("Enter Payout Amount (e.g., KSh 1,500/Day): ").strip()

        new_task = Task(title, pay)
        project.tasks.append(new_task)
        save_database()
        print(f"\n[Success] Added Task: {new_task}")
    except ValueError:
        print("\n[Error] Invalid Input.")


def assign_fundi_to_task():
    print("\n--- Assign a Fundi to a Task (Many-to-Many Assignment) ---")
    if not projects_list:
        print("No active projects/tasks available.")
        return

    # List all available tasks
    task_headers = ["Project Title", "Task ID", "Task Title", "Status", "Contributors"]
    task_rows = []
    for proj in projects_list:
        for t in proj.tasks:
            task_rows.append([proj.title, t.id, t.title, t.status, t.contributors])
    
    if not task_rows:
        print("No tasks found. Please add a task to a project first.")
        return
        
    print(tabulate(task_rows, headers=task_headers, tablefmt="grid"))

    try:
        task_id = int(input("\nEnter Task ID to update: "))
        
        # Find matching task across projects
        target_task = None
        for proj in projects_list:
            for t in proj.tasks:
                if t.id == task_id:
                    target_task = t
                    break

        if not target_task:
            print("Task ID not found.")
            return

        # Show available Fundis
        fundis = [u for u in users_list if u.role.lower() == "fundi"]
        if not fundis:
            print("No workers registered with the role 'Fundi' yet.")
            return

        print("\nAvailable Tradespeople (Fundis):")
        print(tabulate([[f.id, f.name, f.email] for f in fundis], headers=["ID", "Name", "Email"], tablefmt="grid"))

        fundi_id = int(input("\nEnter the Fundi's User ID to assign to this piece work: "))
        if not any(f.id == fundi_id for f in fundis):
            print("Invalid Fundi ID choice.")
            return

        target_task.assign_fundi(fundi_id)
        target_task.status = "In Progress"
        save_database()
        print(f"\n[Success] Assigned Fundi {fundi_id} to Task {task_id}. Task status updated to In Progress.")

    except ValueError:
        print("\n[Error] Invalid numeric entry.")


def view_dashboard():
    print("\n================== HUSTLEFLOW DASHBOARD ==================")
    print("\n--- REGISTERED USERS ---")
    if users_list:
        print(tabulate([[u.id, u.name, u.email, u.role] for u in users_list], 
                       headers=["ID", "Name", "Email", "Role"], tablefmt="simple"))
    else:
        print("No users in system database.")

    print("\n--- ACTIVE CONTRACTS & DAILY VIBARUA ---")
    if projects_list:
        for proj in projects_list:
            print(f"\nProject: {proj.title.upper()} | Scope: {proj.description}")
            if proj.tasks:
                task_data = [[t.id, t.title, t.pay_amount, t.status, t.contributors] for t in proj.tasks]
                print(tabulate(task_data, headers=["Task ID", "Job Item", "Payout Details", "Status", "Workers IDs Assigned"], tablefmt="grid"))
            else:
                print("  (No sub-tasks listed under this project site yet)")
    else:
        print("No construction or service contract pipelines registered.")
    print("\n==========================================================")


def main():
    load_database()
    while True:
        print("\n=== HUSTLEFLOW MANAGER CLI ===")
        print("1. Register a New User (Client / Fundi)")
        print("2. Create a New Contract Project")
        print("3. Add a Task/Vibarua to a Project")
        print("4. Assign a Fundi to a Task (Many-to-Many)")
        print("5. View Central Live Dashboard")
        print("6. Exit Application")
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == "1":
            add_new_user()
        elif choice == "2":
            create_new_project()
        elif choice == "3":
            add_task_to_project()
        elif choice == "4":
            assign_fundi_to_task()
        elif choice == "5":
            view_dashboard()
        elif choice == "6":
            print("\nThank you for using HustleFlow Manager. Closing connection. Kwaheri!")
            break
        else:
            print("\n[Error] Invalid choice. Please select 1 through 6.")


if __name__ == "__main__":
    main()