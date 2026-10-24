from services.employee_service import (
    add_employee,
    deactivate_employee,
    get_all_employees,
    update_employee,
)

print("\nEMPLOYEE MANAGEMENT")
print("1. View all employees")
print("2. Add a new employee")
print("3. Update an employee")
print("4. Deactivate an employee")

choice = input("Enter your choice: ").strip()

if choice == "1":
    get_all_employees()
elif choice == "2":
    add_employee()
elif choice == "3":
    update_employee()
elif choice == "4":
    deactivate_employee()
else:
    print("Invalid choice.")