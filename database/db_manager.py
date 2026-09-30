# Import sqlite3 - Python's built-in SQLite database library
# Used for: Creating database connections, executing SQL queries, managing transactions
import sqlite3

# Import os - Python's built-in operating system interface library
# Used for: File/folder operations (checking if files exist, creating directories, path handling)
import os

# Import datetime - Python's built-in date and time library
# Used for: Working with timestamps, formatting dates, getting current time
from datetime import datetime

class DatabaseManager:
    """
    Handles all database operations for TaskBot.
    Uses SQLite as a lightweight, file-based database.
    """
    
    def __init__(self, db_path='data/taskbot.db'):
        """
        Initialize database manager with path to SQLite file.
        
        Args:
            db_path (str): Path where the database file will be stored
        """
        # Store the database path
        self.db_path = db_path
        
        # Create the 'data' folder if it doesn't exist
        # os.path.dirname gets the folder part of the path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Create tables if they don't exist yet
        self._create_tables()
    
    def _get_connection(self):
        """
        Create and return a database connection.
        
        The underscore prefix (_) is a Python convention meaning
        "this is a private method, only use inside this class"
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        # Connect to SQLite database (creates file if doesn't exist)
        conn = sqlite3.connect(self.db_path)
        
        # This makes query results return as dictionaries instead of tuples
        # Example: row['username'] instead of row[0]
        conn.row_factory = sqlite3.Row
        
        return conn
    
    def _create_tables(self):
        """
        Create all necessary tables if they don't exist.
        This runs automatically when DatabaseManager is initialized.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    priority TEXT DEFAULT 'medium',
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    user_input TEXT NOT NULL,
                    detected_intent TEXT,
                    bot_response TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Commit changes to database
            conn.commit()
    
    def execute_query(self, query, params=()):
        """
        Execute a SELECT query and return results.
        
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters to safely insert into query
        
        Returns:
            list: Query results as list of Row objects
        
        Example:
            results = db.execute_query(
                "SELECT * FROM users WHERE username = ?", 
                ("john_doe",)
            )
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_update(self, query, params=()):
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query (str): SQL query to execute
            params (tuple): Parameters to safely insert into query
        
        Returns:
            int: ID of last inserted row (for INSERT) or number of affected rows
        
        Example:
            user_id = db.execute_update(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                ("john_doe", "hashed_password_here")
            )
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            # Return the ID of the newly created row (useful for INSERT)
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount