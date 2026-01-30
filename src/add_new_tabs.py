#!/usr/bin/env python3
"""
添加三个新榜单标签到HTML
"""
import re

def add_new_trending_tabs():
    html_path = 'templates/index.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 在trending-tabs后添加新标签
    old_tabs = '''                        <div class="trending-tab" data-trending="ai" style="padding: 8px 16px; cursor: pointer; border-radius: 20px; background: #f0f0f0; color: #666; transition: all 0.2s; font-size: 14px; font-weight: 500;">
                            🤖 AI热榜
                        </div>'''
    
    new_tabs = '''                        <div class="trending-tab" data-trending="ai" style="padding: 8px 16px; cursor: pointer; border-radius: 20px; background: #f0f0f0; color: #666; transition: all 0.2s; font-size: 14px; font-weight: 500;">
                            🤖 AI热榜
                        </div>
                        <div class="trending-tab" data-trending="entertainment" style="padding: 8px 16px; cursor: pointer; border-radius: 20px; background: #f0f0f0; color: #666; transition: all 0.2s; font-size: 14px; font-weight: 500;">
                            🎭 娱乐八卦
                        </div>
                        <div class="trending-tab" data-trending="parenting" style="padding: 8px 16px; cursor: pointer; border-radius: 20px; background: #f0f0f0; color: #666; transition: all 0.2s; font-size: 14px; font-weight: 500;">
                            👶 育儿榜
                        </div>
                        <div class="trending-tab" data-trending="gaming" style="padding: 8px 16px; cursor: pointer; border-radius: 20px; background: #f0f0f0; color: #666; transition: all 0.2s; font-size: 14px; font-weight: 500;">
                            🎮 游戏榜
                        </div>'''
    
    content = content.replace(old_tabs, new_tabs)
    
    # 2. 在AI热榜内容后添加新内容区
    marker = '''                </div>
            </div>'''
    
    new_content_areas = '''                </div>

                <!-- 娱乐八卦榜 -->
                <div class="trending-content" id="trending-entertainment" style="display: none;">
                    <div class="feed-card">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            🎭 大馋猫娱乐八卦榜 <span style="font-size: 12px; color: #999; font-weight: normal;">实时热搜</span>
                        </div>
                        {% for item in enriched_trending.entertainment_trending %}
                        <div class="trend-item">
                            <span style="color: #ff1493; font-weight: bold; margin-right: 10px;">{{ loop.index }}</span>
                            <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                            <span class="trend-badge">{{ item.hot }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <!-- 育儿榜 -->
                <div class="trending-content" id="trending-parenting" style="display: none;">
                    <div class="feed-card">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            👶 育儿知识热榜 <span style="font-size: 12px; color: #999; font-weight: normal;">宝宝树热门</span>
                        </div>
                        {% for item in enriched_trending.parenting_trending %}
                        <div class="trend-item">
                            <span style="color: #ffa500; font-weight: bold; margin-right: 10px;">{{ loop.index }}</span>
                            <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                            <span class="trend-badge">{{ item.hot }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <!-- 游戏榜 -->
                <div class="trending-content" id="trending-gaming" style="display: none;">
                    <div class="feed-card">
                        <div style="font-size: 18px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                            🎮 游戏热搜榜 <span style="font-size: 12px; color: #999; font-weight: normal;">Steam | 手游 | 电竞</span>
                        </div>
                        {% for item in enriched_trending.gaming_trending %}
                        <div class="trend-item">
                            <span style="color: #9370db; font-weight: bold; margin-right: 10px;">{{ loop.index }}</span>
                            <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                            <span class="trend-badge">{{ item.hot }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>'''
    
    # 找到AI榜单的结束位置并替换
    # 使用正则表达式找到最后一个trending-content的结束
    pattern = r'(<!-- AI热榜 -->.*?</div>\s*</div>)\s*</div>'
    replacement = r'\1' + new_content_areas
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Successfully added 3 new trending tabs!")
    print("   🎭 娱乐八卦榜")
    print("   👶 育儿榜")
    print("   🎮 游戏榜")

if __name__ == '__main__':
    add_new_trending_tabs()
