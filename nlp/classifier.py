# Import pickle for saving/loading the trained model to disk
import pickle

# Import TfidfVectorizer - converts text to numerical features using TF-IDF algorithm
# TF-IDF = Term Frequency-Inverse Document Frequency (measures word importance)
from sklearn.feature_extraction.text import TfidfVectorizer

# Import MultinomialNB - the Naive Bayes classifier for text classification
# "Multinomial" means it works with word counts/frequencies
from sklearn.naive_bayes import MultinomialNB

# Import train_test_split - splits data into training and testing sets
from sklearn.model_selection import train_test_split

# Import accuracy_score - measures how many predictions were correct
from sklearn.metrics import accuracy_score, classification_report

# Import our custom modules
from nlp.preprocessor import TextPreprocessor  # Text cleaning and stemming
from nlp.training_data import get_training_examples  # Training data loader


class IntentClassifier:
    """
    Machine Learning model for classifying user intents.
    
    This class handles:
    1. Training - Learning from examples
    2. Prediction - Classifying new user input
    3. Persistence - Saving/loading the trained model
    
    How it works:
    1. Text → Preprocessor → Clean tokens
    2. Tokens → TF-IDF Vectorizer → Numerical features
    3. Features → Naive Bayes → Intent prediction
    """
    
    def __init__(self):
        """
        Initialize the classifier with preprocessor and ML models.
        """
        # Text preprocessor for cleaning and stemming
        self.preprocessor = TextPreprocessor()
        
        # TF-IDF Vectorizer - converts text to numerical features
        # max_features=100: Use only the 100 most important words
        # This prevents overfitting and speeds up training
        self.vectorizer = TfidfVectorizer(max_features=100)
        
        # Multinomial Naive Bayes classifier
        # alpha=1.0: Smoothing parameter (prevents zero probabilities) - Very cautious, spreads probability across intents
        # alpha=0.1:Less conservative, higher confidence - More confident, concentrates probability on top intent
        self.classifier = MultinomialNB(alpha=0.1)
        
        # Flag to track if model has been trained
        self.is_trained = False
    
    def train(self, test_size=0.2, random_state=42):
        """
        Train the intent classifier on the training data.
        
        Steps:
        1. Load training examples
        2. Preprocess all text
        3. Split into train/test sets
        4. Convert text to TF-IDF features
        5. Train Naive Bayes classifier
        6. Evaluate accuracy
        
        Args:
            test_size (float): Fraction of data to use for testing (0.2 = 20%)
            random_state (int): Random seed for reproducible splits
        
        Returns:
            dict: Training results with accuracy and report
        """
        print("🤖 BEEP BOOP. Initiating training sequence...")
        
        # Step 1: Get training data
        # texts = ["add task", "show tasks", ...] (raw examples)
        # labels = ["create_task", "list_tasks", ...] (corresponding intents)
        texts, labels = get_training_examples()
        print(f"   Loaded {len(texts)} training examples")
        
        # Step 2: Preprocess all training texts
        # Apply cleaning, tokenization, and stemming to each example
        preprocessed_texts = [
            self.preprocessor.preprocess_to_string(text) 
            for text in texts
        ]
        print(f"   Preprocessed {len(preprocessed_texts)} examples")
        
        # Step 3: Split data into training and testing sets
        # Training set (80%): Used to teach the model
        # Test set (20%): Used to evaluate how well it learned
        # random_state=42: Ensures same split every time (reproducible)
        X_train, X_test, y_train, y_test = train_test_split(
            preprocessed_texts,  # Input texts
            labels,              # Target labels (intents)
            test_size=test_size,
            random_state=random_state
        )
        print(f"   Split: {len(X_train)} training, {len(X_test)} testing")
        
        # Step 4: Convert text to TF-IDF features
        # fit_transform: Learn vocabulary from training data AND transform it
        # The vectorizer learns which words are important
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        
        # transform: Apply same vocabulary to test data (don't learn new words!)
        X_test_vectorized = self.vectorizer.transform(X_test)
        print(f"   Vectorized to {X_train_vectorized.shape[1]} features")
        
        # Step 5: Train the Naive Bayes classifier
        # This is where the actual machine learning happens!
        # The model learns probabilities: P(intent | words)
        self.classifier.fit(X_train_vectorized, y_train)
        print("   ✅ Classifier trained!")
        
        # Step 6: Evaluate on test set
        # Predict intents for test examples (data the model hasn't seen)
        y_pred = self.classifier.predict(X_test_vectorized)
        
        # Calculate accuracy: What % did we get right?
        accuracy = accuracy_score(y_test, y_pred)
        print(f"   📊 Accuracy: {accuracy * 100:.2f}%")
        
        # Generate detailed classification report
        # Shows precision, recall, F1-score for each intent
        report = classification_report(y_test, y_pred, zero_division=0)
        
        # Mark as trained
        self.is_trained = True
        
        return {
            "accuracy": accuracy,
            "report": report,
            "train_size": len(X_train),
            "test_size": len(X_test),
            "num_features": X_train_vectorized.shape[1]
        }
    
    def predict(self, text):
        """
        Predict the intent of user input.
        
        Args:
            text (str): User's input text
        
        Returns:
            dict: {
                "intent": predicted intent,
                "confidence": probability (0.0 to 1.0)
            }
        
        Example:
            result = classifier.predict("add new task")
            print(result)  # {"intent": "create_task", "confidence": 0.87}
        """
        if not self.is_trained:
            raise Exception("Classifier not trained! Call train() first.")
        
        # Step 1: Preprocess the input text
        preprocessed = self.preprocessor.preprocess_to_string(text)
        
        # Step 2: Convert to TF-IDF features (using learned vocabulary)
        vectorized = self.vectorizer.transform([preprocessed])
        
        # Step 3: Predict the intent
        predicted_intent = self.classifier.predict(vectorized)[0]
        
        # Step 4: Get confidence scores for all intents
        # predict_proba returns probabilities for each possible intent
        probabilities = self.classifier.predict_proba(vectorized)[0]
        
        # Get the highest probability (confidence in our prediction)
        confidence = max(probabilities)
        
        return {
            "intent": predicted_intent,
            "confidence": float(confidence)
        }
    
    def predict_with_details(self, text):
        """
        Predict intent with detailed probabilities for all intents.
        
        Useful for debugging or showing alternatives.
        
        Args:
            text (str): User's input text
        
        Returns:
            dict: {
                "intent": predicted intent,
                "confidence": probability,
                "all_probabilities": {intent: probability, ...}
            }
        """
        if not self.is_trained:
            raise Exception("Classifier not trained! Call train() first.")
        
        # Preprocess and vectorize
        preprocessed = self.preprocessor.preprocess_to_string(text)
        vectorized = self.vectorizer.transform([preprocessed])
        
        # Predict
        predicted_intent = self.classifier.predict(vectorized)[0]
        probabilities = self.classifier.predict_proba(vectorized)[0]
        
        # Get list of all possible intents (classes)
        all_intents = self.classifier.classes_
        
        # Create dictionary of intent -> probability
        intent_probabilities = {
            intent: float(prob) 
            for intent, prob in zip(all_intents, probabilities)
        }
        
        return {
            "intent": predicted_intent,
            "confidence": float(max(probabilities)),
            "all_probabilities": intent_probabilities
        }
    
    def predict_with_confidence_check(self, text, margin_threshold=0.15, ratio_threshold=2.0):
        """
        Predict intent with confidence assessment using relative comparison.
        
        Instead of using absolute confidence (>50%), this method compares
        the top prediction to alternatives to determine reliability.
        
        Args:
            text (str): User input
            margin_threshold (float): Minimum difference between top and second (default 0.15 = 15%)
            ratio_threshold (float): Minimum ratio of top to second (default 2.0 = 2x better)
        
        Returns:
            dict: {
                "intent": predicted intent,
                "confidence": probability,
                "is_confident": bool indicating if prediction is reliable,
                "margin": difference between top and second prediction,
                "ratio": how many times better top is than second,
                "alternatives": list of (intent, probability) tuples for top 3
            }
        
        Example:
            result = classifier.predict_with_confidence_check("add task")
            
            if result['is_confident']:
                # Proceed with the intent
                execute_action(result['intent'])
            else:
                # Ask user for clarification
                show_alternatives(result['alternatives'])
        """
        if not self.is_trained:
            raise Exception("Classifier not trained! Call train() first.")
        
        # Get full prediction details
        result = self.predict_with_details(text)
        
        # Sort probabilities from highest to lowest
        sorted_probs = sorted(
            result['all_probabilities'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get top two predictions
        top_prob = sorted_probs[0][1]
        second_prob = sorted_probs[1][1]
        
        # Calculate margin (difference between top and second)
        margin = top_prob - second_prob
        
        # Calculate ratio (how many times better is top than second)
        ratio = top_prob / second_prob if second_prob > 0 else float('inf')
        
        # Determine if we're confident:
        # Confident if EITHER:
        # 1. Top prediction is at least 2x better than second (ratio >= 2.0)
        # 2. Margin between them is at least 15 percentage points
        is_confident = (ratio >= ratio_threshold) or (margin >= margin_threshold)
        
        return {
            "intent": result['intent'],
            "confidence": result['confidence'],
            "is_confident": is_confident,
            "margin": margin,
            "ratio": ratio,
            "alternatives": sorted_probs[:3]  # Top 3 for showing user
        }
    
    def save_model(self, filepath='data/intent_classifier.pkl'):
        """
        Save the trained model to disk.
        
        Saves:
        - Trained vectorizer (vocabulary and TF-IDF weights)
        - Trained classifier (learned probabilities)
        
        Args:
            filepath (str): Path where to save the model
        """
        if not self.is_trained:
            raise Exception("Cannot save untrained model!")
        
        # Create model package with both vectorizer and classifier
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier
        }
        
        # Pickle = Python's way of saving objects to files
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath='data/intent_classifier.pkl'):
        """
        Load a previously trained model from disk.
        
        Args:
            filepath (str): Path to the saved model
        """
        try:
            # Load the pickled model data
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            # Restore vectorizer and classifier
            self.vectorizer = model_data['vectorizer']
            self.classifier = model_data['classifier']
            self.is_trained = True
            
            print(f"✅ Model loaded from {filepath}")
        
        except FileNotFoundError:
            print(f"❌ Model file not found: {filepath}")
            print("   Train the model first using train()")