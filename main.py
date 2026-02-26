import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, render_template, abort
import markdown
from google.cloud import pubsub_v1

# Initialize Flask app, serving static files from the 'app' directory
app = Flask(__name__, static_folder='app', static_url_path='', template_folder='templates')

PUBSUB_TOPIC_ID = "anwesha-net-msg-topic"


def publish_message(payload: dict) -> str:
    """
    Serialize *payload* to JSON and publish it to the configured Pub/Sub topic.

    Authentication is handled automatically by Application Default Credentials
    (ADC) — no hardcoded key path is required. On Cloud Run, the attached
    service account is used transparently.

    Args:
        payload: A dictionary of form data to publish.

    Returns:
        The Pub/Sub message ID string on success.

    Raises:
        EnvironmentError: If GCP_PROJECT_ID is not set.
        Exception: Propagates any Pub/Sub client error to the caller.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise EnvironmentError("GCP_PROJECT_ID environment variable is not set")

    publisher  = pubsub_v1.PublisherClient()   # keyless — uses ADC / service account
    topic_path = publisher.topic_path(project_id, PUBSUB_TOPIC_ID)
    future     = publisher.publish(
        topic_path,
        data=json.dumps(payload).encode("utf-8"),
        content_type="application/json",
    )
    return future.result(timeout=10)

POSTS_DIR = Path(__file__).parent / 'posts'


def parse_post(path):
    """Parse a Markdown file with YAML-style frontmatter (--- delimited)."""
    text = path.read_text(encoding='utf-8')
    meta = {}
    body = text

    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ':' in line:
                    key, _, val = line.partition(':')
                    meta[key.strip()] = val.strip().strip('"')
            body = parts[2].strip()

    return {
        'slug': path.stem,
        'title': meta.get('title', path.stem.replace('-', ' ').title()),
        'date': meta.get('date', ''),
        'excerpt': meta.get('excerpt', ''),
        'content': markdown.markdown(body, extensions=['tables', 'fenced_code']),
    }


def get_all_posts():
    """Return all posts sorted newest-first."""
    posts = [parse_post(p) for p in sorted(POSTS_DIR.glob('*.md'), reverse=True)]
    return posts


@app.route('/')
def index():
    """Serves the main frontend page."""
    return app.send_static_file('index.html')


@app.route('/blog')
def blog_list():
    """Lists all blog posts."""
    posts = get_all_posts()
    return render_template('blog_list.html', posts=posts)


@app.route('/blog/<slug>')
def blog_post(slug):
    """Renders a single blog post by slug."""
    post_path = POSTS_DIR / f'{slug}.md'
    if not post_path.exists():
        abort(404)
    post = parse_post(post_path)
    return render_template('blog_post.html', **post)


@app.route('/contact', methods=['POST'])
def contact():
    """
    Accepts a JSON contact form submission and publishes it to
    GCP Pub/Sub topic anwesha-net-msg-topic.

    Expected JSON body: { "name": "...", "email": "...", "message": "..." }
    """
    body = request.get_json(force=True, silent=True)
    if not body:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    name    = str(body.get("name",    "")).strip()
    email   = str(body.get("email",   "")).strip()
    message = str(body.get("message", "")).strip()

    # Input validation
    if not all([name, email, message]):
        return jsonify({"error": "name, email and message are all required"}), 422

    if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
        return jsonify({"error": "Invalid email format"}), 422

    payload = {
        "name":      name,
        "email":     email,
        "message":   message,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    try:
        message_id = publish_message(payload)
    except EnvironmentError as exc:
        app.logger.error("Server misconfiguration: %s", exc)
        return jsonify({"error": "Server misconfiguration. Please contact the administrator."}), 500
    except Exception as exc:
        # Log full traceback to Cloud Logging; don't leak internals to the caller
        app.logger.exception("Pub/Sub publish failed: %s", exc)
        return jsonify({"error": "Failed to submit message. Please try again."}), 502

    return jsonify({"status": "sent", "message_id": message_id}), 200


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
        if result.is_integer():
            return str(int(result))
        return str(result)
    except ValueError:
        return "Invalid input", 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
