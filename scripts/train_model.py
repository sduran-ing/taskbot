"""
Training script for the intent classifier.

Run this script ONLY when:
- First time setup
- You've added more training examples
- You want to improve the model

Usage. Run this from the project root:
    py scripts/train_model.py
"""
# Import sys and os for path manipulation
import sys
import os

# Add parent directory to Python path so we can import our modules
# This allows the script to find 'nlp', 'database', etc.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our classifier module
from nlp.classifier import IntentClassifier


def train_and_save():
    """Train the intent classifier and save it."""
    
    print("🤖 TASKBOT - TRAINING INTENT CLASSIFIER")
    print("=" * 70)
    print("\n⚠️  This will train a NEW model and overwrite the existing one.")
    print("   Only run this when you've updated training data.\n")
    
    # Ask for confirmation
    response = input("Continue? (yes/no): ").strip().lower()
    
    if response != "yes":
        print("❌ Training cancelled.")
        return
    
    print("\n📚 Starting training...")
    
    # Create and train classifier
    classifier = IntentClassifier()
    results = classifier.train()
    
    # Display results
    print(f"\n📊 TRAINING RESULTS:")
    print(f"   Training examples: {results['train_size']}")
    print(f"   Test examples: {results['test_size']}")
    print(f"   Features: {results['num_features']}")
    print(f"   Accuracy: {results['accuracy'] * 100:.2f}%")
    
    # Show detailed report
    print(f"\n   Detailed Classification Report:")
    print(results['report'])
    
    # Save the model
    print("\n💾 Saving model...")
    classifier.save_model()
    
    print("\n" + "=" * 70)
    print("✅ Training complete! Model saved to data/intent_classifier.pkl")
    print("\n💡 Your app will now use this trained model.")
    print("   Run 'py main.py' to start the chatbot.\n")


if __name__ == "__main__":
    train_and_save()