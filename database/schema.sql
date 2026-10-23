
CREATE DATABASE IF NOT EXISTS employee_tracker;

USE employee_tracker;

-- Table 1: Employees
CREATE TABLE IF NOT EXISTS employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    department VARCHAR(100) NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    employment_status ENUM('Active', 'Inactive')
        NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Tasks
CREATE TABLE IF NOT EXISTS tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    priority ENUM('Low', 'Medium', 'High', 'Critical')
        NOT NULL DEFAULT 'Medium',
    due_date DATE NOT NULL,
    status ENUM('Pending', 'In Progress', 'Completed', 'On Hold')
        NOT NULL DEFAULT 'Pending',
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tasks_created_by
        FOREIGN KEY (created_by)
        REFERENCES employees(employee_id)
);

--Table 3: Task Assignments
CREATE TABLE IF NOT EXISTS task_assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    employee_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_assignment_task
        FOREIGN KEY (task_id)
        REFERENCES tasks(task_id),

    CONSTRAINT fk_assignment_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),

    CONSTRAINT uq_task_employee
        UNIQUE (task_id, employee_id)
);


-- Table 4: Comments
CREATE TABLE IF NOT EXISTS comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    employee_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_comment_task
        FOREIGN KEY (task_id)
        REFERENCES tasks(task_id),

    CONSTRAINT fk_comment_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);


-- Table 5: Task History
CREATE TABLE IF NOT EXISTS task_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    changed_by INT NOT NULL,
    old_status ENUM('Pending', 'In Progress', 'Completed', 'On Hold'),
    new_status ENUM('Pending', 'In Progress', 'Completed', 'On Hold')
        NOT NULL,
    change_note VARCHAR(255),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_history_task
        FOREIGN KEY (task_id)
        REFERENCES tasks(task_id),

    CONSTRAINT fk_history_employee
        FOREIGN KEY (changed_by)
        REFERENCES employees(employee_id)
);
--Table 6: Users
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Employee') NOT NULL DEFAULT 'Employee',
    account_status ENUM('Active', 'Inactive')
        NOT NULL DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_users_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);

