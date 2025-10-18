-- ========================================================
-- Database: employees
-- Description: Employee Management System (XAMPP + Python)
-- Includes sample data for testing
-- ========================================================

-- 1️⃣ Create database
CREATE DATABASE IF NOT EXISTS employees;
USE employees;

-- 2️⃣ Create user login table
CREATE TABLE IF NOT EXISTS log (
  username VARCHAR(50) PRIMARY KEY,
  password VARCHAR(100)
);

-- Sample login users
INSERT INTO log (username, password) VALUES
('admin', 'admin123'),
('manager', 'manager123'),
('hruser', 'hrpass');

-- 3️⃣ Create employee details table
CREATE TABLE IF NOT EXISTS office (
  em_no VARCHAR(20) PRIMARY KEY,         -- Manual Employee ID (entered by user)
  em_name VARCHAR(100),                  -- Employee name
  em_dept VARCHAR(100),                  -- Department
  em_salary FLOAT,                       -- Salary
  em_age INT                             -- Age
);

-- Sample employee records
INSERT INTO office (em_no, em_name, em_dept, em_salary, em_age) VALUES
('E001', 'Suman Bhattacharya', 'Development', 400000, 24),
('E002', 'Riya Mehta', 'HR', 350000, 26),
('E003', 'Arjun Das', 'Finance', 420000, 29),
('E004', 'Priya Singh', 'Marketing', 300000, 25),
('E005', 'Karan Patel', 'IT Support', 320000, 28);

-- 4️⃣ Create employee performance table
CREATE TABLE IF NOT EXISTS em_performance (
  id INT AUTO_INCREMENT PRIMARY KEY,     -- Unique record ID
  em_no VARCHAR(20),                     -- Employee ID (links to office.em_no)
  em_name VARCHAR(100),                  -- Employee name
  em_dept VARCHAR(100),                  -- Department
  performance VARCHAR(10),               -- Performance rating (A+, A, B, etc.)
  experience VARCHAR(100),               -- Experience description (years or details)
  FOREIGN KEY (em_no) REFERENCES office(em_no) ON DELETE CASCADE
);

-- Sample performance records
INSERT INTO em_performance (em_no, em_name, em_dept, performance, experience) VALUES
('E001', 'Suman Bhattacharya', 'Development', 'A+', '2 years'),
('E002', 'Riya Mehta', 'HR', 'A', '3 years'),
('E003', 'Arjun Das', 'Finance', 'B+', '4 years'),
('E004', 'Priya Singh', 'Marketing', 'A', '1.5 years'),
('E005', 'Karan Patel', 'IT Support', 'B', '2 years');

-- ✅ Done: Database, tables, and sample data created successfully
