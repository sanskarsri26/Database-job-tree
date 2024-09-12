-- Create a new database
CREATE DATABASE IF NOT EXISTS test_db;

-- Use the new database
USE test_db;

-- Create a new table called 'employees'
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100),
    salary DECIMAL(10, 2),
    hire_date DATE
);

-- Insert sample data into 'employees' table
INSERT INTO employees (name, position, salary, hire_date)
VALUES 
    ('John Doe', 'Software Engineer', 80000.00, '2022-01-15'),
    ('Jane Smith', 'Data Scientist', 90000.00, '2022-03-22'),
    ('Michael Brown', 'DevOps Engineer', 85000.00, '2023-06-30');

-- Query the table to check the data
SELECT * FROM employees;

-- Update a record
UPDATE employees SET salary = 95000.00 WHERE name = 'John Doe';

-- Delete a record
DELETE FROM employees WHERE name = 'Jane Smith';

-- Select all records again to see the changes
SELECT * FROM employees;
