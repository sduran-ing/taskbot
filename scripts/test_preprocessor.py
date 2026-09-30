"""
Test the text preprocessor to see how it transforms text.
"""

from nlp.preprocessor import TextPreprocessor

def test_preprocessor():
    """Test various inputs through the preprocessor."""
    
    print("🤖 TESTING TEXT PREPROCESSOR")
    print("=" * 60)
    
    # Initialize preprocessor
    preprocessor = TextPreprocessor()
    
    # Test cases
    test_inputs = [
        "Add task: review pull request",
        "I'm adding multiple tasks!!!",
        "Show me my completed tasks",
        "HELLO! How are you?",
        "Delete task 5",
        "What's the task count?",
    ]
    
    for text in test_inputs:
        # Preprocess
        tokens = preprocessor.preprocess(text)
        processed_string = preprocessor.preprocess_to_string(text)
        
        # Display results
        print(f"\n📝 Input:  {text}")
        print(f"   Tokens: {tokens}")
        print(f"   String: {processed_string}")
    
    print("\n" + "=" * 60)
    print("✅ Preprocessing test complete!")

if __name__ == "__main__":
    test_preprocessor()