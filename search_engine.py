import json
import os
import re
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

class SearchEngine:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.index_file = os.path.join(data_dir, "index.json")
        self.documents_file = os.path.join(data_dir, "documents.json")
        
        # Initialize NLTK components
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing index and documents
        self.inverted_index = self._load_index()
        self.documents = self._load_documents()
        
    def _load_index(self) -> Dict[str, Dict[int, int]]:
        """Load the inverted index from file."""
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_documents(self) -> Dict[int, Dict]:
        """Load documents from file."""
        if os.path.exists(self.documents_file):
            with open(self.documents_file, 'r') as f:
                return {int(k): v for k, v in json.load(f).items()}
        return {}
    
    def _save_index(self):
        """Save the inverted index to file."""
        with open(self.index_file, 'w') as f:
            json.dump(self.inverted_index, f, indent=2)
    
    def _save_documents(self):
        """Save documents to file."""
        with open(self.documents_file, 'w') as f:
            json.dump(self.documents, f, indent=2)
    
    def _preprocess_text(self, text: str) -> List[str]:
        """Tokenize, remove stopwords, and stem text."""
        # Convert to lowercase and tokenize
        tokens = word_tokenize(text.lower())
        
        # Remove non-alphabetic tokens and stopwords
        tokens = [token for token in tokens if token.isalpha() and token not in self.stop_words]
        
        # Stem tokens
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        
        return stemmed_tokens
    
    def add_document(self, doc_id: int, title: str, content: str, url: str = ""):
        """Add a document to the search engine."""
        # Store document
        self.documents[doc_id] = {
            'title': title,
            'content': content,
            'url': url
        }
        
        # Process text for indexing
        full_text = f"{title} {content}"
        tokens = self._preprocess_text(full_text)
        
        # Update inverted index
        token_counts = Counter(tokens)
        for token, count in token_counts.items():
            if token not in self.inverted_index:
                self.inverted_index[token] = {}
            self.inverted_index[token][doc_id] = count
        
        # Save to disk
        self._save_index()
        self._save_documents()
        
        print(f"Added document {doc_id}: '{title}'")
    
    def search(self, query: str, max_results: int = 10) -> List[Tuple[int, float, Dict]]:
        """Search for documents matching the query."""
        query_tokens = self._preprocess_text(query)
        
        if not query_tokens:
            return []
        
        # Calculate document scores
        doc_scores = defaultdict(float)
        
        for token in query_tokens:
            if token in self.inverted_index:
                # Simple TF scoring
                for doc_id, tf in self.inverted_index[token].items():
                    doc_scores[doc_id] += tf
        
        # Sort by score and return top results
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_id, score in sorted_docs[:max_results]:
            if doc_id in self.documents:
                results.append((doc_id, score, self.documents[doc_id]))
        
        return results
    
    def get_stats(self) -> Dict:
        """Get search engine statistics."""
        return {
            'total_documents': len(self.documents),
            'total_terms': len(self.inverted_index),
            'index_size_kb': os.path.getsize(self.index_file) / 1024 if os.path.exists(self.index_file) else 0
        }
