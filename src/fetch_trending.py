#!/usr/bin/env python3
"""
Fetch trending topics from multiple Chinese platforms
抓取微博、知乎、百度等平台的热搜榜单
"""
import os
import json
import requests
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fetch_weibo_trending():
    """
    抓取微博热搜 (使用公开API)
    """
    try:
        # 使用第三方聚合API - Tenapi (免费)
        url = "https://tenapi.cn/v2/weibohot"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 200:
            items = data.get('data', [])[:20]  # 取前20条
            return [{
                'title': item.get('name', ''),
                'url': item.get('url', '#'),
                'hot': item.get('hot', ''),
                'type': 'weibo'
            } for item in items]
    except Exception as e:
        print(f"Failed to fetch Weibo trending: {e}")
    
    return []

def fetch_zhihu_trending():
    """
    抓取知乎热榜
    """
    try:
        url = "https://tenapi.cn/v2/zhihuhot"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 200:
            items = data.get('data', [])[:15]
            return [{
                'title': item.get('query', ''),
                'url': item.get('url', '#'),
                'hot': item.get('display', ''),
                'type': 'zhihu'
            } for item in items]
    except Exception as e:
        print(f"Failed to fetch Zhihu trending: {e}")
    
    return []

def fetch_baidu_trending():
    """
    抓取百度热搜
    """
    try:
        url = "https://tenapi.cn/v2/baiduhot"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 200:
            items = data.get('data', [])[:15]
            return [{
                'title': item.get('title', ''),
                'url': item.get('url', '#'),
                'hot': item.get('hot', ''),
                'type': 'baidu'
            } for item in items]
    except Exception as e:
        print(f"Failed to fetch Baidu trending: {e}")
    
    return []

def main():
    print("Fetching trending topics...")
    
    # 抓取各平台热搜
    weibo = fetch_weibo_trending()
    zhihu = fetch_zhihu_trending()
    baidu = fetch_baidu_trending()
    
    # 合并数据
    trending_data = {
        'weibo': weibo,
        'zhihu': zhihu,
        'baidu': baidu,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # 保存到 data 目录
    output_path = os.path.join(BASE_DIR, 'data', 'trending.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(trending_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Trending data saved: {len(weibo)} Weibo + {len(zhihu)} Zhihu + {len(baidu)} Baidu")
    print(f"📁 Saved to: {output_path}")

if __name__ == "__main__":
    main()
