# Import re - Python's built-in regular expression library for pattern matching in text
# Used for: Removing special characters, cleaning text
import re

# Import nltk - Natural Language Toolkit, a comprehensive NLP library
# Used for: Tokenization, stemming, and other text processing tasks
import nltk

# Import word_tokenize - NLTK's function to split text into individual words (tokens)
# Smarter than text.split() because it handles punctuation and contractions properly
from nltk.tokenize import word_tokenize

# Import PorterStemmer - Algorithm that reduces words to their root form
# Example: "running" → "run", "tasks" → "task", "added" → "add"
from nltk.stem import PorterStemmer

class TextPreprocessor:
    """
    Handles text preprocessing for intent classification.
    
    Steps:
    1. Lowercase - "Add Task" → "add task"
    2. Remove punctuation - "add task!" → "add task"
    3. Tokenize - "add task" → ["add", "task"]
    4. Stem - ["adding", "tasks"] → ["add", "task"]
    
    Why preprocessing?
    - Makes text consistent
    - Reduces variations (add/adding/added → add)
    - Improves classification accuracy
    """
    
    def __init__(self):
        """
        Initialize the preprocessor and download required NLTK data.
        
        NLTK (Natural Language Toolkit) needs some data files for
        tokenization and stemming. This downloads them if not present.
        """
        # Initialize the Porter Stemmer (reduces words to root form)
        self.stemmer = PorterStemmer()
        
        # Download NLTK data (only happens once, then cached)
        # punkt: Rules for splitting text into words/sentences
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("⏳ Downloading NLTK data (one-time setup)...")
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
            print("✅ NLTK data downloaded!")
    
    def clean_text(self, text):
        """
        Clean text by lowercasing and removing special characters.
        
        Args:
            text (str): Raw input text
        
        Returns:
            str: Cleaned text
        
        Example:
            Input:  "Add Task!!! What's next?"
            Output: "add task whats next"
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        # [^a-z0-9\s] means: anything that's NOT (letter, number, or space)
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Remove extra whitespace
        # \s+ means: one or more whitespace characters
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text):
        """
        Split text into individual words (tokens).
        
        Args:
            text (str): Text to tokenize
        
        Returns:
            list: List of word tokens
        
        Example:
            Input:  "add new task"
            Output: ["add", "new", "task"]
        """
        # NLTK's word_tokenize is smarter than text.split()
        # It handles punctuation and contractions better
        return word_tokenize(text)
    
    def stem_tokens(self, tokens):
        """
        Reduce words to their root form (stem).
        
        Args:
            tokens (list): List of word tokens
        
        Returns:
            list: List of stemmed tokens
        
        Example:
            Input:  ["adding", "tasks", "completed"]
            Output: ["add", "task", "complet"]
        
        Note: Stems aren't always real words ("completed" → "complet")
        but that's okay! We just need consistency.
        """
        return [self.stemmer.stem(token) for token in tokens]
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline: clean → tokenize → stem.
        
        This is the main method you'll use. It applies all preprocessing
        steps in the correct order.
        
        Args:
            text (str): Raw input text
        
        Returns:
            list: List of preprocessed tokens
        
        Example:
            Input:  "I'm adding two tasks!!"
            Steps:
                1. Clean:    "im adding two tasks"
                2. Tokenize: ["im", "adding", "two", "tasks"]
                3. Stem:     ["im", "add", "two", "task"]
            Output: ["im", "add", "two", "task"]
        """
        # Step 1: Clean the text
        cleaned = self.clean_text(text)
        
        # Step 2: Tokenize into words
        tokens = self.tokenize(cleaned)
        
        # Step 3: Stem each token
        stemmed = self.stem_tokens(tokens)
        
        return stemmed
    
    def preprocess_to_string(self, text):
        """
        Preprocess and return as a string (for vectorizer).
        
        The TF-IDF vectorizer expects strings, not lists, so this
        joins the tokens back into a single string.
        
        Args:
            text (str): Raw input text
        
        Returns:
            str: Preprocessed text as string
        
        Example:
            Input:  "I'm adding tasks"
            Output: "im add task"
        """
        tokens = self.preprocess(text)
        return ' '.join(tokens)