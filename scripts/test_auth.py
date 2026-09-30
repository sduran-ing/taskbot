"""
Quick manual test to verify database and authentication work.
This is a temporary file for testing - not part of the final app.
"""

from database.db_manager import DatabaseManager
from models.user import User

def test_authentication():
    """Test user registration and login."""
    
    print("🤖 TASKBOT AUTHENTICATION TEST")
    print("=" * 50)
    
    # Initialize database and user model
    db = DatabaseManager('data/taskbot.db')
    user_model = User(db)
    
    # Test 1: Register a new user
    print("\nTEST 1: Registering new user 'testuser'")
    result = user_model.register("testuser", "password123")
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    if result['success']:
        print(f"   User ID: {result['user_id']}")
    
    # Test 2: Try to register duplicate username
    print("\nTEST 2: Trying to register duplicate username")
    result = user_model.register("testuser", "different_password")
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    
    # Test 3: Login with correct password
    print("\nTEST 3: Login with correct password")
    result = user_model.login("testuser", "password123")
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    if result['success']:
        print(f"   User: {result['user']}")
    
    # Test 4: Login with wrong password
    print("\nTEST 4: Login with wrong password")
    result = user_model.login("testuser", "wrong_password")
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    
    # Test 5: Login with non-existent user
    print("\nTEST 5: Login with non-existent user")
    result = user_model.login("fake_user", "password123")
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    
    print("\n" + "=" * 50)
    print(" All tests completed!")

if __name__ == "__main__":
    test_authentication()