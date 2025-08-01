# Quasar - Minimal Search Engine

A lightweight, fast search engine built in Python with both CLI and web interfaces. Designed for the midnight browser project.

## Features

- **Document Indexing**: Add documents with title, content, and optional URL
- **Full-Text Search**: Search across document titles and content
- **Multiple Interfaces**: Command-line interface and web API
- **Persistent Storage**: JSON-based storage for documents and search index
- **Text Processing**: Tokenization, stemming, and stopword removal using NLTK
- **TF Scoring**: Simple term frequency scoring for search results

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Quasar
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Load sample data (optional):
```bash
python sample_data.py
```

## Usage

### Command Line Interface

**Add a document:**
```bash
python cli.py add --id 1 --title "My Document" --content "Document content here" --url "https://example.com"
```

**Search for documents:**
```bash
python cli.py search "machine learning"
```

**Interactive search mode:**
```bash
python cli.py interactive
```

**View statistics:**
```bash
python cli.py stats
```

### Web Interface

1. Start the web server:
```bash
python web_api.py
```

2. Open your browser to `http://localhost:5000`

### API Endpoints

- `GET /` - Web search interface
- `POST /api/search` - Search documents
- `POST /api/add` - Add new document
- `GET /api/stats` - Get search engine statistics

## Architecture

### Core Components

1. **SearchEngine Class** (`search_engine.py`)
   - Document indexing and storage
   - Inverted index for fast searching
   - Text preprocessing (tokenization, stemming, stopword removal)
   - TF-based scoring algorithm

2. **CLI Interface** (`cli.py`)
   - Command-line tools for document management and searching
   - Interactive search mode

3. **Web API** (`web_api.py`)
   - Flask-based REST API
   - Modern web interface with real-time search

### Data Storage

- `data/documents.json` - Document storage
- `data/index.json` - Inverted index for search

### Text Processing Pipeline

1. Tokenization using NLTK
2. Lowercase conversion
3. Stopword removal
4. Porter stemming
5. Term frequency calculation

## Example Usage

```python
from search_engine import SearchEngine

# Initialize search engine
engine = SearchEngine()

# Add a document
engine.add_document(
    doc_id=1,
    title="Python Tutorial",
    content="Learn Python programming with examples",
    url="https://example.com/python"
)

# Search for documents
results = engine.search("python programming")
for doc_id, score, doc in results:
    print(f"{doc['title']} (Score: {score})")
```

## Contributing

This is a minimal search engine designed for educational purposes and the midnight browser project. Feel free to extend it with additional features like:

- TF-IDF scoring
- Boolean queries
- Phrase searching
- Document ranking algorithms
- Web crawling capabilities

## License

Open source - feel free to use and modify as needed.

