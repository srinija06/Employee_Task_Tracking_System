# Employee Task Tracking System

A Python and MySQL-based application designed to manage employee information, assign tasks, track task progress, and generate task reports. The system provides separate Admin and Employee dashboards with role-based access control.

## Features

### Admin Dashboard
- Create and manage employee profiles.
- Create employee login accounts.
- Create tasks and assign them to employees.
- View all tasks.
- Search and filter tasks.
- View overdue tasks.
- Generate employee task reports.
- View task completion summaries.

### Employee Dashboard
- Log in using individual credentials.
- View assigned tasks.
- Update the status of assigned tasks.
- Add comments to assigned tasks.
- View task-related comments.

### Security
- Role-based access control for Admin and Employee users.
- Password hashing using bcrypt.
- Parameterized SQL queries.
- Database credentials managed through environment variables.
- Validation of user input and password requirements.

## Technologies Used

- **Programming Language:** Python
- **Database:** MySQL
- **Database Connectivity:** mysql-connector-python
- **Password Hashing:** bcrypt
- **Environment Configuration:** python-dotenv
- **Automated Testing:** pytest
- **Development Tools:** Visual Studio Code, MySQL Workbench, Git, and GitHub


## Project Structure

```text
employee-task-tracking-system/
├── app.py
├── config.py
├── create_admin.py
├── read_employees.py
├── test_connection.py
├── test_employee_service.py
├── database/
│   ├── schema.sql
│   └── seed.sql
├── database_connection/
│   ├── __init__.py
│   └── connection.py
├── docs/
│   ├── database_design.md
│   └── screenshots/
├── services/
│   ├── assignment_service.py
│   ├── auth_service.py
│   ├── comment_service.py
│   ├── employee_dashboard_service.py
│   ├── employee_service.py
│   ├── report_service.py
│   ├── task_service.py
│   └── user_service.py
├── tests/
│   ├── test_assignments.py
│   ├── test_employees.py
│   ├── test_tasks.py
│   ├── test_users.py
│   └── test_validators.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   └── validators.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```


## Prerequisites

Before running the project, install:

- Python 3.10 or a compatible version
- MySQL Server
- MySQL Workbench (recommended)
- Git (for cloning the repository)

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/srinija06/Employee_Task_Tracking_System.git
cd Employee_Task_Tracking_System
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Set up the database

1. Start MySQL Server and open MySQL Workbench.
2. Create the `employee_tracker` database if it does not already exist.
3. Execute `database/schema.sql` to create the required tables.
4. Execute `database/seed.sql` if you want to insert the sample data.

**Important:** Review the SQL files before running them against an existing database to avoid unintended changes to existing data.

### 5. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Configure your own MySQL credentials:

```dotenv
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=employee_tracker
```

Replace the placeholder password with your actual MySQL password.

**Security note:** Never commit `.env` or expose your database password on GitHub. Only commit `.env.example` with placeholder values.

### 6. Create an Admin account

Run the project's Admin account creation script:

```powershell
python create_admin.py
```

Follow the prompts. Use this script to create an initial Admin account if your implementation supports that workflow.

### 7. Run the application

```powershell
python app.py
```

Log in using an account created in the database.

## Running Automated Tests

Run the complete test suite with:

```powershell
python -m pytest -v
```

The project currently has **15 passing automated tests** covering areas such as input validation, employee creation, task creation, authorization, and password validation.

## Database Design

The database includes tables for:

- Employee profiles
- User login accounts
- Tasks
- Task assignments
- Comments
- Task history

Refer to `docs/database_design.md` for additional database design information.

## Future Enhancements

- Develop a web-based user interface.
- Add task deadline reminders and notifications.
- Expand automated test coverage.
- Improve reporting and dashboard visualizations.
- Introduce employee-specific task progress tracking if required.

## Project Objective

This project demonstrates practical skills in Python programming, relational database management, SQL operations, authentication, role-based authorization, error handling, and automated testing.
