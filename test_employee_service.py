
from services.employee_service import add_employee, get_all_employees

print("1. View all employees")
print("2. Add a new employee")

choice = input("Enter your choice: ").strip()

if choice == "1":
    get_all_employees()
elif choice == "2":
    add_employee()
else:
    print("Invalid choice.")
