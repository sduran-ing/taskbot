"""
PyQt6 stylesheet definitions for TaskBot.

Inspired by modern chat UIs with clean blue theme.
"""

# =============================================================================
# COLOR PALETTE - Modern Blue Theme
# =============================================================================

# Primary colors
PRIMARY_BLUE = "#2563eb"       # Tailwind blue-600 (main action color)
PRIMARY_DARK = "#1e40af"       # Darker blue for pressed states
PRIMARY_LIGHT = "#dbeafe"      # Very light blue for backgrounds

# Neutral colors
BACKGROUND = "#f7f9fc"         # Off-white app background
WHITE = "#ffffff"              # Pure white
TEXT_DARK = "#0f172a"          # Almost black (slate-900)
TEXT_MUTED = "#64748b"         # Gray text (slate-500)
BORDER = "#e5e7eb"             # Light gray border

# Message bubble colors
USER_BUBBLE_BG = "#2563eb"     # Blue for user messages
USER_TEXT = "#ffffff"          # White text on blue
BOT_BUBBLE_BG = "#ffffff"      # White for bot messages
BOT_TEXT = "#0f172a"           # Dark text on white
BOT_BORDER = "#e5e7eb"         # Subtle border for bot bubbles

# Status colors
SUCCESS = "#10b981"            # Green
ERROR = "#ef4444"              # Red
WARNING = "#f59e0b"            # Orange

# =============================================================================
# LOGIN WINDOW STYLES
# =============================================================================

LOGIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {BACKGROUND};
    }}
    
    QLabel {{
        color: {TEXT_DARK};
    }}
    
    QLineEdit {{
        padding: 12px;
        border: 2px solid {BORDER};
        border-radius: 10px;
        font-size: 18px;
        background-color: {WHITE};
        color: {TEXT_DARK};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {PRIMARY_BLUE};
    }}
    
    QPushButton {{
        padding: 12px;
        background-color: {PRIMARY_BLUE};
        color: {WHITE};
        border: none;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }}
    
    QPushButton:hover {{
        background-color: #1d4ed8;
    }}
    
    QPushButton:pressed {{
        background-color: {PRIMARY_DARK};
    }}
"""

# =============================================================================
# CHAT WINDOW STYLES
# =============================================================================

CHAT_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {WHITE};
    }}
    
    /* Chat area background */
    QTextEdit {{
        background-color: {BACKGROUND};
        border: none;
        font-size: 18px;
        font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    }}
    
    /* Input field */
    QLineEdit {{
        padding: 12px 16px;
        border: 1px solid {BORDER};
        border-radius: 12px;
        font-size: 18px;
        background-color: {WHITE};
        color: {TEXT_DARK};
    }}
    
    QLineEdit:focus {{
        border: 1px solid {PRIMARY_BLUE};
    }}
    
    /* Send button */
    QPushButton {{
        padding: 12px 24px;
        background-color: {PRIMARY_BLUE};
        color: {WHITE};
        border: none;
        border-radius: 10px;
        font-size: 18px;
        font-weight: 600;
    }}
    
    QPushButton:hover {{
        background-color: #1d4ed8;
    }}
    
    QPushButton:pressed {{
        background-color: {PRIMARY_DARK};
    }}
    
    /* Status bar */
    QStatusBar {{
        background-color: {WHITE};
        color: {TEXT_DARK};
        border-top: 1px solid {BORDER};
        font-size: 18px;
        padding: 4px 8px;
    }}
    
    /* Menu bar */
    QMenuBar {{
        background-color: {WHITE};
        border-bottom: 1px solid {BORDER};
        padding: 4px;
    }}
    
    QMenuBar::item {{
        padding: 8px 12px;
        background-color: transparent;
        border-radius: 6px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {PRIMARY_LIGHT};
    }}
    
    QMenu {{
        background-color: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 4px;
    }}
    
    QMenu::item {{
        padding: 8px 12px;
        border-radius: 6px;
    }}
    
    QMenu::item:selected {{
        background-color: {PRIMARY_LIGHT};
    }}
"""

# =============================================================================
# MESSAGE BUBBLE STYLES (HTML/CSS for QTextEdit)
# Inspired by modern chat applications like iMessage, WhatsApp
# =============================================================================

def get_user_message_html(message):
    """
    Generate HTML for user message bubble (blue, right-aligned).
    
    Args:
        message (str): User's message text
    
    Returns:
        str: HTML formatted message with modern styling
    """
    # Escape HTML special characters
    message = message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    return f"""
    <div style="text-align: right; margin: 8px 12px;">
        <div style="display: inline-block; 
                    background: {USER_BUBBLE_BG}; 
                    color: {USER_TEXT}; 
                    padding: 10px 14px; 
                    border-radius: 18px; 
                    max-width: 65%;
                    text-align: left;
                    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
                    font-family: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
                    font-size: 18px;
                    line-height: 1.4;
                    word-wrap: break-word;">
            {message}
        </div>
    </div>
    """

def get_bot_message_html(message):
    """
    Generate HTML for bot message bubble (white with border, left-aligned).
    
    Args:
        message (str): Bot's message text
    
    Returns:
        str: HTML formatted message with modern styling
    """
    # Escape HTML special characters but preserve newlines
    message = message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    message = message.replace('\n', '<br>')
    
    return f"""
    <div style="text-align: left; margin: 8px 12px;">
        <div style="display: inline-block; 
                    background: {BOT_BUBBLE_BG}; 
                    color: {BOT_TEXT}; 
                    padding: 10px 14px; 
                    border-radius: 18px; 
                    max-width: 65%;
                    text-align: left;
                    border: 1px solid {BOT_BORDER};
                    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
                    font-family: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
                    font-size: 18px;
                    line-height: 1.4;
                    word-wrap: break-word;">
            <span style="font-weight: 600; margin-right: 6px;">🤖</span>{message}
        </div>
    </div>
    """