# Import datetime for timestamp handling
from datetime import datetime

# Import our database manager
from database.db_manager import DatabaseManager


class Task:
    """
    Handles all task-related database operations.
    
    This model provides methods to:
    - Create new tasks
    - List tasks (all, by status, by priority)
    - Update tasks (complete, set priority)
    - Delete tasks
    - Get task statistics
    
    Architecture note: Follows Active Record pattern where the model
    contains both business logic and database operations.
    """
    
    def __init__(self, db_manager):
        """
        Initialize Task model with database manager.
        
        Args:
            db_manager (DatabaseManager): Database manager instance
        """
        self.db = db_manager
    
    def create_task(self, user_id, title, priority='medium'):
        """
        Create a new task for a user.
        
        Args:
            user_id (int): ID of the user who owns this task
            title (str): Task description/title
            priority (str): 'low', 'medium', or 'high' (default: 'medium')
        
        Returns:
            dict: {
                "success": bool,
                "message": str,
                "task_id": int or None,
                "task": dict or None (task details)
            }
        """
        try:
            # Validation: Check if title is not empty
            if not title or not title.strip():
                return {
                    "success": False,
                    "message": "Task title cannot be empty",
                    "task_id": None,
                    "task": None
                }
            
            # Validation: Check priority is valid
            valid_priorities = ['low', 'medium', 'high']

            # Handle None or invalid priority
            if not priority or priority.lower() not in valid_priorities:
                priority = 'medium'  # Default to medium if None or invalid
            
            # Insert task into database
            task_id = self.db.execute_update(
                """INSERT INTO tasks (user_id, title, priority, status) 
                   VALUES (?, ?, ?, 'pending')""",
                (user_id, title.strip(), priority.lower())
            )
            
            # Get the created task details
            task = self.get_task_by_id(task_id)
            
            return {
                "success": True,
                "message": f"Task created successfully! BEEP BOOP. Task ID: {task_id}",
                "task_id": task_id,
                "task": task
            }
        
        except Exception as e:
            # Log error for debugging
            print(f"[ERROR] Failed to create task: {str(e)}")
            
            return {
                "success": False,
                "message": "Failed to create task. Please try again.",
                "task_id": None,
                "task": None
            }
    
    def get_task_by_id(self, task_id):
        """
        Retrieve a single task by its ID.
        
        Args:
            task_id (int): Task ID
        
        Returns:
            dict or None: Task details or None if not found
        """
        tasks = self.db.execute_query(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        )
        
        if tasks:
            task_row = tasks[0]
            return {
                "id": task_row['id'],
                "user_id": task_row['user_id'],
                "title": task_row['title'],
                "priority": task_row['priority'],
                "status": task_row['status'],
                "created_at": task_row['created_at']
            }
        
        return None
    
    def list_tasks(self, user_id, status=None, priority=None):
        """
        List tasks for a user with optional filters.
        
        Args:
            user_id (int): User ID
            status (str, optional): Filter by 'pending' or 'completed'
            priority (str, optional): Filter by 'low', 'medium', or 'high'
        
        Returns:
            dict: {
                "success": bool,
                "tasks": list of task dicts,
                "count": int
            }
        """
        try:
            # Build query based on filters
            query = "SELECT * FROM tasks WHERE user_id = ?"
            params = [user_id]
            
            # Add status filter if provided
            if status:
                query += " AND status = ?"
                params.append(status.lower())
            
            # Add priority filter if provided
            if priority:
                query += " AND priority = ?"
                params.append(priority.lower())
            
            # Order by: pending first, then by creation date (newest first)
            query += " ORDER BY status ASC, created_at DESC"
            
            # Execute query
            task_rows = self.db.execute_query(query, tuple(params))
            
            # Convert to list of dictionaries
            tasks = []
            for row in task_rows:
                tasks.append({
                    "id": row['id'],
                    "title": row['title'],
                    "priority": row['priority'],
                    "status": row['status'],
                    "created_at": row['created_at']
                })
            
            return {
                "success": True,
                "tasks": tasks,
                "count": len(tasks)
            }
        
        except Exception as e:
            # Log error for debugging
            print(f"[ERROR] Failed to list tasks: {str(e)}")
            
            return {
                "success": False,
                "tasks": [],
                "count": 0
            }
    
    def complete_task(self, task_id, user_id):
        """
        Mark a task as completed.
        
        Args:
            task_id (int): Task ID to complete
            user_id (int): User ID (for security - ensure user owns this task)
        
        Returns:
            dict: {
                "success": bool,
                "message": str
            }
        """
        try:
            # Check if task exists and belongs to user
            task = self.get_task_by_id(task_id)
            
            if not task:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found."
                }
            
            if task['user_id'] != user_id:
                return {
                    "success": False,
                    "message": "You don't have permission to complete this task."
                }
            
            if task['status'] == 'completed':
                return {
                    "success": False,
                    "message": f"Task {task_id} is already completed!"
                }
            
            # Mark as completed
            self.db.execute_update(
                "UPDATE tasks SET status = 'completed' WHERE id = ?",
                (task_id,)
            )
            
            return {
                "success": True,
                "message": f"BEEP BOOP. Task {task_id} marked as completed! 🎉"
            }
        
        except Exception as e:
            # Log error for debugging
            print(f"[ERROR] Failed to complete task: {str(e)}")
            
            return {
                "success": False,
                "message": "Failed to complete task. Please try again."
            }
    
    def delete_task(self, task_id, user_id):
        """
        Delete a task.
        
        Args:
            task_id (int): Task ID to delete
            user_id (int): User ID (for security)
        
        Returns:
            dict: {
                "success": bool,
                "message": str
            }
        """
        try:
            # Check if task exists and belongs to user
            task = self.get_task_by_id(task_id)
            
            if not task:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found."
                }
            
            if task['user_id'] != user_id:
                return {
                    "success": False,
                    "message": "You don't have permission to delete this task."
                }
            
            # Delete the task
            self.db.execute_update(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )
            
            return {
                "success": True,
                "message": f"BEEP BOOP. Task {task_id} deleted successfully! 🗑️"
            }
        
        except Exception as e:
            # Log error for debugging
            print(f"[ERROR] Failed to delete task: {str(e)}")
            
            return {
                "success": False,
                "message": "Failed to delete task. Please try again."
            }
    
    def set_priority(self, task_id, user_id, priority):
        """
        Update task priority.
        
        Args:
            task_id (int): Task ID
            user_id (int): User ID (for security)
            priority (str): 'low', 'medium', or 'high'
        
        Returns:
            dict: {
                "success": bool,
                "message": str
            }
        """
        try:
            # Validate priority
            valid_priorities = ['low', 'medium', 'high']
            if not priority or priority.lower() not in valid_priorities:
                return {
                    "success": False,
                    "message": f"Invalid priority. Use: {', '.join(valid_priorities)}"
                }
            
            # Check if task exists and belongs to user
            task = self.get_task_by_id(task_id)
            
            if not task:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found."
                }
            
            if task['user_id'] != user_id:
                return {
                    "success": False,
                    "message": "You don't have permission to update this task."
                }
            
            # Update priority
            self.db.execute_update(
                "UPDATE tasks SET priority = ? WHERE id = ?",
                (priority.lower(), task_id)
            )
            
            return {
                "success": True,
                "message": f"BEEP BOOP. Task {task_id} priority set to {priority}! 🎯"
            }
        
        except Exception as e:
            # Log error for debugging
            print(f"[ERROR] Failed to set priority: {str(e)}")
            
            return {
                "success": False,
                "message": "Failed to update priority. Please try again."
            }
    
    def get_task_count(self, user_id):
        """
        Get task statistics for a user.
        
        Args:
            user_id (int): User ID
        
        Returns:
            dict: {
                "total": int,
                "pending": int,
                "completed": int,
                "high_priority": int
            }
        """
        try:
            # Count total tasks
            total = self.db.execute_query(
                "SELECT COUNT(*) as count FROM tasks WHERE user_id = ?",
                (user_id,)
            )[0]['count']
            
            # Count pending tasks
            pending = self.db.execute_query(
                "SELECT COUNT(*) as count FROM tasks WHERE user_id = ? AND status = 'pending'",
                (user_id,)
            )[0]['count']
            
            # Count completed tasks
            completed = self.db.execute_query(
                "SELECT COUNT(*) as count FROM tasks WHERE user_id = ? AND status = 'completed'",
                (user_id,)
            )[0]['count']
            
            # Count high priority tasks
            high_priority = self.db.execute_query(
                "SELECT COUNT(*) as count FROM tasks WHERE user_id = ? AND priority = 'high' AND status = 'pending'",
                (user_id,)
            )[0]['count']
            
            return {
                "total": total,
                "pending": pending,
                "completed": completed,
                "high_priority": high_priority
            }
        
        except Exception as e:
            # Log error for debugging
            print(f"[ERROR] Failed to get task count: {str(e)}")
            
            return {
                "total": 0,
                "pending": 0,
                "completed": 0,
                "high_priority": 0
            }