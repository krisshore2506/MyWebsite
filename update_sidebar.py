import os
import re

files = ['index.html', 'stress.html', 'study.html', 'timer.html', 'contact.html', 'dashboard.html']
base_dir = r"c:\Users\KRISSHORE S\OneDrive\Desktop\MyWebsite\templates"

new_sidebar = """<div class="sidebar" id="sidebar">
    <div class="sidebar-header">
        <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" class="sidebar-logo">
        <h2>Menu</h2>
    </div>

    <div class="sidebar-links">
        <a href="/">
            <span class="icon">🏠</span>
            <span class="text">Home</span>
        </a>
        <a href="/study">
            <span class="icon">📚</span>
            <span class="text">Study</span>
        </a>
        <a href="/stress">
            <span class="icon">🧘</span>
            <span class="text">Stress Tips</span>
        </a>
        <a href="/timer">
            <span class="icon">⏱️</span>
            <span class="text">Timer</span>
        </a>
        <a href="/contact">
            <span class="icon">✉️</span>
            <span class="text">Contact</span>
        </a>
    </div>

    <div class="sidebar-footer">
        <hr style="border-color: rgba(0, 247, 255, 0.3); margin: 15px 20px;">
        {% if session.user_email %}
            <a href="{{ url_for('logout') }}" class="logout-link">
                <span class="icon">🚪</span>
                <span class="text">Logout</span>
            </a>
        {% else %}
            <a href="{{ url_for('login') }}" class="login-link">
                <span class="icon">🔑</span>
                <span class="text">Login</span>
            </a>
        {% endif %}
    </div>
</div>"""

for f in files:
    path = os.path.join(base_dir, f)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    pattern = r'<div class="sidebar" id="sidebar">.*?(?=<!-- Main Content -->|<div class="content">)'
    content = re.sub(pattern, new_sidebar + '\n\n    ', content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
        
print("Sidebar updated")
