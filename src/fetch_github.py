import requests
import json
import os
from datetime import datetime, timedelta

def fetch_github_trends(limit=10):
    """Fetch trending AI repositories from GitHub."""
    print("Fetching GitHub AI trends...")
    try:
        # Search for AI related topics created or updated recently with high stars
        # Query: topic:ai OR topic:machine-learning sort:stars
        
        # Date 7 days ago
        date_7_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        query = f"topic:ai created:>{date_7_days_ago}"
        
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
        headers = {
            "Accept": "application/vnd.github.v3+json"
            # "Authorization": "token YOUR_GITHUB_TOKEN" # Added via env var in Action
        }
        
        # Check for env var
        if os.environ.get("GITHUB_TOKEN"):
             headers["Authorization"] = f"token {os.environ.get('GITHUB_TOKEN')}"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"GitHub API Error: {response.status_code} - {response.text}")
            return []
            
        items = response.json().get('items', [])
        repos = []
        
        for item in items:
            repos.append({
                'name': item['name'],
                'full_name': item['full_name'],
                'description': item['description'],
                'url': item['html_url'],
                'stars': item['stargazers_count'],
                'language': item['language'],
                'updated_at': item['updated_at']
            })
            
        return repos
    except Exception as e:
        print(f"Error fetching GitHub trends: {e}")
        return []

def main():
    repos = fetch_github_trends()
    
    os.makedirs('data', exist_ok=True)
    with open('data/github.json', 'w') as f:
        json.dump(repos, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(repos)} repos to data/github.json")

if __name__ == "__main__":
    main()
