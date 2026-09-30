"""
TaskBot - AI-Powered Task Management Assistant

Main application entry point.
Manages window transitions: Login → Chat → Login (on logout)

Run:
    py main.py
"""

# Import sys for system operations and application management
import sys

# Import PyQt6 application class
from PyQt6.QtWidgets import QApplication

# Import our components
from chatbot.bot_logic import ChatBot
from gui.login_window import LoginWindow
from gui.chat_window import ChatWindow


class TaskBotApp:
    """
    Main application controller.
    
    Manages the application lifecycle and window transitions:
    1. Shows login window
    2. On successful login → Shows chat window
    3. On logout → Shows login window (keeps app running)
    4. On exit → Closes app completely
    """
    
    def __init__(self):
        """Initialize the application."""
        # Create PyQt application
        self.app = QApplication(sys.argv)
        
        # Set application-wide properties
        self.app.setApplicationName("TaskBot")
        self.app.setOrganizationName("TaskBot")
        
        # Initialize bot (shared across all windows)
        self.bot = ChatBot()
        
        # Window references
        self.login_window = None
        self.chat_window = None
        
        # Flag to track if we're logging out (vs exiting)
        self.is_logging_out = False
        
        # Show login window to start
        self.show_login_window()
    
    def show_login_window(self):
        """Display the login window."""
        # Create login window
        self.login_window = LoginWindow(self.bot)
        
        # Connect login success signal to show chat window
        self.login_window.login_successful.connect(self.show_chat_window)
        
        # Show the window
        self.login_window.show()
    
    def show_chat_window(self, user_data):
        """
        Display the chat window after successful login.
        
        Args:
            user_data (dict): User information from login
        """
        # Hide login window (don't close it yet)
        if self.login_window:
            self.login_window.hide()
        
        # Create chat window
        self.chat_window = ChatWindow(self.bot, user_data)
        
        # Connect logout signal
        self.chat_window.logout_requested.connect(self.handle_logout)
        
        # Show the window
        self.chat_window.show()
    
    def handle_logout(self):
        """
        Handle logout request from chat window.
        
        Shows login window before closing chat.
        """
        # Close chat window
        if self.chat_window:
            self.chat_window.close()
            self.chat_window = None
        
        # Show login window again
        self.show_login_window()
    
    def run(self):
        """
        Start the application event loop.
        
        Returns:
            int: Exit code (0 for normal exit)
        """
        return self.app.exec()


def main():
    """
    Main entry point for TaskBot application.
    
    Creates and runs the application.
    """
    print("=" * 70)
    print("🤖 TASKBOT - AI-Powered Task Management")
    print("=" * 70)
    print("\n⏳ Initializing application...")
    
    try:
        # Create and run application
        app = TaskBotApp()
        
        print("✅ Application initialized!")
        print("📱 GUI launched - check your screen!")
        print("\n💡 Close all windows to exit.\n")
        print("=" * 70 + "\n")
        
        # Run application (blocks until exit)
        exit_code = app.run()
        
        print("\n" + "=" * 70)
        print("👋 TaskBot shutting down...")
        print("=" * 70)
        
        sys.exit(exit_code)
    
    except Exception as e:
        print(f"\n❌ ERROR: Application failed to start!")
        print(f"   {str(e)}")
        print("\n💡 Make sure:")
        print("   1. All files are in correct locations")
        print("   2. Virtual environment is activated")
        print("   3. Requirements are installed: pip install -r requirements.txt")
        print("   4. Model is trained: py scripts/train_model.py\n")
        sys.exit(1)


if __name__ == "__main__":
    main()