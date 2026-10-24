from services.employee_service import (
    add_employee,
    deactivate_employee,
    get_all_employees,
    update_employee,
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
else:
    print("Invalid choice.")