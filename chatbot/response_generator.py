# Import random - Python's built-in module for generating random choices
# Used for: Picking random variations of responses to make the bot feel more natural
import random


class ResponseGenerator:
    """
    Generates responses with quirky robot personality.
    
    This class takes plain data and converts it into engaging,
    personality-filled responses that make the bot feel alive.
    
    Personality traits:
    - Enthusiastic about helping ("BEEP BOOP!")
    - Uses robot-themed expressions
    - Occasionally uses emojis
    - Professional but playful
    """
    
    def __init__(self):
        """Initialize response generator with personality templates."""
        
        # Greeting variations - randomly selected to feel natural
        self.greetings = [
            "BEEP BOOP! Hello, human! 🤖",
            "Greetings! This unit is ready to assist! 🤖",
            "Hello there! Robot assistant activated! ⚡",
            "BEEP! Greetings, human user! How may this unit serve?",
            "Hi! TaskBot online and ready! 🤖",
        ]
        
        # Help message - explains what the bot can do
        self.help_message = """
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
        
        # Goodbye variations
        self.goodbyes = [
            "BEEP BOOP! Goodbye, human! TaskBot shutting down... 👋",
            "Farewell! This unit enjoyed assisting you! 🤖",
            "Goodbye! TaskBot entering standby mode... ⚡",
            "BEEP! Until next time, human! 👋",
            "See you later! TaskBot signing off! 🤖",
        ]
        
        # Fallback responses when intent is unclear
        self.fallback_responses = [
            "BEEP BOOP? I didn't quite understand that. Try 'help' to see what I can do! 🤔",
            "ERROR: Command not recognized. Type 'help' for available commands. 🤖",
            "Hmm, this unit is confused. Could you rephrase that? Type 'help' for guidance. 💭",
            "BEEP? I'm not sure what you mean. Try asking differently or type 'help'. 🔧",
        ]
    
    def generate_greeting(self):
        """
        Generate a random greeting response.
        
        Returns:
            str: A greeting message with robot personality
        """
        return random.choice(self.greetings)
    
    def generate_help(self):
        """
        Generate help message.
        
        Returns:
            str: Complete help documentation
        """
        return self.help_message
    
    def generate_goodbye(self):
        """
        Generate a random goodbye response.
        
        Returns:
            str: A farewell message with robot personality
        """
        return random.choice(self.goodbyes)
    
    def generate_logout(self):
        """
        Generate logout confirmation message.
        
        Returns:
            str: Logout message
        """
        return "BEEP BOOP! Logging out... See you next time! 👋"
    
    def generate_fallback(self):
        """
        Generate a fallback response for unclear input.
        
        Returns:
            str: A helpful fallback message
        """
        return random.choice(self.fallback_responses)
    
    def generate_task_created(self, task):
        """
        Generate response for successful task creation.
        
        Args:
            task (dict): Task details from Task.create_task()
        
        Returns:
            str: Success message with task details
        """
        responses = [
            f"BEEP BOOP! Task created successfully! 🎉\n\n📋 Task #{task['id']}: {task['title']}\n   Priority: {task['priority']} | Status: {task['status']}",
            f"✅ Task registered in memory banks!\n\n📋 Task #{task['id']}: {task['title']}\n   Priority: {task['priority']}",
            f"BEEP! New task added to your list! 🤖\n\n📋 Task #{task['id']}: {task['title']}\n   Priority: {task['priority']} | Status: {task['status']}",
        ]
        return random.choice(responses)
    
    def generate_task_list(self, tasks, filter_type=None):
        """
        Generate response for listing tasks.
        
        Args:
            tasks (list): List of task dictionaries
            filter_type (str, optional): Type of filter applied (e.g., "completed", "high priority")
        
        Returns:
            str: Formatted task list
        """
        if not tasks:
            if filter_type:
                return f"BEEP! No {filter_type} tasks found. Your list is clear! ✨"
            else:
                return "BEEP BOOP! No tasks found. Ready to add some? 📋"
        
        # Build header
        if filter_type:
            header = f"🤖 BEEP! Here are your {filter_type} tasks:\n"
        else:
            header = f"🤖 BEEP! Here are your tasks ({len(tasks)} total):\n"
        
        # Build task list
        task_list = header + "=" * 50 + "\n\n"
        
        for task in tasks:
            # Status emoji
            status_emoji = "✅" if task['status'] == 'completed' else "⏳"
            
            # Priority indicator
            if task['priority'] == 'high':
                priority_emoji = "🔴"
            elif task['priority'] == 'medium':
                priority_emoji = "🟡"
            else:
                priority_emoji = "🟢"
            
            # Format task line
            task_list += f"{status_emoji} Task #{task['id']}: {task['title']}\n"
            task_list += f"   {priority_emoji} Priority: {task['priority']} | Status: {task['status']}\n\n"
        
        task_list += "=" * 50
        return task_list
    
    def generate_task_completed(self, task_id):
        """
        Generate response for task completion.
        
        Args:
            task_id (int): ID of completed task
        
        Returns:
            str: Success message
        """
        responses = [
            f"BEEP BOOP! 🎉 Task #{task_id} marked as completed! Great work, human!",
            f"✅ Task #{task_id} complete! This unit is proud of your productivity! 🤖",
            f"BEEP! Task #{task_id} finished! One step closer to total task domination! 💪",
            f"🎊 Task #{task_id} completed successfully! Keep up the good work!",
        ]
        return random.choice(responses)
    
    def generate_task_deleted(self, task_id):
        """
        Generate response for task deletion.
        
        Args:
            task_id (int): ID of deleted task
        
        Returns:
            str: Success message
        """
        responses = [
            f"BEEP BOOP! 🗑️ Task #{task_id} has been deleted from memory banks!",
            f"✅ Task #{task_id} removed successfully! Deletion complete! 🤖",
            f"BEEP! Task #{task_id} erased! *poof* Gone! ✨",
        ]
        return random.choice(responses)
    
    def generate_priority_updated(self, task_id, priority):
        """
        Generate response for priority update.
        
        Args:
            task_id (int): Task ID
            priority (str): New priority level
        
        Returns:
            str: Success message
        """
        responses = [
            f"BEEP BOOP! 🎯 Task #{task_id} priority updated to {priority}!",
            f"✅ Priority set! Task #{task_id} is now {priority} priority! 🤖",
            f"BEEP! Task #{task_id} priority level adjusted to {priority}! ⚡",
        ]
        return random.choice(responses)
    
    def generate_task_count(self, stats):
        """
        Generate response for task statistics.
        
        Args:
            stats (dict): Statistics from Task.get_task_count()
                {
                    "total": int,
                    "pending": int,
                    "completed": int,
                    "high_priority": int
                }
        
        Returns:
            str: Formatted statistics
        """
        response = "📊 BEEP BOOP! Task Statistics:\n"
        response += "=" * 50 + "\n\n"
        response += f"📋 Total Tasks: {stats['total']}\n"
        response += f"⏳ Pending: {stats['pending']}\n"
        response += f"✅ Completed: {stats['completed']}\n"
        response += f"🔴 High Priority: {stats['high_priority']}\n\n"
        
        # Add motivational message based on stats
        if stats['pending'] == 0:
            response += "🎉 All tasks complete! This unit is impressed!"
        elif stats['high_priority'] > 0:
            response += "⚡ You have urgent tasks! Time to prioritize, human!"
        else:
            response += "💪 Keep up the good work!"
        
        response += "\n" + "=" * 50
        return response
    
    def generate_error(self, message):
        """
        Generate user-friendly error message.
        
        Args:
            message (str): Error message from the system
        
        Returns:
            str: Formatted error with robot personality
        """
        return f"⚠️ BEEP! Error encountered:\n{message}\n\nPlease try again or type 'help' for assistance. 🤖"
    
    def generate_clarification(self, alternatives):
        """
        Generate clarification request when intent is unclear.
        
        Args:
            alternatives (list): List of (intent, probability) tuples
        
        Returns:
            str: Message asking user to clarify
        """
        response = "🤔 BEEP? I'm not quite sure what you want. Did you mean:\n\n"
        
        for i, (intent, prob) in enumerate(alternatives[:3], 1):
            # Convert intent names to readable format
            readable = intent.replace('_', ' ').title()
            response += f"{i}. {readable}\n"
        
        response += "\nPlease rephrase or type the number of your choice. 🤖"
        return response