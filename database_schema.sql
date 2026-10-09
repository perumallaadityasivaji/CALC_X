
-- ==========================================
-- CALC-X DATABASE SCHEMA
-- ==========================================

-- 1. Create the database
CREATE DATABASE IF NOT EXISTS calcx;

-- Select the database
USE calcx;


-- ==========================================
-- 2. USERS TABLE
-- Stores each CALC-X user's information
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE
);


-- ==========================================
-- 3. CALCULATIONS TABLE
-- Stores users' calculation history
-- ==========================================

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


-- ==========================================
-- 4. VIEW ALL TABLES
-- ==========================================

SHOW TABLES;


-- ==========================================
-- 5. VIEW TABLE STRUCTURES
-- ==========================================

DESCRIBE users;

DESCRIBE calculations;


-- ==========================================
-- 6. VIEW ALL USERS
-- ==========================================

SELECT * FROM users;


-- ==========================================
-- 7. VIEW ALL CALCULATIONS
-- ==========================================

SELECT * FROM calculations;


-- ==========================================
-- 8. VIEW HISTORY WITH USERNAMES
-- ==========================================

SELECT
    users.user_id,
    users.username,
    calculations.calculation_id,
    calculations.expression,
    calculations.result,
    calculations.module,
    calculations.timestamp
FROM users
INNER JOIN calculations
    ON users.user_id = calculations.user_id
ORDER BY calculations.timestamp DESC;


-- ==========================================
-- 9. COUNT CALCULATIONS BY MODULE
-- ==========================================

SELECT
    module,
    COUNT(*) AS total_calculations
FROM calculations
GROUP BY module
ORDER BY total_calculations DESC;


-- ==========================================
-- 10. COUNT CALCULATIONS PER USER
-- ==========================================

SELECT
    users.username,
    COUNT(calculations.calculation_id) AS total_calculations
FROM users
LEFT JOIN calculations
    ON users.user_id = calculations.user_id
GROUP BY users.user_id, users.username;

