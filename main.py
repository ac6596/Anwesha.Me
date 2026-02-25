import os
import re
from pathlib import Path
from flask import Flask, request, render_template, abort
import markdown

# Initialize Flask app, serving static files from the 'app' directory
app = Flask(__name__, static_folder='app', static_url_path='', template_folder='templates')

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
