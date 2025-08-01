#!/usr/bin/env python3
"""
Command-line interface for the Quasar search engine.
"""

import argparse
import sys
from search_engine import SearchEngine

def main():
    parser = argparse.ArgumentParser(description='Quasar - Minimal Search Engine')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add document command
    add_parser = subparsers.add_parser('add', help='Add a document to the index')
    add_parser.add_argument('--id', type=int, required=True, help='Document ID')
    add_parser.add_argument('--title', required=True, help='Document title')
    add_parser.add_argument('--content', required=True, help='Document content')
    add_parser.add_argument('--url', default='', help='Document URL (optional)')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for documents')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--max-results', type=int, default=10, help='Maximum number of results')
    
    # Stats command
    subparsers.add_parser('stats', help='Show search engine statistics')
    
    # Interactive mode
    subparsers.add_parser('interactive', help='Start interactive search mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize search engine
    engine = SearchEngine()
    
    if args.command == 'add':
        engine.add_document(args.id, args.title, args.content, args.url)
        
    elif args.command == 'search':
        results = engine.search(args.query, args.max_results)
        
        if not results:
            print("No results found.")
            return
        
        print(f"Found {len(results)} results for '{args.query}':\n")
        
        for i, (doc_id, score, doc) in enumerate(results, 1):
            print(f"{i}. {doc['title']} (Score: {score:.2f})")
            print(f"   ID: {doc_id}")
            if doc['url']:
                print(f"   URL: {doc['url']}")
            print(f"   Content: {doc['content'][:100]}{'...' if len(doc['content']) > 100 else ''}")
            print()
    
    elif args.command == 'stats':
        stats = engine.get_stats()
        print("Search Engine Statistics:")
        print(f"  Total Documents: {stats['total_documents']}")
        print(f"  Total Terms: {stats['total_terms']}")
        print(f"  Index Size: {stats['index_size_kb']:.2f} KB")
    
    elif args.command == 'interactive':
        print("Quasar Interactive Search Mode")
        print("Type 'quit' or 'exit' to leave")
        print("-" * 40)
        
        while True:
            try:
                query = input("\nSearch> ").strip()
                
                if query.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                if not query:
                    continue
                
                results = engine.search(query)
                
                if not results:
                    print("No results found.")
                    continue
                
                print(f"\nFound {len(results)} results:")
                
                for i, (doc_id, score, doc) in enumerate(results, 1):
                    print(f"\n{i}. {doc['title']} (Score: {score:.2f})")
                    if doc['url']:
                        print(f"   URL: {doc['url']}")
                    print(f"   {doc['content'][:150]}{'...' if len(doc['content']) > 150 else ''}")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break

if __name__ == '__main__':
    main()
