"""
database.py

Handles MySQL database operations for CALC-X.
"""

import mysql.connector
from mysql.connector import Error


# ---------------------------------------------------------
# Database configuration
# ---------------------------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Fayaz@1234",
    "database": "calcx"
}


# ---------------------------------------------------------
# Connect to database
# ---------------------------------------------------------

def connect_database():
    """
    Connects to the CALC-X MySQL database.

    Returns:
        MySQL connection object
    """

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

    except Error as error:
        print("Database connection error:", error)

    return None


# ---------------------------------------------------------
# User functions
# ---------------------------------------------------------

def create_user(username: str):
    """
    Creates a user if the username does not already exist.

    Returns:
        user_id or None
    """

    connection = connect_database()

    if connection is None:
        return None

    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT user_id FROM users WHERE username = %s",
            (username,)
        )

        row = cursor.fetchone()

        if row is not None:
            return row[0]

        cursor.execute(
            "INSERT INTO users (username) VALUES (%s)",
            (username,)
        )

        connection.commit()

        return cursor.lastrowid

    except Error as error:
        print("Database error:", error)
        return None

    finally:
        cursor.close()
        connection.close()


# ---------------------------------------------------------
# Add calculation
# ---------------------------------------------------------

def add_calculation(
    user_id: int,
    expression: str,
    result: str,
    module: str
) -> None:
    """
    Stores a successful calculation in MySQL.
    """

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        query = """
        INSERT INTO calculations
        (user_id, expression, result, module)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            user_id,
            expression,
            result,
            module
        )

        cursor.execute(query, values)

        connection.commit()

    except Error as error:
        print("Could not save calculation:", error)

    finally:
        cursor.close()
        connection.close()


# ---------------------------------------------------------
# Get history
# ---------------------------------------------------------

def get_history(user_id: int) -> list:
    """
    Returns all calculations belonging to a user.
    """

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor()

    try:
        query = """
        SELECT calculation_id,
               expression,
               result,
               module,
               timestamp
        FROM calculations
        WHERE user_id = %s
        ORDER BY timestamp DESC
        """

        cursor.execute(query, (user_id,))

        return cursor.fetchall()

    except Error as error:
        print("Could not retrieve history:", error)
        return []

    finally:
        cursor.close()
        connection.close()


# ---------------------------------------------------------
# Search history
# ---------------------------------------------------------

def search_history(user_id: int, keyword: str) -> list:
    """
    Searches calculations belonging to a user.
    """

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor()

    try:
        query = """
        SELECT calculation_id,
               expression,
               result,
               module,
               timestamp
        FROM calculations
        WHERE user_id = %s
        AND expression LIKE %s
        ORDER BY timestamp DESC
        """

        search_value = "%" + keyword + "%"

        cursor.execute(
            query,
            (user_id, search_value)
        )

        return cursor.fetchall()

    except Error as error:
        print("Could not search history:", error)
        return []

    finally:
        cursor.close()
        connection.close()


# ---------------------------------------------------------
# Delete one calculation
# ---------------------------------------------------------

def delete_calculation(
    user_id: int,
    calculation_id: int
) -> None:
    """
    Deletes one calculation belonging to the current user.
    """

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        query = """
        DELETE FROM calculations
        WHERE calculation_id = %s
        AND user_id = %s
        """

        cursor.execute(
            query,
            (calculation_id, user_id)
        )

        connection.commit()

        if cursor.rowcount == 0:
            print("Calculation not found.")

        else:
            print("Calculation deleted successfully.")

    except Error as error:
        print("Could not delete calculation:", error)

    finally:
        cursor.close()
        connection.close()


# ---------------------------------------------------------
# Clear history
# ---------------------------------------------------------

def clear_history(user_id: int) -> None:
    """
    Deletes all calculations belonging to the current user.
    """

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:
        query = """
        DELETE FROM calculations
        WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))

        connection.commit()

        print("History cleared successfully.")

    except Error as error:
        print("Could not clear history:", error)

    finally:
        cursor.close()
        connection.close()


# ---------------------------------------------------------
# Module statistics
# ---------------------------------------------------------

def get_module_statistics(user_id: int) -> list:
    """
    Returns number of calculations performed
    in each module.
    """

    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor()

    try:
        query = """
        SELECT module, COUNT(*)
        FROM calculations
        WHERE user_id = %s
        GROUP BY module
        ORDER BY COUNT(*) DESC
        """

        cursor.execute(query, (user_id,))

        return cursor.fetchall()

    except Error as error:
        print("Could not retrieve statistics:", error)
        return []

    finally:
        cursor.close()
        connection.close()