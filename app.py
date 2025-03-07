import os
import sys
from flask import Flask, request, jsonify, render_template
from agents.orchestrator_agent import OrchestratorAgent
from utils.data_loader import DataLoader
from utils.llm_utils import LLMHandler
from config import DEBUG, HOST, PORT

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize data loader and LLM handler
data_loader = DataLoader()
llm_handler = LLMHandler()

# Initialize orchestrator agent
orchestrator = OrchestratorAgent(llm_handler, data_loader)

@app.route('/')
def index():
    """
    Render the main page
    """
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def process_query():
    """
    Process a user query
    """
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({
            'error': 'No query provided'
        }), 400
    
    # Process the query using the orchestrator
    result = orchestrator.process_query(query)
    
    return jsonify({
        'response': result['response'],
        'agent': result['agent'],
        'confidence': result['confidence'],
        'explanation': result['explanation']
    })

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """
    Get a list of available agents
    """
    agents = []
    for name, agent in orchestrator.agents.items():
        agents.append({
            'name': name,
            'description': agent.get_description()
        })
    
    return jsonify({
        'agents': agents
    })

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Tap Bonds AI Assistant is running'
    })

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Copy data files from data_dump to data directory
    data_dump_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_dump")
    if os.path.exists(data_dump_dir):
        for file in os.listdir(data_dump_dir):
            src = os.path.join(data_dump_dir, file)
            dst = os.path.join(data_dir, file)
            if not os.path.exists(dst) and os.path.isfile(src):
                print(f"Copying {src} to {dst}")
                with open(src, 'rb') as f_src, open(dst, 'wb') as f_dst:
                    f_dst.write(f_src.read())
    
    # Get port from environment variable for Heroku/Render compatibility
    port = int(os.environ.get('PORT', PORT))
    
    # Run the app
    app.run(debug=DEBUG, host=HOST, port=port) 