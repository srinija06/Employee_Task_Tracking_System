
from services.assignment_service import assign_task
from services.auth_service import login
from services.employee_dashboard_service import (
    add_my_task_comment,
    update_my_task_status,
    view_my_task_comments,
    view_my_tasks,
)
from services.report_service import (
    view_employee_task_report,
    view_overdue_tasks,
    view_task_completion_summary,
)
from services.task_service import create_task, get_all_tasks
from services.user_service import create_employee_account


def admin_menu(user):
    """Display the Admin dashboard."""

    while True:
        print("\n========== ADMIN DASHBOARD ==========")
        print("1. Create Employee Login Account")
        print("2. Create Task")
        print("3. View All Tasks")
        print("4. Assign Task to Employee")
        print("5. View Overdue Tasks")
        print("6. View Employee Task Report")
        print("7. View Task Completion Summary")
        print("8. Logout")
        print("=====================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_employee_account(user)

        elif choice == "2":
            create_task(user)

        elif choice == "3":
            get_all_tasks()

        elif choice == "4":
            assign_task(user)

        elif choice == "5":
            view_overdue_tasks(user)

        elif choice == "6":
            view_employee_task_report(user)

        elif choice == "7":
            view_task_completion_summary(user)

        elif choice == "8":
            print("Admin logged out successfully.")
            break

        else:
            print("Invalid choice. Please select 1 to 8.")


def employee_menu(user):
    """Display the Employee dashboard."""

    while True:
        print("\n========== EMPLOYEE DASHBOARD ==========")
        print("1. View My Assigned Tasks")
        print("2. Update My Task Status")
        print("3. Add a Comment")
        print("4. View Task Comments")
        print("5. Logout")
        print("========================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_my_tasks(user)

        elif choice == "2":
            update_my_task_status(user)

        elif choice == "3":
            add_my_task_comment(user)

        elif choice == "4":
            view_my_task_comments(user)

        elif choice == "5":
            print("Employee logged out successfully.")
            break

        else:
            print("Invalid choice. Please select 1 to 5.")


def main():
    """Start the Employee Task Tracking System."""

    print("\nEMPLOYEE TASK TRACKING SYSTEM")
    print("=" * 38)

    user = login()

    if user is None:
        print("Access denied.")
        return

    if user["role"] == "Admin":
        admin_menu(user)

    elif user["role"] == "Employee":
        employee_menu(user)

    else:
        print("Error: Unknown user role.")


if __name__ == "__main__":
    main()
