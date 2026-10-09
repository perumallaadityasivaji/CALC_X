-- CALC-X Database Setup
-- Run this file in MySQL Workbench.

CREATE DATABASE IF NOT EXISTS calcx;
USE calcx;

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS calculations (
    calculation_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    expression TEXT NOT NULL,
    result TEXT NOT NULL,
    module VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_calculations_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Optional queries for viewing data:
-- SELECT * FROM users;
-- SELECT * FROM calculations ORDER BY timestamp DESC;
