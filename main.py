import os
from flask import Flask, request

# Initialize Flask app, serving static files from the 'app' directory
app = Flask(__name__, static_folder='app', static_url_path='')

@app.route('/')
def index():
    """Serves the main frontend page."""
    return app.send_static_file('index.html')

@app.route('/hello', methods=['POST'])
def hello():
    """Simple hello endpoint migrated from hello_routes.js."""
    return 'Hello'

@app.route('/bello', methods=['GET'])
def bello():
    """Bello endpoint migrated from bello_routes.js, adds two numbers."""
    try:
        num1 = float(request.args.get('num1', 0))
        num2 = float(request.args.get('num2', 0))
        result = num1 + num2
        # Use int representation if it's a whole number, to precisely match string format
        if result.is_integer():
            return str(int(result))
        return str(result)
    except ValueError:
        return "Invalid input", 400

if __name__ == '__main__':
    # Start the application on the port specified by the PORT environment variable
    # Defaults to 8080 if not set (suitable for Cloud Run testing locally)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
