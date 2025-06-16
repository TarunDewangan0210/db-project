from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import json
import os
import sys

app = Flask(__name__)
CORS(app)

@app.route('/api/analysis')
def get_analysis():
    try:
        # Get the absolute path to analysis_queries.py
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'analysis_queries.py')
        
        # Run the analysis script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode != 0:
            print(f"Error running analysis script: {result.stderr}")
            return jsonify({'error': 'Failed to run analysis script'}), 500

        # Parse the output from analysis_queries.py
        try:
            # The script should output JSON data
            analysis_data = json.loads(result.stdout)
            return jsonify(analysis_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON output: {e}")
            print(f"Script output: {result.stdout}")
            return jsonify({'error': 'Failed to parse analysis results'}), 500

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 