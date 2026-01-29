import requests
import json
import json
import os
from datetime import datetime, timedelta

def fetch_hacker_news_ai(limit=20):
    """Fetch AI-related stories from Hacker News."""
    print("Fetching Hacker News AI stories...")
    # HN API top stories
    try:
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        top_ids = requests.get(top_stories_url, timeout=10).json()
        
        ai_keywords = ['ai', 'gpt', 'llm', 'machine learning', 'diffusion', 'transformer', 'neural', 'deepseek', 'openai', 'anthropic']
        
        stories = []
        count = 0
        
        # We might need to scan more to find AI topics
        scan_limit = 10 
        
        for item_id in top_ids[:scan_limit]:
            if count >= limit:
                break
                
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
            try:
                item = requests.get(item_url, timeout=10).json()
                if not item or 'title' not in item or 'url' not in item:
                    continue
                
                title = item['title'].lower()
                if any(kw in title for kw in ai_keywords):
                    stories.append({
                        'title': item['title'],
                        'url': item.get('url', f"https://news.ycombinator.com/item?id={item_id}"),
                        'source': 'Hacker News',
                        'time': datetime.fromtimestamp(item.get('time', 0)).strftime('%Y-%m-%d %H:%M'),
                        'score': item.get('score', 0),
                        'comments': item.get('descendants', 0)
                    })
                    count += 1
            except Exception as e:
                print(f"Error fetching item {item_id}: {e}")
                
        return stories
    except Exception as e:
        print(f"Error fetching Hacker News: {e}")
        return []

def main():
    stories = fetch_hacker_news_ai()
    
    # Save to data.json
    output = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'news': stories
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/news.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(stories)} stories to data/news.json")

if __name__ == "__main__":
    main()
