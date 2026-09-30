"""
Test the login window GUI.

This script launches just the login window to test styling and functionality.

Run from project root:
    py scripts/test_login_gui.py
"""

# Import sys and os for path handling
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import PyQt6 application class
from PyQt6.QtWidgets import QApplication

# Import our components
from chatbot.bot_logic import ChatBot
from gui.login_window import LoginWindow


def test_login_window():
    """Launch the login window for testing."""
    
    print("🤖 Launching TaskBot Login Window...")
    print("=" * 70)
    
    # Create PyQt application
    # Every PyQt app needs exactly one QApplication instance
    app = QApplication(sys.argv)
    
    # Initialize bot
    bot = ChatBot()
    
    # Create login window
    login_window = LoginWindow(bot)
    
    # Connect signal to see when login succeeds
    def on_login(user_data):
        print(f"\n✅ Login successful!")
        print(f"   User: {user_data['username']}")
        print(f"   User ID: {user_data['id']}")
        print("\n💡 Close the window to exit test.\n")
    
    login_window.login_successful.connect(on_login)
    
    # Show the window
    login_window.show()
    
    # Start the application event loop
    # This keeps the window open until closed
    sys.exit(app.exec())


if __name__ == "__main__":
    test_login_window()