"""
Debug script to investigate low confidence issues.

Run from project root:
    py scripts/debug_classifier.py
"""

# Import sys and os for path handling
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import numpy for array operations
import numpy as np

# Import our modules
from nlp.classifier import IntentClassifier
from nlp.training_data import get_training_examples


def debug_classifier():
    """Debug the classifier to understand confidence issues."""
    
    print("🔍 CLASSIFIER DEBUGGING")
    print("=" * 70)
    
    # Step 1: Check training data
    texts, labels = get_training_examples()
    print(f"\n📊 Training Data Stats:")
    print(f"   Total examples: {len(texts)}")
    
    # Count examples per intent
    from collections import Counter
    intent_counts = Counter(labels)
    print(f"   Number of intents: {len(intent_counts)}")
    print(f"\n   Examples per intent:")
    for intent, count in sorted(intent_counts.items()):
        print(f"      {intent}: {count}")
    
    # Step 2: Train fresh model
    print(f"\n📚 Training fresh model...")
    classifier = IntentClassifier()
    results = classifier.train()
    print(f"   Accuracy: {results['accuracy'] * 100:.2f}%")
    
    # Step 3: Test on TRAINING examples (should be high confidence)
    print(f"\n🧪 Testing on TRAINING examples (should be confident):")
    print("-" * 70)
    
    # Test first 3 examples from each intent
    test_samples = []
    for intent in list(intent_counts.keys())[:3]:  # First 3 intents
        intent_examples = [text for text, label in zip(texts, labels) if label == intent]
        test_samples.append((intent_examples[0], intent))
    
    for text, expected_intent in test_samples:
        result = classifier.predict_with_details(text)
        match = "✓" if result['intent'] == expected_intent else "✗"
        print(f"\n{match} Input: \"{text}\"")
        print(f"   Expected: {expected_intent}")
        print(f"   Got: {result['intent']} ({result['confidence']:.2%})")
        
        # Show all probabilities
        sorted_probs = sorted(
            result['all_probabilities'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        print(f"   All predictions:")
        for intent, prob in sorted_probs[:5]:
            print(f"      {intent}: {prob:.4f}")
    
    # Step 4: Check if probabilities are normalized
    print(f"\n🔬 Probability Distribution Check:")
    result = classifier.predict_with_details("add task")
    total_prob = sum(result['all_probabilities'].values())
    print(f"   Sum of all probabilities: {total_prob:.4f}")
    print(f"   (Should be 1.0 if normalized correctly)")
    
    # Step 5: Save and load model, test again
    print(f"\n💾 Testing save/load cycle...")
    classifier.save_model()
    
    classifier2 = IntentClassifier()
    classifier2.load_model()
    
    result_before = classifier.predict("add task")
    result_after = classifier2.predict("add task")
    
    print(f"   Before save: {result_before['intent']} ({result_before['confidence']:.2%})")
    print(f"   After load:  {result_after['intent']} ({result_after['confidence']:.2%})")
    
    if result_before['confidence'] != result_after['confidence']:
        print(f"   ⚠️  WARNING: Confidence changed after save/load!")
    else:
        print(f"   ✓ Confidence consistent after save/load")
    
    print("\n" + "=" * 70)
    print("✅ Debugging complete!")


if __name__ == "__main__":
    debug_classifier()