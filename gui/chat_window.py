# Import sys for system operations
import sys

# Import PyQt6 components for building the chat GUI
from PyQt6.QtWidgets import (
    QMainWindow,       # Main window container
    QWidget,           # Base widget class
    QVBoxLayout,       # Vertical layout manager
    QHBoxLayout,       # Horizontal layout manager
    QTextEdit,         # Multi-line text display (for chat history)
    QLineEdit,         # Single-line text input (for user messages)
    QPushButton,       # Clickable button
    QStatusBar,        # Status bar at bottom
    QMenuBar,          # Menu bar at top
    QMessageBox        # Popup message dialogs
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal  # Core utilities and timer
from PyQt6.QtGui import QAction, QFont  # Actions and fonts


class ChatWindow(QMainWindow):
    """
    Main chat interface window.
    
    This is where users interact with TaskBot through conversation.
    Features:
    - Message display area with bubbles
    - Input field for typing messages
    - Send button
    - Status bar showing username and task count
    - Menu bar with logout option
    """
    
    # Define signal for logout (emitted when user wants to logout)
    logout_requested = pyqtSignal()

    def __init__(self, bot, user_data):
        """
        Initialize chat window.
        
        Args:
            bot (ChatBot): ChatBot instance for processing messages
            user_data (dict): User information from login
        """
        super().__init__()
        
        # Store bot and user data
        self.bot = bot
        self.user_data = user_data
        
        # Setup the window
        self.setWindowTitle(f"TaskBot - Chat ({user_data['username']})")
        self.setGeometry(100, 100, 800, 600)
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create chat display area (shows conversation history)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)  # Users can't edit chat history
        main_layout.addWidget(self.chat_display)
        
        # Create input area (bottom section)
        input_layout = QHBoxLayout()
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here... (e.g., 'add task review code')")
        self.input_field.returnPressed.connect(self._send_message)  # Enter key sends message
        input_layout.addWidget(self.input_field)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self._send_message)
        input_layout.addWidget(self.send_button)
        
        main_layout.addLayout(input_layout)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self._update_status_bar()
        
        # Apply styling
        self._apply_styles()
        
        # Show welcome message
        self._show_welcome_message()
    
    def _create_menu_bar(self):
        """Create the menu bar with options."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        # Logout action
        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self._handle_logout)
        file_menu.addAction(logout_action)
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self._handle_exit)
        file_menu.addAction(exit_action)
        
        # NEW: View menu
        view_menu = menubar.addMenu("View")
        
        # Conversation history action
        history_action = QAction("📜 Conversation History", self)
        history_action.triggered.connect(self._show_history)
        view_menu.addAction(history_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        # Show help action
        help_action = QAction("Show Commands", self)
        help_action.triggered.connect(self._show_help)
        help_menu.addAction(help_action)
    
    def _show_welcome_message(self):
        """Display welcome message when chat opens."""
        welcome = self.bot.process_input("hello")
        self._add_bot_message(welcome)
        
        # Add helpful hint
        hint = "\n💡 Try: 'add task review code' or 'show my tasks' or type 'help'"
        self._add_bot_message(hint)
    
    def _send_message(self):
        """
        Handle sending a message.
        
        Called when user clicks Send button or presses Enter.
        """
        # Get user input
        user_message = self.input_field.text().strip()
        
        # Ignore empty messages
        if not user_message:
            return
        
        # Clear input field
        self.input_field.clear()
        
        # Display user message
        self._add_user_message(user_message)
        
        # Check for logout/goodbye
        if user_message.lower() in ['logout', 'log out']:
            self._handle_logout()
            return
        
        if user_message.lower() in ['goodbye', 'bye', 'exit', 'quit']:
            bot_response = self.bot.process_input(user_message)
            self._add_bot_message(bot_response)
            
            # Close window after short delay
            QTimer.singleShot(1000, self.close)  # 1 second delay
            return
        
        # Process message with bot
        bot_response = self.bot.process_input(user_message)
        
        # Display bot response
        self._add_bot_message(bot_response)
        
        # Update status bar (task count might have changed)
        self._update_status_bar()
        
        # Focus back on input field
        self.input_field.setFocus()
    
    def _add_user_message(self, message):
        """
        Add user message to chat display.
        
        Args:
            message (str): User's message text
        """
        # Import HTML formatting from styles
        from gui.styles import get_user_message_html
        
        # Append formatted message to chat
        self.chat_display.append(get_user_message_html(message))
        
        # Scroll to bottom to show new message
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def _add_bot_message(self, message):
        """
        Add bot message to chat display.
        
        Args:
            message (str): Bot's message text
        """
        # Import HTML formatting from styles
        from gui.styles import get_bot_message_html
        
        # Append formatted message to chat
        self.chat_display.append(get_bot_message_html(message))
        
        # Scroll to bottom to show new message
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def _update_status_bar(self):
        """Update status bar with current user info and task count."""
        # Get task statistics
        stats = self.bot.task_model.get_task_count(self.user_data['id'])
        
        # Build status message
        status_message = f"👤 {self.user_data['username']} | "
        status_message += f"📋 Tasks: {stats['pending']} pending, {stats['completed']} completed"
        
        if stats['high_priority'] > 0:
            status_message += f" | 🔴 {stats['high_priority']} urgent"
        
        # Update status bar with timeout=0 (makes it permanent)
        self.status_bar.showMessage(status_message, 0)
    
    def _show_help(self):
        """Show help dialog with bot commands."""
        help_response = self.bot.process_input("help")
        
        # Show in message box
        QMessageBox.information(self, "TaskBot Help", help_response)

    def _show_history(self):
        """Show conversation history window."""
        # Import the history window
        from gui.history_window import HistoryWindow
        
        # Create and show history window
        history_window = HistoryWindow(
            db_manager=self.bot.db,
            user_id=self.user_data['id'],
            parent=self
        )
        
        # Show as modal dialog (blocks interaction with chat until closed)
        history_window.exec()
    
    def _handle_logout(self):
        """Handle logout action - returns to login window."""
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Logout from bot
            self.bot.logout()
            
            # Emit signal to main app (will show login and close this)
            self.logout_requested.emit()


    def _handle_exit(self):
        """Handle exit action - closes entire application."""
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit TaskBot?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Import QApplication to access quit method
            from PyQt6.QtWidgets import QApplication
            
            # Quit the entire application
            QApplication.quit()
    
    
    def _apply_styles(self):
        """Apply CSS styling to the window."""
        # Import styles from separate file
        from gui.styles import CHAT_WINDOW_STYLE
        
        self.setStyleSheet(CHAT_WINDOW_STYLE)