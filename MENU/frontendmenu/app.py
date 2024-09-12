from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'try2.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    script_path = request.json.get('script')
    
    if not script_path:
        return jsonify({'error': 'No script specified'}), 400
    
    if not os.path.isfile(script_path):
        return jsonify({'error': 'Script file does not exist'}), 400
    
    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        return jsonify({'output': result.stdout, 'error': result.stderr}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/open-html', methods=['POST'])
def open_html():
    file_path = request.json.get('file_path')

    if not file_path:
        return jsonify({'error': 'No file path specified'}), 400
    
    if not os.path.isfile(file_path):
        return jsonify({'error': 'HTML file does not exist'}), 400

    try:
        # Open the HTML file in the browser
        webbrowser.open(f'file://{os.path.abspath(file_path)}')
        return jsonify({'message': 'HTML file opened successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
