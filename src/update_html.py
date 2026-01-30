#!/usr/bin/env python3
"""
自动更新HTML文件，添加榜单子标签和视频内容
"""
import re

def update_html():
    html_path = 'templates/index.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 更新榜单视图 - 添加子标签
    trending_view_new = '''            <!-- View: Trending (Hot Rankings) -->
            <div id="view-trending" class="view-content active">
                <!-- 榜单子标签 -->
                <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <div class="trending-tabs" style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <div class="trending-tab active" data-trending="weibo" style="padding: 8px 16px; cursor: pointer; border-radius: 20px; background: var(--accent); color: white; transition: all 0.2s; font-size: 14px; font-weight: 500;">
                            🔥 今日头条
                        </div>
                        <div class="trending-tab" data-trending="zhihu" style="padding: 8px 16px; cursor: pointer; border-radius: 20px; background: #f0f0f0; color: #666; transition: all 0.2s; font-size: 14px; font-weight: 500;">
                            💬 知乎热榜
                        </div>
                        <div class="trending-tab" data-trending="bilibili" style="padding: 8px 16px; cursor: pointer; border-radius: 20px; background: #f0f0f0; color: #666; transition: all 0.2s; font-size: 14px; font-weight: 500;">
                            📺 B站热门
                        </div>
                        <div class="trending-tab" data-trending="ai" style="padding: 8px 16px; cursor: pointer; border-radius: 20px; background: #f0f0f0; color: #666; transition: all 0.2s; font-size: 14px; font-weight: 500;">
                            🤖 AI热榜
                        </div>
                    </div>
                </div>

                <!-- 今日头条 -->
                <div class="trending-content" id="trending-weibo">
                    <div class="feed-card">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            🔥 今日头条榜 <span style="font-size: 12px; color: #999; font-weight: normal;">实时更新</span>
                        </div>
                        {% for item in enriched_trending.domestic_trending.weibo %}
                        <div class="trend-item">
                            <span style="color: var(--accent); font-weight: bold; margin-right: 10px;">{{ loop.index }}</span>
                            <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                            <span class="trend-badge">{{ item.hot }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <!-- 知乎热榜 -->
                <div class="trending-content" id="trending-zhihu" style="display: none;">
                    <div class="feed-card">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            💬 知乎热榜 <span style="font-size: 12px; color: #999; font-weight: normal;">热度Top50</span>
                        </div>
                        {% for item in enriched_trending.domestic_trending.zhihu %}
                        <div class="trend-item">
                            <span style="color: #0084ff; font-weight: bold; margin-right: 10px;">{{ loop.index }}</span>
                            <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                            <span class="trend-badge">{{ item.hot }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <!-- B站热门 -->
                <div class="trending-content" id="trending-bilibili" style="display: none;">
                    <div class="feed-card">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            📺 B站热门 <span style="font-size: 12px; color: #999; font-weight: normal;">综合榜</span>
                        </div>
                        {% for item in enriched_trending.domestic_trending.bilibili %}
                        <div class="trend-item">
                            <span style="color: #00a1d6; font-weight: bold; margin-right: 10px;">{{ loop.index }}</span>
                            <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                            <span class="trend-badge">{{ item.hot }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <!-- AI热榜 -->
                <div class="trending-content" id="trending-ai" style="display: none;">
                    <div class="feed-card">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            🚀 Product Hunt AI <span style="font-size: 12px; color: #999; font-weight: normal;">今日最热</span>
                        </div>
                        {% for item in enriched_trending.ai_trending.producthunt %}
                        <div class="trend-item">
                            <span style="color: #da552f; font-weight: bold; margin-right: 10px;">{{ loop.index }}</span>
                            <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                            <span class="trend-badge">👍 {{ item.votes }}</span>
                        </div>
                        {% endfor %}
                    </div>
                    <div class="feed-card">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            🤗 HuggingFace热门模型 <span style="font-size: 12px; color: #999; font-weight: normal;">下载量排行</span>
                        </div>
                        {% for item in enriched_trending.ai_trending.huggingface %}
                        <div class="trend-item">
                            <span style="color: #ffcc00; font-weight: bold; margin-right: 10px;">{{ loop.index }}</span>
                            <a href="{{ item.url }}" target="_blank" style="font-family: monospace; font-size: 12px;">{{ item.title }}</a>
                            <span class="trend-badge">⬇️ {{ item.downloads }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>'''
    
    # 替换榜单视图
    pattern = r'<!-- View: Trending \(Hot Rankings\) -->.*?(?=<!-- View:|</div>\s*</div>\s*<div class="right-sidebar">)'
    content = re.sub(pattern, trending_view_new + '\n        ', content, flags=re.DOTALL)
    
    # 保存
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ HTML updated successfully!")
    print("   - Added trending sub-tabs (Weibo/Zhihu/Bilibili/AI)")
    print("   - Updated data source to enriched_trending")

if __name__ == '__main__':
    update_html()
