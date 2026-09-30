"""
Test intent predictions using the EXISTING trained model.

This script loads the saved model and tests predictions.
It does NOT retrain the model.

Usage. Run this from the project root:
    py scripts/test_predictions.py
"""

# Import sys and os for path manipulation and file checking
import sys
import os

# Add parent directory to Python path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our classifier
from nlp.classifier import IntentClassifier


def test_predictions():
    """Test predictions using the saved model."""
    
    print("🤖 TASKBOT - INTENT PREDICTION TEST")
    print("=" * 70)
    
    # Create classifier instance
    classifier = IntentClassifier()
    
    # Try to load existing model
    model_path = 'data/intent_classifier.pkl'
    
    if not os.path.exists(model_path):
        print("\n❌ ERROR: No trained model found!")
        print(f"   Expected location: {model_path}")
        print("\n💡 Solution: Run 'py train_model.py' first to train the model.\n")
        return
    
    # Load the existing trained model
    print(f"\n📂 Loading model from {model_path}...")
    classifier.load_model(model_path)
    
    # Test with examples
    print("\n🧪 TESTING PREDICTIONS:")
    print("=" * 70)
    
    test_inputs = [
        "add task review code",
        "show my tasks",
        "delete task 5",
        "mark task 3 as done",
        "what are my pending tasks",
        "hello",
        "goodbye",
        "help me",
        "how many tasks do I have",
        "make task urgent",
        "I want to create a new task",
        "show completed tasks",
        "this is random gibberish xyz",
    ]
    
    for text in test_inputs:
        # Get prediction
        result = classifier.predict_with_details(text)
        
        # Display
        print(f"\n📝 Input: \"{text}\"")
        print(f"   Intent: {result['intent']}")
        print(f"   Confidence: {result['confidence']:.2%}")
        
        # Show if confidence is low
        if result['confidence'] < 0.5:
            print(f"   ⚠️  Low confidence - might need fallback response")
    
    print("\n" + "=" * 70)
    print("✅ Prediction test complete!")
    
    # Interactive mode
    print("\n💬 Interactive Mode (type 'quit' to exit):")
    print("-" * 70)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        result = classifier.predict(user_input)
        print(f"Bot: Intent detected = {result['intent']} ({result['confidence']:.2%})")


if __name__ == "__main__":
    test_predictions()