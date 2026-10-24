from services.assignment_service import assign_task
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

print("\nEMPLOYEE MANAGEMENT")
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
    create_task()
elif choice == "7":
    update_task_status()
elif choice == "8":
    search_tasks()
elif choice == "9":
    assign_task()
elif choice == "10":
    add_comment()
elif choice == "11":
    view_task_comments()
elif choice == "12":
    view_overdue_tasks()
elif choice == "13":
    view_employee_task_report()
elif choice == "14":
    view_task_completion_summary()
else:
    print("Invalid choice.")