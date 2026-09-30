"""
Response templates for TaskBot personality.

This file contains all text responses separated from logic.
Makes it easy to:
- Change bot personality
- Support multiple languages
- A/B test different tones
- Let non-developers edit responses

To change bot personality: Just edit this file!
"""

# =============================================================================
# GREETINGS
# =============================================================================

GREETINGS = [
    "BEEP BOOP! Hello, human! 🤖",
    "Greetings! This unit is ready to assist! 🤖",
    "Hello there! Robot assistant activated! ⚡",
    "BEEP! Greetings, human user! How may this unit serve?",
    "Hi! TaskBot online and ready! 🤖",
]

# =============================================================================
# GOODBYES
# =============================================================================

GOODBYES = [
    "BEEP BOOP! Goodbye, human! TaskBot shutting down... 👋",
    "Farewell! This unit enjoyed assisting you! 🤖",
    "Goodbye! TaskBot entering standby mode... ⚡",
    "BEEP! Until next time, human! 👋",
    "See you later! TaskBot signing off! 🤖",
]

# =============================================================================
# LOGOUT
# =============================================================================

LOGOUT_MESSAGE = "BEEP BOOP! Logging out... See you next time! 👋"

# =============================================================================
# FALLBACK RESPONSES
# =============================================================================

FALLBACK_RESPONSES = [
    "BEEP BOOP? I didn't quite understand that. Try 'help' to see what I can do! 🤔",
    "ERROR: Command not recognized. Type 'help' for available commands. 🤖",
    "Hmm, this unit is confused. Could you rephrase that? Type 'help' for guidance. 💭",
    "BEEP? I'm not sure what you mean. Try asking differently or type 'help'. 🔧",
]

# =============================================================================
# HELP MESSAGE
# =============================================================================

HELP_MESSAGE = """
🤖 BEEP BOOP! TaskBot Capabilities:

📝 Task Management:
   • "add task [description]" - Create a new task
   • "show my tasks" - List all tasks
   • "complete task [id]" - Mark task as done
   • "delete task [id]" - Remove a task
   
⚙️ Organization:
   • "set task [id] priority [low/medium/high]" - Set priority
   • "show completed tasks" - View finished tasks
   • "show pending tasks" - View active tasks
   • "show high priority tasks" - View urgent tasks
   
📊 Statistics:
   • "how many tasks" - Get task summary
   • "task count" - View statistics
   
🔧 System:
   • "help" - Show this message
   • "logout" - Switch user
   • "goodbye" - Exit

BEEP BOOP! Ready to assist! 🤖
"""

# =============================================================================
# TASK CREATED
# =============================================================================

TASK_CREATED_TEMPLATES = [
    "BEEP BOOP! Task created successfully! 🎉\n\n📋 Task #{id}: {title}\n   Priority: {priority} | Status: {status}",
    "✅ Task registered in memory banks!\n\n📋 Task #{id}: {title}\n   Priority: {priority}",
    "BEEP! New task added to your list! 🤖\n\n📋 Task #{id}: {title}\n   Priority: {priority} | Status: {status}",
]

# =============================================================================
# TASK COMPLETED
# =============================================================================

TASK_COMPLETED_TEMPLATES = [
    "BEEP BOOP! 🎉 Task #{id} marked as completed! Great work, human!",
    "✅ Task #{id} complete! This unit is proud of your productivity! 🤖",
    "BEEP! Task #{id} finished! One step closer to total task domination! 💪",
    "🎊 Task #{id} completed successfully! Keep up the good work!",
]

# =============================================================================
# TASK DELETED
# =============================================================================

TASK_DELETED_TEMPLATES = [
    "BEEP BOOP! 🗑️ Task #{id} has been deleted from memory banks!",
    "✅ Task #{id} removed successfully! Deletion complete! 🤖",
    "BEEP! Task #{id} erased! *poof* Gone! ✨",
]

# =============================================================================
# PRIORITY UPDATED
# =============================================================================

PRIORITY_UPDATED_TEMPLATES = [
    "BEEP BOOP! 🎯 Task #{id} priority updated to {priority}!",
    "✅ Priority set! Task #{id} is now {priority} priority! 🤖",
    "BEEP! Task #{id} priority level adjusted to {priority}! ⚡",
]

# =============================================================================
# TASK LIST HEADERS
# =============================================================================

TASK_LIST_NO_TASKS_FILTERED = "BEEP! No {filter_type} tasks found. Your list is clear! ✨"
TASK_LIST_NO_TASKS = "BEEP BOOP! No tasks found. Ready to add some? 📋"
TASK_LIST_HEADER_FILTERED = "🤖 BEEP! Here are your {filter_type} tasks:\n"
TASK_LIST_HEADER = "🤖 BEEP! Here are your tasks ({count} total):\n"

# =============================================================================
# TASK STATS MESSAGES
# =============================================================================

TASK_STATS_ALL_COMPLETE = "🎉 All tasks complete! This unit is impressed!"
TASK_STATS_HIGH_PRIORITY = "⚡ You have urgent tasks! Time to prioritize, human!"
TASK_STATS_KEEP_GOING = "💪 Keep up the good work!"

# =============================================================================
# ERROR & CLARIFICATION
# =============================================================================

ERROR_TEMPLATE = "⚠️ BEEP! Error encountered:\n{message}\n\nPlease try again or type 'help' for assistance. 🤖"

CLARIFICATION_HEADER = "🤔 BEEP? I'm not quite sure what you want. Did you mean:\n\n"
CLARIFICATION_FOOTER = "\nPlease rephrase or type the number of your choice. 🤖"