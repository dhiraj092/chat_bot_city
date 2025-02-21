# app.py
from flask import Flask, render_template, request, jsonify
from query_data import EnhancedQueryProcessor
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize the query processor
try:
    processor = EnhancedQueryProcessor()
except ValueError as e:
    print(f"Error: {e}")
    exit(1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def process_query():
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    result = processor.process_query(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)