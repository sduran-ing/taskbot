# Import re - Regular expression library for pattern matching and text extraction
import re


class EntityExtractor:
    """
    Extracts entities (task IDs, priorities, status) from user input.
    
    Entities are specific pieces of information within the text:
    - Task IDs: numbers that refer to specific tasks
    - Priorities: low, medium, high
    - Status: pending, completed
    
    Example:
        "complete task 5" → task_id: 5
        "set priority high" → priority: "high"
        "show completed tasks" → status: "completed"
    """
    
    def __init__(self):
        """Initialize the entity extractor with pattern definitions."""
        
        # Define valid values for different entity types
        self.valid_priorities = ['low', 'medium', 'high', 'urgent', 'important']
        self.valid_statuses = ['pending', 'completed', 'done', 'finished']
        
        # Map alternative words to standard values
        # This helps handle variations in how users express things
        self.priority_mapping = {
            'urgent': 'high',
            'important': 'high',
            'low': 'low',
            'medium': 'medium',
            'high': 'high'
        }
        
        self.status_mapping = {
            'pending': 'pending',
            'completed': 'completed',
            'done': 'completed',
            'finished': 'completed'
        }
    
    def extract_task_id(self, text):
        """
        Extract task ID (number) from text.
        
        Looks for patterns like:
        - "task 5"
        - "task number 3"
        - "task id 7"
        - Just a number: "complete 5"
        
        Args:
            text (str): User input text
        
        Returns:
            int or None: Extracted task ID, or None if not found
        
        Example:
            extract_task_id("complete task 5") → 5
            extract_task_id("delete 3") → 3
            extract_task_id("show my tasks") → None
        """
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Pattern 1: "task [number/id/num] X" or "task X"
        # Examples: "task 5", "task number 3", "task id 7"
        pattern1 = r'task\s+(?:number|id|num|#)?\s*(\d+)'
        match = re.search(pattern1, text_lower)
        if match:
            return int(match.group(1))
        
        # Pattern 2: Just a standalone number
        # Examples: "complete 5", "delete 3"
        # Only extract if it's a reasonable task ID (1-9999)
        pattern2 = r'\b(\d{1,4})\b'
        match = re.search(pattern2, text_lower)
        if match:
            task_id = int(match.group(1))
            # Only return if it looks like a task ID (not a year or large number)
            if 1 <= task_id <= 9999:
                return task_id
        
        # No task ID found
        return None
    
    def extract_priority(self, text):
        """
        Extract priority level from text.
        
        Looks for words like: low, medium, high, urgent, important
        
        Args:
            text (str): User input text
        
        Returns:
            str or None: Extracted priority ('low', 'medium', 'high'), or None
        
        Example:
            extract_priority("make it high priority") → "high"
            extract_priority("urgent task") → "high"
            extract_priority("set priority low") → "low"
        """
        # Convert to lowercase
        text_lower = text.lower()
        
        # Check for each valid priority word
        for priority in self.valid_priorities:
            # Use word boundaries \b to match whole words only
            # This prevents matching "highlight" when looking for "high"
            pattern = r'\b' + priority + r'\b'
            if re.search(pattern, text_lower):
                # Map to standard value
                return self.priority_mapping[priority]
        
        # No priority found
        return None
    
    def extract_status(self, text):
        """
        Extract status from text.
        
        Looks for words like: pending, completed, done, finished
        
        Args:
            text (str): User input text
        
        Returns:
            str or None: Extracted status ('pending', 'completed'), or None
        
        Example:
            extract_status("show completed tasks") → "completed"
            extract_status("pending tasks") → "pending"
            extract_status("what's done") → "completed"
        """
        # Convert to lowercase
        text_lower = text.lower()
        
        # Check for each valid status word
        for status in self.valid_statuses:
            # Use word boundaries to match whole words
            pattern = r'\b' + status + r'\b'
            if re.search(pattern, text_lower):
                # Map to standard value
                return self.status_mapping[status]
        
        # No status found
        return None
    
    def extract_task_title(self, text, intent):
        """
        Extract task title from create_task intent.
        
        Removes command words AND priority/status keywords to get clean title.
        
        Args:
            text (str): User input text
            intent (str): Detected intent
        
        Returns:
            str or None: Extracted task title, or None if not create_task intent
        
        Example:
            extract_task_title("add task lunch urgent", "create_task") 
            → "lunch" (removed "add task" and "urgent")
        """
        # Only extract title for create_task intent
        if intent != 'create_task':
            return None
        
        # Remove common command phrases
        command_phrases = [
            r'add\s+tasks?:?\s*',      # Matches "add task" or "add tasks"
            r'create\s+tasks?:?\s*',   # Matches "create task" or "create tasks"
            r'new\s+tasks?:?\s*',      # Matches "new task" or "new tasks"
            r'make\s+tasks?:?\s*',     # Matches "make task" or "make tasks"
            r'add\s+a\s+task:?\s*',
            r'create\s+a\s+task:?\s*',
            r'add\s+new\s+tasks?:?\s*',
            r'create\s+new\s+tasks?:?\s*',
            r'add\s+',
            r'create\s+',
        ]
        
        # Start with original text
        title = text
        
        # Remove each command phrase
        for phrase in command_phrases:
            title = re.sub(phrase, '', title, flags=re.IGNORECASE)
        
        # Remove priority keywords from title
        priority_words = [
            'urgent', 'important', 'high', 'medium', 'low',
            'high priority', 'low priority', 'medium priority',
            'priority high', 'priority low', 'priority medium'
        ]
        for word in priority_words:
            # Use word boundaries to match whole words only
            pattern = r'\b' + re.escape(word) + r'\b'
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
        
        # Remove status keywords from title
        status_words = ['pending', 'completed', 'done', 'finished']
        for word in status_words:
            pattern = r'\b' + word + r'\b'
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
        
        # Clean up: strip whitespace and remove extra spaces
        title = title.strip()
        title = re.sub(r'\s+', ' ', title)
        
        # Return None if title is empty after cleaning
        if not title:
            return None
        
        return title
    
    def extract_all(self, text, intent):
        """
        Extract all entities from text in one call.
        
        Convenience method that extracts all possible entities.
        
        Args:
            text (str): User input text
            intent (str): Detected intent
        
        Returns:
            dict: {
                "task_id": int or None,
                "priority": str or None,
                "status": str or None,
                "task_title": str or None
            }
        
        Example:
            extract_all("set task 5 priority high", "set_priority")
            → {"task_id": 5, "priority": "high", "status": None, "task_title": None}
        """
        return {
            "task_id": self.extract_task_id(text),
            "priority": self.extract_priority(text),
            "status": self.extract_status(text),
            "task_title": self.extract_task_title(text, intent)
        }