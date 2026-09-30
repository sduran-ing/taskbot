"""
Test the relative confidence approach.

Run from project root:
    py scripts/test_confidence.py
"""

# Import sys and os for path handling
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our classifier
from nlp.classifier import IntentClassifier


def test_confidence_approach():
    """Test predictions with relative confidence checking."""
    
    print("🤖 TESTING RELATIVE CONFIDENCE APPROACH")
    print("=" * 70)
    
    # Load model
    classifier = IntentClassifier()
    
    if not os.path.exists('data/intent_classifier.pkl'):
        print("\n❌ No model found. Run: py scripts/train_model.py")
        return
    
    print("\n📂 Loading trained model...")
    classifier.load_model()
    
    # Test cases with expectations
    test_cases = [
        ("hello", "Should be CONFIDENT (clear greeting)"),
        ("add task review code", "Should be CONFIDENT (clear create action)"),
        ("show my tasks", "Might be CONFIDENT or UNCLEAR"),
        ("delete task 3", "Should be CONFIDENT"),
        ("task", "Should be UNCLEAR (too vague)"),
        ("xyz random gibberish", "Should be UNCLEAR (nonsense)"),
        ("help", "Should be CONFIDENT"),
        ("show", "Should be UNCLEAR (ambiguous - show what?)"),
    ]
    
    print("\n🧪 Testing predictions:\n")
    
    confident_count = 0
    unclear_count = 0
    
    for text, expected in test_cases:
        result = classifier.predict_with_confidence_check(text)
        
        # Determine status
        if result['is_confident']:
            status = "✓ CONFIDENT"
            confident_count += 1
        else:
            status = "⚠ UNCLEAR"
            unclear_count += 1
        
        print(f"📝 Input: \"{text}\"")
        print(f"   Expected: {expected}")
        print(f"   Intent: {result['intent']} (confidence: {result['confidence']:.1%})")
        print(f"   Status: {status}")
        print(f"   Margin: {result['margin']:.1%} | Ratio: {result['ratio']:.2f}x")
        print(f"   Top 3 alternatives:")
        for intent, prob in result['alternatives']:
            marker = "→" if intent == result['intent'] else " "
            print(f"     {marker} {intent}: {prob:.1%}")
        print()
    
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"   Confident predictions: {confident_count}/{len(test_cases)}")
    print(f"   Unclear predictions: {unclear_count}/{len(test_cases)}")
    
    print("\n💡 Interpretation:")
    print("   ✓ CONFIDENT = Top prediction is clearly better than alternatives")
    print("                 (ratio ≥ 2.0x OR margin ≥ 15%)")
    print("   ⚠ UNCLEAR   = Predictions too close, should ask for clarification")
    
    print("\n✅ Test complete!")


if __name__ == "__main__":
    test_confidence_approach()