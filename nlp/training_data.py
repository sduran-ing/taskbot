"""
Training data for intent classification.

This file contains example utterances (things users might say) for each intent.
The more examples we provide, the better the classifier learns.

Structure: Each intent has a list of example phrases that should trigger it.
"""

TRAINING_DATA = {
    "greeting": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "sup",
        "what's up",
        "howdy",
        "greetings",
        "yo",
        "hi there",
        "hello there",
        "hey there",
        "morning",
        "afternoon",
        "evening",
        "hiya",
        "heya",
        "whats up",
    ],
    
    "create_task": [
        "add task",
        "create task",
        "new task",
        "add a task",
        "create a new task",
        "I need to add a task",
        "can you add a task",
        "make a task",
        "add this to my list",
        "create new task",
        "add item",
        "new item",
        "add to do",
        "create to do",
        "I want to create a task",
        "add task called",
        "make task",
        "add new task",
        "create task for",
        "need to add task",
        "want to add task",
        "make new task",
        "add something to my list",
        "create something for me",
        "add to my tasks",
        "put this on my list",
        "add this task",
        "make this a task",

        # Plural variations:
        "add tasks",           
        "create tasks",        
        "new tasks",           
        "make tasks",          
        "add new tasks",       
        "create new tasks",
    ],
    
    "list_tasks": [
        "show tasks",
        "list tasks",
        "what are my tasks",
        "show my tasks",
        "display tasks",
        "what do I have to do",
        "show my list",
        "what's on my list",
        "view tasks",
        "see my tasks",
        "show all tasks",
        "list all tasks",
        "what tasks do I have",
        "show pending tasks",
        "what's pending",
        "display all tasks",
        "let me see my tasks",
        "show me what I have",
        "what's on my to do list",
        "view my list",
        "see all tasks",
        "list everything",
        "show everything",
        "what do I need to do",
        "tasks",
        "my tasks",
    ],
    
    "complete_task": [
        "complete task",
        "mark task as done",
        "finish task",
        "task done",
        "mark complete",
        "complete",
        "done",
        "finished task",
        "mark as complete",
        "mark as done",
        "I finished task",
        "task complete",
        "check off task",
        "mark task done",
        "finish",
        "completed task",
        "task is done",
        "mark done",
        "check task",
        "I completed task",
        "done with task",
        "finished with task",
        "complete this task",
        "mark this done",
        "this task is done",
    ],
    
    "delete_task": [
        "delete task",
        "remove task",
        "erase task",
        "get rid of task",
        "delete",
        "remove",
        "cancel task",
        "discard task",
        "eliminate task",
        "clear task",
        "delete this task",
        "remove this task",
        "get rid of this",
        "erase this",
        "throw away task",
        "remove from list",
        "delete from list",
        "clear this task",
        "cancel this",
        "drop task",
        "drop this task",
        "remove it",
        "delete it",
    ],
    
    "set_priority": [
        "set priority",
        "change priority",
        "make urgent",
        "make important",
        "high priority",
        "low priority",
        "medium priority",
        "priority high",
        "priority low",
        "set task priority",
        "change task priority",
        "make this urgent",
        "mark as urgent",
        "mark as important",
        "set as high priority",
        "set as low priority",
        "priority medium",
        "medium importance",
        "this is urgent",
        "this is important",
        "urgent task",
        "important task",
        "make priority high",
        "make priority low",
    ],
    
    "view_by_status": [
        "show completed tasks",
        "show pending tasks",
        "completed tasks",
        "pending tasks",
        "show done tasks",
        "show finished tasks",
        "what's completed",
        "what's pending",
        "view completed",
        "view pending",
        "list completed",
        "list pending",
        "display completed tasks",
        "display pending tasks",
        "see completed tasks",
        "see pending tasks",
        "show me completed",
        "show me pending",
        "finished tasks",
        "unfinished tasks",
        "done tasks",
        "not done tasks",
    ],
    
    "view_by_priority": [
        "show high priority tasks",
        "show urgent tasks",
        "high priority tasks",
        "urgent tasks",
        "important tasks",
        "show important tasks",
        "low priority tasks",
        "medium priority tasks",
        "show low priority",
        "show medium priority",
        "display urgent tasks",
        "display important tasks",
        "list urgent tasks",
        "list important tasks",
        "see urgent tasks",
        "see important tasks",
        "view high priority",
        "view urgent",
        "what's urgent",
        "what's important",
        "critical tasks",
        "show critical tasks",
    ],
    
    "task_count": [
        "how many tasks",
        "task count",
        "number of tasks",
        "how many tasks do I have",
        "count my tasks",
        "task summary",
        "show summary",
        "statistics",
        "how many pending",
        "how many completed",
        "count tasks",
        "total tasks",
        "how many total",
        "number of pending tasks",
        "number of completed tasks",
        "task stats",
        "give me stats",
        "show me statistics",
        "how many do I have",
        "total task count",
        "pending count",
        "completed count",
    ],
    
    "help": [
        "help",
        "what can you do",
        "help me",
        "I need help",
        "show commands",
        "what are the commands",
        "how do I use this",
        "instructions",
        "guide",
        "what can I ask",
        "what can I say",
        "how does this work",
        "show me how to use this",
        "what are my options",
        "tell me what you can do",
        "features",
        "capabilities",
        "how to use",
        "usage",
        "help please",
        "I'm lost",
        "I don't understand",
    ],
    
    "logout": [
        "logout",
        "log out",
        "switch user",
        "change user",
        "sign out",
        "log off",
        "switch account",
        "change account",
        "different user",
        "I want to logout",
        "I want to log out",
        "sign me out",
        "log me out",
    ],
    
    "goodbye": [
        "bye",
        "goodbye",
        "exit",
        "quit",
        "see you later",
        "see ya",
        "later",
        "I'm done",
        "close",
        "leave",
        "bye bye",
        "talk to you later",
        "see you",
        "gotta go",
        "I have to go",
        "goodbye bot",
        "bye bot",
        "cya",
        "peace",
        "I'm leaving",
        "time to go",
    ],
}

# Helper function to get all intents
def get_all_intents():
    """
    Returns a list of all intent names.
    
    Returns:
        list: List of intent strings
    """
    return list(TRAINING_DATA.keys())

# Helper function to get training examples
def get_training_examples():
    """
    Converts training data into format needed for scikit-learn.
    
    Returns:
        tuple: (texts, labels)
            - texts: List of example phrases
            - labels: List of corresponding intent labels
    
    Example output:
        texts = ["hello", "hi", "add task", "create task", ...]
        labels = ["greeting", "greeting", "create_task", "create_task", ...]
    """
    texts = []
    labels = []
    
    # Loop through each intent and its examples
    for intent, examples in TRAINING_DATA.items():
        for example in examples:
            texts.append(example)
            labels.append(intent)
    
    return texts, labels