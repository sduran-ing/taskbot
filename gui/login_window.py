# Import sys for application management
import sys

# Import PyQt6 components for building the GUI
from PyQt6.QtWidgets import (
    QApplication,      # Main application object
    QMainWindow,       # Main window container
    QWidget,           # Base widget class
    QVBoxLayout,       # Vertical layout manager
    QHBoxLayout,       # Horizontal layout manager
    QLabel,            # Text label widget
    QLineEdit,         # Single-line text input
    QPushButton,       # Clickable button
    QMessageBox,       # Popup message dialogs
    QStackedWidget     # Widget that shows one page at a time
)
from PyQt6.QtCore import Qt, pyqtSignal  # Core utilities and signal system
from PyQt6.QtGui import QFont           # Font styling


class LoginWindow(QMainWindow):
    """
    Login and registration window.
    
    This is the first window users see. It provides:
    - Login form
    - Registration form
    - Toggle between the two
    
    Signals:
        login_successful: Emitted when user logs in successfully
                         Carries user data dictionary
    """
    
    # Define signal that will be emitted when login succeeds
    # This allows other windows to know when to show up
    login_successful = pyqtSignal(dict)
    
    def __init__(self, bot):
        """
        Initialize login window.
        
        Args:
            bot (ChatBot): ChatBot instance for authentication
        """
        super().__init__()
        
        # Store bot reference for authentication
        self.bot = bot
        
        # Setup the window
        self.setWindowTitle("TaskBot - Login")
        self.setFixedSize(400, 500)
        
        # Create and set central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Create stacked widget to switch between login and register
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Create login and register pages
        self.login_page = self._create_login_page()
        self.register_page = self._create_register_page()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        
        # Start with login page
        self.stacked_widget.setCurrentWidget(self.login_page)
        
        # Apply styling
        self._apply_styles()
    
    def _create_login_page(self):
        """
        Create the login page layout.
        
        Returns:
            QWidget: Login page widget
        """
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Add spacing at top
        layout.addStretch()
        
        # Title
        title = QLabel("🤖 TaskBot")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("BEEP BOOP! Please login")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Arial", 10))
        layout.addWidget(subtitle)
        
        # Add spacing
        layout.addSpacing(30)
        
        # Username field
        username_label = QLabel("Username:")
        layout.addWidget(username_label)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter username")
        layout.addWidget(self.login_username)
        
        # Password field
        password_label = QLabel("Password:")
        layout.addWidget(password_label)
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter password")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password
        layout.addWidget(self.login_password)
        
        # Add spacing
        layout.addSpacing(20)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self._handle_login)
        layout.addWidget(login_btn)
        
        # Add spacing
        layout.addSpacing(10)
        
        # Switch to register button
        switch_btn = QPushButton("Don't have an account? Register")
        switch_btn.clicked.connect(self._show_register_page)
        layout.addWidget(switch_btn)
        
        # Add spacing at bottom
        layout.addStretch()
        
        return page
    
    def _create_register_page(self):
        """
        Create the registration page layout.
        
        Returns:
            QWidget: Register page widget
        """
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # Add spacing at top
        layout.addStretch()
        
        # Title
        title = QLabel("🤖 TaskBot")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Register new account")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Arial", 10))
        layout.addWidget(subtitle)
        
        # Add spacing
        layout.addSpacing(30)
        
        # Username field
        username_label = QLabel("Username:")
        layout.addWidget(username_label)
        
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose username")
        layout.addWidget(self.register_username)
        
        # Password field
        password_label = QLabel("Password:")
        layout.addWidget(password_label)
        
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Choose password (min 6 characters)")
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.register_password)
        
        # Confirm password field
        confirm_label = QLabel("Confirm Password:")
        layout.addWidget(confirm_label)
        
        self.register_confirm = QLineEdit()
        self.register_confirm.setPlaceholderText("Confirm password")
        self.register_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.register_confirm)
        
        # Add spacing
        layout.addSpacing(20)
        
        # Register button
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self._handle_register)
        layout.addWidget(register_btn)
        
        # Add spacing
        layout.addSpacing(10)
        
        # Switch to login button
        switch_btn = QPushButton("Already have an account? Login")
        switch_btn.clicked.connect(self._show_login_page)
        layout.addWidget(switch_btn)
        
        # Add spacing at bottom
        layout.addStretch()
        
        return page
    
    def _show_register_page(self):
        """Switch to registration page."""
        self.stacked_widget.setCurrentWidget(self.register_page)
    
    def _show_login_page(self):
        """Switch to login page."""
        self.stacked_widget.setCurrentWidget(self.login_page)
    
    def _handle_login(self):
        """Handle login button click."""
        # Get input values
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        # Validate inputs
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return
        
        # Attempt login
        result = self.bot.login(username, password)
        
        if result['success']:
            # Login successful - emit signal with user data
            self.login_successful.emit(result['user'])
            
            # Close this window
            self.close()
        else:
            # Login failed - show error
            QMessageBox.warning(self, "Login Failed", result['message'])
    
    def _handle_register(self):
        """Handle register button click."""
        # Get input values
        username = self.register_username.text().strip()
        password = self.register_password.text()
        confirm = self.register_confirm.text()
        
        # Validate inputs
        if not username or not password or not confirm:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        
        # Check passwords match
        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        
        # Attempt registration
        result = self.bot.register(username, password)
        
        if result['success']:
            # Registration successful - show message
            QMessageBox.information(
                self, 
                "Success", 
                "Registration successful! You can now login."
            )
            
            # Switch to login page and pre-fill username
            self.login_username.setText(username)
            self._show_login_page()
        else:
            # Registration failed - show error
            QMessageBox.warning(self, "Registration Failed", result['message'])
    
    def _apply_styles(self):
        """Apply CSS styling to the window."""
        # Import styles from separate file
        from gui.styles import LOGIN_WINDOW_STYLE
        
        self.setStyleSheet(LOGIN_WINDOW_STYLE)