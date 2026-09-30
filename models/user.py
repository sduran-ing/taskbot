import bcrypt
from database.db_manager import DatabaseManager

class User:
    """
    Handles all user-related operations: registration, login, and user data.
    Uses bcrypt for secure password hashing.
    
    Architecture Note: This follows the Active Record pattern where the model
    contains both business logic and database operations. In larger applications,
    you might separate this into a Service layer (business logic) and Repository
    layer (data access), but for this project size, Active Record is appropriate.
    """
    
    def __init__(self, db_manager):
        """
        Initialize User model with database manager.
        
        Args:
            db_manager (DatabaseManager): Database manager instance
        """
        self.db = db_manager
    
    def _hash_password(self, password):
        """
        Hash a password using bcrypt.
        
        This is a private method (notice the underscore) because
        users of this class shouldn't call it directly.
        
        Args:
            password (str): Plain text password
        
        Returns:
            str: Hashed password as a string
        
        How bcrypt works:
        1. Generates a random "salt" (extra random data)
        2. Combines salt + password
        3. Runs through hashing algorithm many times (slow on purpose!)
        4. Returns hash that includes the salt
        
        Note: No try-except here because this is an internal helper method.
        If bcrypt fails, we want to see the error during development.
        """
        # Convert string to bytes (bcrypt requires bytes)
        password_bytes = password.encode('utf-8')
        
        # Generate salt and hash the password
        # The '12' is the "cost factor" - higher = more secure but slower
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Convert bytes back to string for database storage
        return hashed.decode('utf-8')
    
    def _verify_password(self, password, password_hash):
        """
        Verify a password against its hash.
        
        Args:
            password (str): Plain text password to check
            password_hash (str): Stored hash from database
        
        Returns:
            bool: True if password matches, False otherwise
        
        How verification works:
        - bcrypt extracts the salt from the stored hash
        - Hashes the input password with that same salt
        - Compares the results
        
        Note: No try-except here because this is an internal helper method.
        """
        # Convert both to bytes
        password_bytes = password.encode('utf-8')
        hash_bytes = password_hash.encode('utf-8')
        
        # bcrypt does the comparison securely
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def register(self, username, password):
        """
        Register a new user account.
        
        This method includes comprehensive error handling because it's a
        user-facing operation that could fail in many ways (network issues,
        database problems, validation errors, etc.).
        
        Args:
            username (str): Desired username
            password (str): Plain text password
        
        Returns:
            dict: {"success": bool, "message": str, "user_id": int or None}
        
        Example:
            result = user.register("diana", "myPassword123")
            if result["success"]:
                print(f"User ID: {result['user_id']}")
            else:
                print(f"Error: {result['message']}")
        """
        try:
            # Validation: Check if username is not empty
            if not username or not username.strip():
                return {
                    "success": False,
                    "message": "Username cannot be empty",
                    "user_id": None
                }
            
            # Validation: Check if password is strong enough
            if len(password) < 6:
                return {
                    "success": False,
                    "message": "Password must be at least 6 characters",
                    "user_id": None
                }
            
            # Check if username already exists
            # This query could fail if database is locked or corrupted
            existing_user = self.db.execute_query(
                "SELECT id FROM users WHERE username = ?",
                (username,)
            )
            
            if existing_user:
                return {
                    "success": False,
                    "message": "Username already exists",
                    "user_id": None
                }
            
            # Hash the password (NEVER store plain text!)
            password_hash = self._hash_password(password)
            
            # Insert new user into database
            # This could fail if database is locked, disk is full, etc.
            user_id = self.db.execute_update(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            
            return {
                "success": True,
                "message": "Registration successful! BEEP BOOP. New human registered.",
                "user_id": user_id
            }
        
        except Exception as e:
            # Catch any unexpected errors that we didn't handle above
            # This includes: database errors, encoding issues, disk problems, etc.
            # We log the actual error but show a user-friendly message
            print(f"[ERROR] Registration failed: {str(e)}")  # For debugging
            
            return {
                "success": False,
                "message": "Registration failed. Please try again.",
                "user_id": None
            }
    
    def login(self, username, password):
        """
        Authenticate a user and return their information.
        
        This method includes comprehensive error handling because it's a
        user-facing operation. We're especially careful about error messages
        to avoid leaking information to potential attackers.
        
        Args:
            username (str): Username
            password (str): Plain text password
        
        Returns:
            dict: {"success": bool, "message": str, "user": dict or None}
        
        Example:
            result = user.login("diana", "myPassword123")
            if result["success"]:
                print(f"Welcome, {result['user']['username']}!")
            else:
                print(f"Error: {result['message']}")
        """
        try:
            # Query database for user
            # This could fail if database is locked or corrupted
            users = self.db.execute_query(
                "SELECT id, username, password_hash, created_at FROM users WHERE username = ?",
                (username,)
            )
            
            # Check if user exists
            if not users:
                # Security note: We don't say "user doesn't exist" because that
                # would help attackers figure out valid usernames
                return {
                    "success": False,
                    "message": "Invalid username or password",
                    "user": None
                }
            
            # Get the first (and only) user result
            user_row = users[0]
            
            # Verify password against stored hash
            # This could fail if the hash is corrupted
            if self._verify_password(password, user_row['password_hash']):
                # Password is correct! Return user data (but NOT the password hash)
                return {
                    "success": True,
                    "message": "BEEP BOOP. Login successful! Welcome back, human.",
                    "user": {
                        "id": user_row['id'],
                        "username": user_row['username'],
                        "created_at": user_row['created_at']
                    }
                }
            else:
                # Password is incorrect
                # Security note: Same vague message as above
                return {
                    "success": False,
                    "message": "Invalid username or password",
                    "user": None
                }
        
        except Exception as e:
            # Catch any unexpected errors (database issues, corrupted data, etc.)
            # We log the actual error but show a generic message to users
            print(f"[ERROR] Login failed: {str(e)}")  # For debugging
            
            return {
                "success": False,
                "message": "Login failed. Please try again.",
                "user": None
            }
    
    def get_user_by_id(self, user_id):
        """
        Retrieve user information by ID.
        
        Note: This is an internal method used by other parts of the app,
        not directly by users, so we keep error handling minimal. If it fails,
        we want to see the error during development.
        
        Args:
            user_id (int): User's ID
        
        Returns:
            dict or None: User data without password hash
        """
        users = self.db.execute_query(
            "SELECT id, username, created_at FROM users WHERE id = ?",
            (user_id,)
        )
        
        if users:
            user_row = users[0]
            return {
                "id": user_row['id'],
                "username": user_row['username'],
                "created_at": user_row['created_at']
            }
        
        return None