# Import our database manager for database operations
from database.db_manager import DatabaseManager

# Import our models for user and task operations
from models.user import User
from models.task import Task

# Import our NLP components for understanding user input
from nlp.classifier import IntentClassifier
from nlp.preprocessor import TextPreprocessor

# Import our chatbot components for extracting info and generating responses
from chatbot.entity_extractor import EntityExtractor
from chatbot.response_generator import ResponseGenerator


class ChatBot:
    """
    Main chatbot logic - the brain that connects all components.
    
    This class orchestrates the entire conversation flow:
    1. Takes user input
    2. Classifies intent (what user wants)
    3. Extracts entities (specific details)
    4. Executes appropriate action
    5. Generates friendly response
    
    Architecture:
        User Input
            ↓
        [Intent Classifier] → Detect intent
            ↓
        [Entity Extractor] → Extract details
            ↓
        [Bot Logic] → Execute action
            ↓
        [Response Generator] → Create reply
            ↓
        Bot Response
    """
    
    def __init__(self, db_path='data/taskbot.db', model_path='data/intent_classifier.pkl'):
        """
        Initialize the chatbot with all necessary components.
        
        Args:
            db_path (str): Path to SQLite database
            model_path (str): Path to trained intent classifier model
        """
        # Initialize database and models
        self.db = DatabaseManager(db_path)
        self.user_model = User(self.db)
        self.task_model = Task(self.db)
        
        # Initialize NLP components
        self.classifier = IntentClassifier()
        self.classifier.load_model(model_path)
        
        # Initialize chatbot components
        self.entity_extractor = EntityExtractor()
        self.response_generator = ResponseGenerator()
        
        # Track current user session
        self.current_user = None

        # Track if we're waiting for clarification response
        # Stores both alternatives and original input
        self.pending_clarification = None
    
    def login(self, username, password):
        """
        Authenticate user and start session.
        
        Args:
            username (str): Username
            password (str): Password
        
        Returns:
            dict: Login result from User.login()
        """
        result = self.user_model.login(username, password)
        
        if result['success']:
            # Store current user for session
            self.current_user = result['user']
        
        return result
    
    def register(self, username, password):
        """
        Register new user.
        
        Args:
            username (str): Desired username
            password (str): Password
        
        Returns:
            dict: Registration result from User.register()
        """
        return self.user_model.register(username, password)
    
    def logout(self):
        """
        End current user session.
        
        Returns:
            str: Logout message
        """
        self.current_user = None
        return self.response_generator.generate_logout()
    
    def process_input(self, user_input):
        """
        Main method - processes user input and returns bot response.
        
        Args:
            user_input (str): What the user said
        
        Returns:
            str: Bot's response
        """
        # Ensure user is logged in
        if not self.current_user:
            return "❌ Please login first!"
        
        # === CALL #2: Runs first if the user made a clarification, if not it will go directly to CALL #1 ===
        # Check if user is responding to clarification with a number
        if self.pending_clarification:
            # Try to parse as number
            try:
                choice = int(user_input.strip())
                
                # Get stored data
                alternatives = self.pending_clarification['alternatives']
                original_input = self.pending_clarification['original_input']
                
                # Validate choice is in range
                if 1 <= choice <= len(alternatives):
                    # Get the selected intent
                    selected_intent = alternatives[choice - 1][0]
                    
                    # Clear pending clarification
                    self.pending_clarification = None
                    
                    # NOW: Extract entities from the ORIGINAL input using the selected intent
                    entities = self.entity_extractor.extract_all(original_input, selected_intent)
                    
                    # Route to handler with ORIGINAL input and extracted entities
                    handler_map = {
                        'greeting': self._handle_greeting,
                        'create_task': self._handle_create_task,
                        'list_tasks': self._handle_list_tasks,
                        'complete_task': self._handle_complete_task,
                        'delete_task': self._handle_delete_task,
                        'set_priority': self._handle_set_priority,
                        'view_by_status': self._handle_view_by_status,
                        'view_by_priority': self._handle_view_by_priority,
                        'task_count': self._handle_task_count,
                        'help': self._handle_help,
                        'logout': self._handle_logout,
                        'goodbye': self._handle_goodbye,
                    }
                    
                    handler = handler_map.get(selected_intent)
                    if handler:
                        # Use ORIGINAL input and extracted entities
                        response = handler(original_input, entities)
                    
                        # Log conversation
                        self._log_conversation(original_input, selected_intent, response)
                        
                        return response
                    else:
                        return self.response_generator.generate_fallback()
                else:
                    return f"❌ Please choose a number between 1 and {len(alternatives)}."
            
            except ValueError:
                # Not a number - treat as new input and clear pending clarification
                self.pending_clarification = None
                # Continue to normal processing below
        
        # === CALL #1: runs when no pending clarification ===
        # Step 1: Classify intent with confidence check
        prediction = self.classifier.predict_with_confidence_check(user_input)
        intent = prediction['intent']
        is_confident = prediction['is_confident']
        
        # If not confident, ask for clarification
        if not is_confident:
            # Store BOTH alternatives AND original input
            self.pending_clarification = {
                'alternatives': prediction['alternatives'],
                'original_input': user_input  # ← CRITICAL: Store this to use it when asking for clarifications
            }
            
            return self.response_generator.generate_clarification(
                prediction['alternatives']
            )
        
        # Step 2: Extract entities from input
        entities = self.entity_extractor.extract_all(user_input, intent)
        
        # Step 3: Route to appropriate handler based on intent
        handler_map = {
            'greeting': self._handle_greeting,
            'create_task': self._handle_create_task,
            'list_tasks': self._handle_list_tasks,
            'complete_task': self._handle_complete_task,
            'delete_task': self._handle_delete_task,
            'set_priority': self._handle_set_priority,
            'view_by_status': self._handle_view_by_status,
            'view_by_priority': self._handle_view_by_priority,
            'task_count': self._handle_task_count,
            'help': self._handle_help,
            'logout': self._handle_logout,
            'goodbye': self._handle_goodbye,
        }
        
        # Get the appropriate handler function
        handler = handler_map.get(intent)
        
        if handler:
       
            # Call handler and get response
            response = handler(user_input, entities)
            
            # NEW: Log conversation to database
            self._log_conversation(user_input, intent, response)
            
            return response

        else:

            # Fallback for unknown intents
            response = self.response_generator.generate_fallback()
            
            # NEW: Log fallback too
            self._log_conversation(user_input, 'fallback', response)
            
            return response
   
    def _handle_greeting(self, user_input, entities):
        """Handle greeting intent."""
        return self.response_generator.generate_greeting()
    
    def _handle_create_task(self, user_input, entities):
        """
        Handle task creation.
        
        Extracts task title and priority, creates task in database.
        """
        # Get task title from entities
        task_title = entities.get('task_title')
        
        if not task_title:
            return self.response_generator.generate_error(
                "Please specify what task you want to create.\nExample: 'add task review code'"
            )
        
        # Get priority (defaults to medium in Task model if None)
        priority = entities.get('priority')
        
        # Create the task
        result = self.task_model.create_task(
            user_id=self.current_user['id'],
            title=task_title,
            priority=priority
        )
        
        if result['success']:
            return self.response_generator.generate_task_created(result['task'])
        else:
            return self.response_generator.generate_error(result['message'])
    
    def _handle_list_tasks(self, user_input, entities):
        """Handle listing all tasks."""
        result = self.task_model.list_tasks(
            user_id=self.current_user['id']
        )
        
        if result['success']:
            return self.response_generator.generate_task_list(result['tasks'])
        else:
            return self.response_generator.generate_error("Failed to retrieve tasks.")
    
    def _handle_complete_task(self, user_input, entities):
        """
        Handle marking task as complete.
        
        Requires task ID to be extracted from input.
        """
        task_id = entities.get('task_id')
        
        if not task_id:
            return self.response_generator.generate_error(
                "Please specify which task to complete.\nExample: 'complete task 5'"
            )
        
        result = self.task_model.complete_task(
            task_id=task_id,
            user_id=self.current_user['id']
        )
        
        if result['success']:
            return self.response_generator.generate_task_completed(task_id)
        else:
            return self.response_generator.generate_error(result['message'])
    
    def _handle_delete_task(self, user_input, entities):
        """
        Handle task deletion.
        
        Requires task ID to be extracted from input.
        """
        task_id = entities.get('task_id')
        
        if not task_id:
            return self.response_generator.generate_error(
                "Please specify which task to delete.\nExample: 'delete task 5'"
            )
        
        result = self.task_model.delete_task(
            task_id=task_id,
            user_id=self.current_user['id']
        )
        
        if result['success']:
            return self.response_generator.generate_task_deleted(task_id)
        else:
            return self.response_generator.generate_error(result['message'])
    
    def _handle_set_priority(self, user_input, entities):
        """
        Handle setting task priority.
        
        Requires both task ID and priority to be extracted.
        """
        task_id = entities.get('task_id')
        priority = entities.get('priority')
        
        if not task_id:
            return self.response_generator.generate_error(
                "Please specify which task.\nExample: 'set task 5 priority high'"
            )
        
        if not priority:
            return self.response_generator.generate_error(
                "Please specify priority (low, medium, or high).\nExample: 'set task 5 priority high'"
            )
        
        result = self.task_model.set_priority(
            task_id=task_id,
            user_id=self.current_user['id'],
            priority=priority
        )
        
        if result['success']:
            return self.response_generator.generate_priority_updated(task_id, priority)
        else:
            return self.response_generator.generate_error(result['message'])
    
    def _handle_view_by_status(self, user_input, entities):
        """Handle viewing tasks filtered by status (pending/completed)."""
        status = entities.get('status')
        
        if not status:
            # Default to pending if not specified
            status = 'pending'
        
        result = self.task_model.list_tasks(
            user_id=self.current_user['id'],
            status=status
        )
        
        if result['success']:
            filter_label = f"{status}"
            return self.response_generator.generate_task_list(
                result['tasks'],
                filter_type=filter_label
            )
        else:
            return self.response_generator.generate_error("Failed to retrieve tasks.")
    
    def _handle_view_by_priority(self, user_input, entities):
        """Handle viewing tasks filtered by priority."""
        priority = entities.get('priority')
        
        if not priority:
            # Default to high if not specified
            priority = 'high'
        
        result = self.task_model.list_tasks(
            user_id=self.current_user['id'],
            priority=priority
        )
        
        if result['success']:
            filter_label = f"{priority} priority"
            return self.response_generator.generate_task_list(
                result['tasks'],
                filter_type=filter_label
            )
        else:
            return self.response_generator.generate_error("Failed to retrieve tasks.")
    
    def _handle_task_count(self, user_input, entities):
        """Handle showing task statistics."""
        stats = self.task_model.get_task_count(
            user_id=self.current_user['id']
        )
        
        return self.response_generator.generate_task_count(stats)
    
    def _handle_help(self, user_input, entities):
        """Handle help request."""
        return self.response_generator.generate_help()
    
    def _handle_logout(self, user_input, entities):
        """Handle logout request."""
        return self.logout()
    
    def _handle_goodbye(self, user_input, entities):
        """Handle goodbye."""
        return self.response_generator.generate_goodbye()
    
    
    def _log_conversation(self, user_input, intent, bot_response):
        """
        Log conversation to database for history and analytics.
        
        This stores every interaction between user and bot, including:
        - What the user asked
        - What intent was detected
        - How the bot responded
        - Timestamp (automatic)
        
        Args:
            user_input (str): User's message
            intent (str): Detected intent (e.g., 'create_task', 'list_tasks')
            bot_response (str): Bot's response message
        """
        try:
            # SQL query to insert conversation record
            query = """
                INSERT INTO conversations (user_id, user_input, detected_intent, bot_response)
                VALUES (?, ?, ?, ?)
            """
            
            # Execute insert
            self.db.execute_update(
                query,
                (self.current_user['id'], user_input, intent, bot_response)
            )
            
        except Exception as e:
            # If logging fails, don't break the conversation
            # Just print warning and continue
            print(f"⚠️ Warning: Failed to log conversation: {e}")
            # Don't raise exception - logging is not critical for core functionality