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

    tools_data = load_data('tools.json')
    tools_items = tools_data.get('tools', []) if isinstance(tools_data, dict) else []

    showcase_data = load_data('showcase.json')
    showcase_items = showcase_data.get('showcase', []) if isinstance(showcase_data, dict) else []

    trending_data = load_data('trending.json')
    trending_items = trending_data if isinstance(trending_data, dict) else {}
    
    enriched_data = load_data('enriched_trending.json')
    enriched_trending = enriched_data if isinstance(enriched_data, dict) else {}
    
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
        'tools_items': tools_items,
        'showcase_items': showcase_items,
        'trending_items': trending_items,
        'enriched_trending': enriched_trending,
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
