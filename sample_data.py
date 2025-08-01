#!/usr/bin/env python3
"""
Sample data loader for the Quasar search engine.
"""

from search_engine import SearchEngine

def load_sample_data():
    """Load sample documents into the search engine."""
    engine = SearchEngine()
    
    # Sample documents
    documents = [
        {
            'id': 1,
            'title': 'Introduction to Machine Learning',
            'content': 'Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data. It includes supervised learning, unsupervised learning, and reinforcement learning approaches.',
            'url': 'https://example.com/ml-intro'
        },
        {
            'id': 2,
            'title': 'Python Programming Basics',
            'content': 'Python is a high-level programming language known for its simplicity and readability. It supports multiple programming paradigms including procedural, object-oriented, and functional programming.',
            'url': 'https://example.com/python-basics'
        },
        {
            'id': 3,
            'title': 'Web Development with Flask',
            'content': 'Flask is a lightweight web framework for Python. It provides tools and libraries to build web applications quickly and efficiently. Flask follows the WSGI standard and is highly extensible.',
            'url': 'https://example.com/flask-guide'
        },
        {
            'id': 4,
            'title': 'Data Structures and Algorithms',
            'content': 'Understanding data structures like arrays, linked lists, trees, and graphs is fundamental to computer science. Algorithms for searching, sorting, and optimization are essential skills for programmers.',
            'url': 'https://example.com/dsa'
        },
        {
            'id': 5,
            'title': 'Natural Language Processing',
            'content': 'Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and human language. It includes tasks like tokenization, stemming, and sentiment analysis.',
            'url': 'https://example.com/nlp'
        }
    ]
    
    print("Loading sample documents...")
    for doc in documents:
        engine.add_document(doc['id'], doc['title'], doc['content'], doc['url'])
    
    print(f"\nLoaded {len(documents)} sample documents!")
    
    # Show stats
    stats = engine.get_stats()
    print(f"Total documents: {stats['total_documents']}")
    print(f"Total terms: {stats['total_terms']}")
    
    return engine

if __name__ == '__main__':
    load_sample_data()
