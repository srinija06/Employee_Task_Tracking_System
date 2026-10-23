
USE employee_tracker;

-- Sample employee records
INSERT INTO employees
    (name, email, department, job_title)
VALUES
    ('Rahul Sharma', 'rahul@company.com', 'IT', 'Developer'),
    ('Priya Verma', 'priya@company.com', 'HR', 'HR Executive'),
    ('Arjun Reddy', 'arjun@company.com', 'Analytics', 'Data Analyst'),
    ('Swetha Reddy', 'swetha@company.com', 'Finance', 'Accountant'),
    ('Nikhil Kumar', 'nikhil@company.com', 'IT', 'Backend Developer'),
    ('Divya Rao', 'divya@company.com', 'Analytics', 'Business Analyst'),
    ('Manoj Verma', 'manoj@company.com', 'HR', 'Recruiter'),
    ('Keerthi Patel', 'keerthi@company.com', 'IT', 'Software Tester');



-- Sample task records
USE employee_tracker;

INSERT INTO tasks
    (title, description, priority, due_date, status, created_by)
VALUES
    (
        'Develop Employee Dashboard',
        'Create a dashboard to display employee information.',
        'High',
        '2026-11-05',
        'In Progress',
        1
    ),
    (
        'Prepare Monthly Sales Report',
        'Analyze monthly sales data and prepare a report.',
        'Medium',
        '2026-11-08',
        'Pending',
        3
    ),
    (
        'Update Employee Records',
        'Review and update employee information.',
        'Low',
        '2026-11-10',
        'Pending',
        2
    ),
    (
        'Fix Login Module Bug',
        'Investigate and fix an issue in the login module.',
        'Critical',
        '2026-10-28',
        'In Progress',
        1
    ),
    (
        'Test Task Management Module',
        'Perform functional testing of task management features.',
        'High',
        '2026-11-12',
        'On Hold',
        3
    );
-- Sample task assignments
INSERT INTO task_assignments (task_id, employee_id)
VALUES
    (1, 4),
    (2, 5),
    (3, 6),
    (4, 7),
    (5, 8);


-- Sample task comments
INSERT INTO comments
    (task_id, employee_id, comment_text)
VALUES
    (1, 4, 'Started working on the employee dashboard.'),
    (2, 5, 'Collecting the monthly sales data.'),
    (3, 6, 'Employee records are under review.'),
    (4, 7, 'Investigating the login module bug.'),
    (5, 8, 'Testing is waiting for approval.');

-- Sample task status history
INSERT INTO task_history
    (task_id, changed_by, old_status, new_status, change_note)
VALUES
    (1, 4, 'Pending', 'In Progress', 'Started dashboard development.'),
    (2, 5, 'Pending', 'In Progress', 'Started collecting sales data.'),
    (3, 6, 'Pending', 'In Progress', 'Started reviewing employee records.'),
    (4, 7, 'Pending', 'In Progress', 'Started investigating the login bug.'),
    (5, 8, 'Pending', 'On Hold', 'Waiting for approval.');
