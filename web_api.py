#!/usr/bin/env python3
"""
Web API for the Quasar search engine using Flask.
"""

from flask import Flask, request, jsonify, render_template_string
from search_engine import SearchEngine

app = Flask(__name__)
engine = SearchEngine()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quasar Search Engine</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .search-box {
            display: flex;
            margin-bottom: 20px;
        }
        #searchInput {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 6px 0 0 6px;
            font-size: 16px;
        }
        #searchButton {
            padding: 12px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 0 6px 6px 0;
            cursor: pointer;
            font-size: 16px;
        }
        #searchButton:hover {
            background: #0056b3;
        }
        .result {
            border: 1px solid #eee;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
            background: #fafafa;
        }
        .result-title {
            font-weight: bold;
            color: #1a0dab;
            margin-bottom: 5px;
        }
        .result-url {
            color: #006621;
            font-size: 14px;
            margin-bottom: 5px;
        }
        .result-content {
            color: #545454;
            line-height: 1.4;
        }
        .no-results {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 20px;
        }
        .stats {
            background: #e9ecef;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Quasar Search Engine</h1>
        
        <div id="stats" class="stats"></div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Enter your search query..." />
            <button id="searchButton">Search</button>
        </div>
        
        <div id="results"></div>
    </div>

    <script>
        const searchInput = document.getElementById('searchInput');
        const searchButton = document.getElementById('searchButton');
        const resultsDiv = document.getElementById('results');
        const statsDiv = document.getElementById('stats');

        // Load stats on page load
        loadStats();

        function loadStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    statsDiv.innerHTML = `📊 ${data.total_documents} documents indexed | ${data.total_terms} terms | ${data.index_size_kb.toFixed(2)} KB index`;
                });
        }

        function performSearch() {
            const query = searchInput.value.trim();
            if (!query) return;

            searchButton.textContent = 'Searching...';
            searchButton.disabled = true;

            fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            })
            .then(response => response.json())
            .then(data => {
                displayResults(data.results, query);
                searchButton.textContent = 'Search';
                searchButton.disabled = false;
            })
            .catch(error => {
                console.error('Error:', error);
                resultsDiv.innerHTML = '<div class="no-results">Error occurred while searching</div>';
                searchButton.textContent = 'Search';
                searchButton.disabled = false;
            });
        }

        function displayResults(results, query) {
            if (results.length === 0) {
                resultsDiv.innerHTML = `<div class="no-results">No results found for "${query}"</div>`;
                return;
            }

            let html = `<h3>Found ${results.length} results for "${query}":</h3>`;
            
            results.forEach(result => {
                const [docId, score, doc] = result;
                html += `
                    <div class="result">
                        <div class="result-title">${doc.title}</div>
                        ${doc.url ? `<div class="result-url">${doc.url}</div>` : ''}
                        <div class="result-content">${doc.content.substring(0, 200)}${doc.content.length > 200 ? '...' : ''}</div>
                    </div>
                `;
            });
            
            resultsDiv.innerHTML = html;
        }

        searchButton.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main search interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search', methods=['POST'])
def search():
    """Search API endpoint."""
    data = request.get_json()
    query = data.get('query', '')
    max_results = data.get('max_results', 10)
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    results = engine.search(query, max_results)
    
    return jsonify({
        'query': query,
        'results': results,
        'total_results': len(results)
    })

@app.route('/api/add', methods=['POST'])
def add_document():
    """Add document API endpoint."""
    data = request.get_json()
    
    required_fields = ['id', 'title', 'content']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    doc_id = data['id']
    title = data['title']
    content = data['content']
    url = data.get('url', '')
    
    try:
        engine.add_document(doc_id, title, content, url)
        return jsonify({'message': f'Document {doc_id} added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def stats():
    """Get search engine statistics."""
    return jsonify(engine.get_stats())

if __name__ == '__main__':
    print("Starting Quasar Search Engine Web API...")
    print("Visit http://localhost:5000 to use the web interface")
    app.run(debug=True, host='0.0.0.0', port=5000)
