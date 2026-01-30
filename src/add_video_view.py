#!/usr/bin/env python3
"""
在HTML文件的榜单视图后添加视频视图
"""

def add_video_view():
    html_path = 'templates/index.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 视频视图HTML
    video_view = '''
            <!-- View: Video (AI Videos) -->
            <div id="view-video" class="view-content">
                {% for video in enriched_trending.ai_videos %}
                <div class="feed-card" data-category="video">
                    <div class="card-header">
                        <div class="avatar" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; display: flex; align-items: center; justify-content: center; font-size: 20px;">
                            📺
                        </div>
                        <div class="user-info">
                            <div class="username">AI视频精选</div>
                            <div class="time">{{ video.duration }} · {{ video.views }} 观看</div>
                        </div>
                    </div>
                    <div class="content-text">
                        <a href="{{ video.url }}" target="_blank" style="color: inherit; text-decoration: none; font-weight: 500;">
                            {{ video.title }}
                        </a>
                    </div>
                    <div style="background: #f5f5f5; padding: 10px; border-radius: 8px; margin: 10px 0; display: flex; align-items: center; gap: 10px;">
                        <div style="width: 120px; height: 70px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;">
                            ▶️
                        </div>
                        <div style="flex: 1;">
                            <div style="font-size: 12px; color: #666;">时长: {{ video.duration }}</div>
                            <div style="font-size: 12px; color: #666; margin-top: 4px;">{{ video.views }} 次播放</div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <span class="action-btn">🔁 转发</span>
                        <span class="action-btn">💬 评论</span>
                        <span class="action-btn">👍 赞</span>
                    </div>
                </div>
                {% endfor %}
            </div>
'''
    
    # 在trending视图后插入
    marker = '</div>\n        </div>\n\n        <div class="right-sidebar">'
    if marker in content:
        parts = content.split(marker, 1)
        content = parts[0] + video_view + '\n        </div>\n\n        <div class="right-sidebar">' + parts[1]
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Video view added successfully!")
        return True
    else:
        print("❌ Could not find insertion point")
        return False

if __name__ == '__main__':
    add_video_view()
