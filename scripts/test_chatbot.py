"""
Test the complete chatbot in command-line mode.

This script lets you interact with TaskBot to test all functionality:
- Registration and login
- Creating tasks
- Listing tasks
- Completing/deleting tasks
- All other features

Run from project root:
    py scripts/test_chatbot.py
"""

# Import sys and os for path handling
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our chatbot
from chatbot.bot_logic import ChatBot


def test_chatbot():
    """Interactive command-line chatbot testing."""
    
    print("=" * 70)
    print("🤖 TASKBOT - COMMAND LINE TEST")
    print("=" * 70)
    
    # Initialize bot
    print("\n⏳ Initializing TaskBot...")
    bot = ChatBot()
    print("✅ TaskBot initialized!\n")
    
    # Login/Register loop
    while True:
        print("=" * 70)
        print("1. Login")
        print("2. Register new account")
        print("3. Exit")
        print("=" * 70)
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            # Login
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            result = bot.login(username, password)
            print(f"\n{result['message']}")
            
            if result['success']:
                break  # Exit login loop, start chat
        
        elif choice == "2":
            # Register
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            result = bot.register(username, password)
            print(f"\n{result['message']}")
            
            if result['success']:
                # Auto-login after registration
                bot.login(username, password)
                break
        
        elif choice == "3":
            print("\n👋 Goodbye!")
            return
        
        else:
            print("\n❌ Invalid choice. Please try again.")
    
    # Chat loop
    print("\n" + "=" * 70)
    print("🤖 TASKBOT ACTIVE - Start chatting!")
    print("=" * 70)
    print("\n💡 Tips:")
    print("   • Try: 'add task review code'")
    print("   • Try: 'show my tasks'")
    print("   • Try: 'help' to see all commands")
    print("   • Type 'quit' to exit\n")
    print("=" * 70 + "\n")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        # Check for quit command
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Exiting test mode. Goodbye!")
            break
        
        # Process input and get response
        response = bot.process_input(user_input)
        
        # Display response
        print(f"\nBot: {response}\n")
        print("-" * 70 + "\n")


if __name__ == "__main__":
    test_chatbot()