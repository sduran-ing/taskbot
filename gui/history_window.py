"""
Conversation history window.

Displays past conversations between user and bot.
"""

# Import PyQt6 components
from PyQt6.QtWidgets import (
    QDialog,           # Dialog window (instead of main window)
    QVBoxLayout,       # Vertical layout
    QHBoxLayout,       # Horizontal layout
    QTextEdit,         # Text display area
    QPushButton,       # Buttons
    QLabel,            # Labels
    QMessageBox        # Message dialogs
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class HistoryWindow(QDialog):
    """
    Window showing conversation history.
    
    Displays all past conversations for the current user
    in chronological order (newest first).
    """
    
    def __init__(self, db_manager, user_id, parent=None):
        """
        Initialize history window.
        
        Args:
            db_manager: Database manager instance
            user_id (int): Current user's ID
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        
        self.db = db_manager
        self.user_id = user_id
        
        # Window settings
        self.setWindowTitle("Conversation History")
        self.setMinimumSize(700, 500)
        
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header = QLabel("📜 Your Conversation History")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Display area
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        layout.addWidget(self.display)
        
        # Button bar
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_history)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Apply styling
        self._apply_styles()
        
        # Load conversation history
        self.load_history()
    
    def load_history(self):
        """Load and display conversation history from database."""
        try:
            # Query to get conversations for this user
            query = """
                SELECT user_input, detected_intent, bot_response, timestamp
                FROM conversations
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 100
            """
            
            # Execute query
            conversations = self.db.execute_query(query, (self.user_id,))
            
            if not conversations:
                self.display.setHtml("""
                    <div style='text-align: center; padding: 40px; color: #64748b;'>
                        <h2>No conversations yet</h2>
                        <p>Your conversation history will appear here once you start chatting with TaskBot.</p>
                    </div>
                """)
                return
            
            # Build HTML for display
            html = """
            <style>
                .conversation {
                    margin: 15px 0;
                    padding: 12px;
                    background: #f8fafc;
                    border-left: 3px solid #2563eb;
                    border-radius: 6px;
                }
                .timestamp {
                    color: #64748b;
                    font-size: 12px;
                    margin-bottom: 8px;
                }
                .intent {
                    display: inline-block;
                    background: #dbeafe;
                    color: #1e40af;
                    padding: 2px 8px;
                    border-radius: 4px;
                    font-size: 11px;
                    font-weight: 600;
                    margin-left: 8px;
                }
                .user {
                    color: #0f172a;
                    font-weight: 600;
                    margin: 5px 0;
                }
                .bot {
                    color: #475569;
                    margin: 5px 0;
                    white-space: pre-wrap;
                }
            </style>
            """
            
            html += f"<h3 style='color: #0f172a; margin-bottom: 20px;'>Showing {len(conversations)} recent conversations</h3>"
            
            # Add each conversation
            for conv in conversations:
                user_input = conv['user_input']
                intent = conv['detected_intent']
                bot_response = conv['bot_response']
                timestamp = conv['timestamp']
                
                # Escape HTML in messages
                user_input_safe = user_input.replace('<', '&lt;').replace('>', '&gt;')
                bot_response_safe = bot_response.replace('<', '&lt;').replace('>', '&gt;')
                
                # Format timestamp
                time_display = timestamp.split('.')[0]  # Remove microseconds
                
                html += f"""
                <div class='conversation'>
                    <div class='timestamp'>
                        🕐 {time_display}
                        <span class='intent'>{intent}</span>
                    </div>
                    <div class='user'>👤 You: {user_input_safe}</div>
                    <div class='bot'>🤖 TaskBot: {bot_response_safe}</div>
                </div>
                """
            
            # Set HTML content
            self.display.setHtml(html)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load conversation history:\n{str(e)}"
            )
    
    def _apply_styles(self):
        """Apply styling to the window."""
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QTextEdit {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background-color: #ffffff;
                padding: 10px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)