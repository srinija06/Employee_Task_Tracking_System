
from services.assignment_service import assign_task
from services.auth_service import login
from services.comment_service import add_comment, view_task_comments
from services.employee_service import (
    add_employee,
    deactivate_employee,
    get_all_employees,
    update_employee,
)
from services.report_service import (
    view_employee_task_report,
    view_overdue_tasks,
    view_task_completion_summary,
)
from services.task_service import (
    create_task,
    get_all_tasks,
    search_tasks,
    update_task_status,
)


def main():
    """Run the interactive Admin testing menu."""

    user = login()

    if user is None:
        print("Access denied.")
        return

    if user.get("role") != "Admin":
        print("Access denied. Only Admin can use this test menu.")
        return

    while True:
        print("\n========== EMPLOYEE MANAGEMENT ==========")
        print("1. View all employees")
        print("2. Add a new employee")
        print("3. Update an employee")
        print("4. Deactivate an employee")
        print("5. View all tasks")
        print("6. Create a new task")
        print("7. Update task status")
        print("8. Search and filter tasks")
        print("9. Assign task to employee")
        print("10. Add a task comment")
        print("11. View task comments")
        print("12. View overdue tasks")
        print("13. View employee task report")
        print("14. View task completion summary")
        print("15. Exit")
        print("=========================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            get_all_employees()

        elif choice == "2":
            add_employee()

        elif choice == "3":
            update_employee()

        elif choice == "4":
            deactivate_employee()

        elif choice == "5":
            get_all_tasks()

        elif choice == "6":
            create_task(user)

        elif choice == "7":
            update_task_status()

        elif choice == "8":
            search_tasks()

        elif choice == "9":
            assign_task(user)

        elif choice == "10":
            add_comment(user)

        elif choice == "11":
            view_task_comments()

        elif choice == "12":
            view_overdue_tasks(user)

        elif choice == "13":
            view_employee_task_report(user)

        elif choice == "14":
            view_task_completion_summary(user)

        elif choice == "15":
            print("Exiting the temporary test menu.")
            break

        else:
            print("Invalid choice. Please select 1 to 15.")


if __name__ == "__main__":
    main()
