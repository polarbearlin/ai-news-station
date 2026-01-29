import json
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Calculate base directory (one level up from src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data(filename):
    path = os.path.join(BASE_DIR, 'data', filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    print(f"Warning: Data file not found at {path}")
    return []

def generate_html():
    print(f"Generating static site... Base Dir: {BASE_DIR}")
    
    # Load data
    news_data = load_data('news.json')
    news_items = news_data.get('news', []) if isinstance(news_data, dict) else []
    
    github_items = load_data('github.json')
    
    # Prepare template environment
    template_dir = os.path.join(BASE_DIR, 'templates')
    if not os.path.exists(template_dir):
        print(f"Error: Template directory not found at {template_dir}")
        return

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('index.html')
    
    # Context
    context = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'news_items': news_items,
        'github_items': github_items,
    }
    
    # Render
    html_content = template.render(context)
    
    # Output
    output_dir = os.path.join(BASE_DIR, 'dist')
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(html_content)
        
    print(f"Site generated at {output_dir}/index.html")

if __name__ == "__main__":
    generate_html()
