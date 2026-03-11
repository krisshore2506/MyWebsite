import os
import re

html_files = ['index.html', 'study.html', 'stress.html', 'timer.html', 'contact.html', 'dashboard.html']
base_dir = r"c:\Users\KRISSHORE S\OneDrive\Desktop\MyWebsite\templates"

new_sidebar = """<div class="sidebar" id="sidebar">
    <div class="sidebar-header">
        <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" class="sidebar-logo">
        <h2>Menu</h2>
    </div>

    <div class="sidebar-links">
        <a href="{{ url_for('home') }}" class="{% if request.endpoint == 'home' %}active{% endif %}">
            <span class="icon">🏠</span>
            <span class="text">Home</span>
        </a>
        <a href="{{ url_for('study') }}" class="{% if request.endpoint == 'study' %}active{% endif %}">
            <span class="icon">📚</span>
            <span class="text">Study Techniques</span>
        </a>
        <a href="{{ url_for('stress') }}" class="{% if request.endpoint == 'stress' %}active{% endif %}">
            <span class="icon">🧘</span>
            <span class="text">Stress Tips</span>
        </a>
        <a href="{{ url_for('timer') }}" class="{% if request.endpoint == 'timer' %}active{% endif %}">
            <span class="icon">⏱️</span>
            <span class="text">Timer</span>
        </a>
        <a href="{{ url_for('contact') }}" class="{% if request.endpoint == 'contact' %}active{% endif %}">
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

for f in html_files:
    path = os.path.join(base_dir, f)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Use regex to find the menu-toggle and everything till <!-- Main Content --> or <div class="content">
    # Wait, in study.html, we have:
    # <div class="menu-toggle" onclick="toggleMenu()">☰</div>
    # ...
    # <div class="sidebar"> ... </div>
    # Let's replace the whole sidebar div.
    pattern = r'<div class="sidebar"(?: id="sidebar")?>.*?(?=<!-- Main Content -->|<div class="content">)'
    content = re.sub(pattern, new_sidebar + '\n\n    ', content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
        
css_path = r"c:\Users\KRISSHORE S\OneDrive\Desktop\MyWebsite\static\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Replace existing custom sidebar header and links styles to make it perfect
header_fix = """
.sidebar-header {
    text-align: center;
    padding: 70px 20px 10px; /* Pushed down to avoid toggle button overlapping */
}

.sidebar-logo {
    height: 55px; /* Sizing logo stringently between 50-60px */
    width: auto;
    filter: drop-shadow(0 0 10px #00f7ff);
    margin-bottom: 10px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}
"""

css_content = re.sub(r'\.sidebar-header\s*\{[^}]*\}', '', css_content)
css_content = re.sub(r'\.sidebar-logo\s*\{[^}]*\}', '', css_content)
css_content += "\n" + header_fix

# Add active state and update normal hover state
active_fix = """
.sidebar a.active {
    background: rgba(0, 247, 255, 0.2);
    border-left: 4px solid #00f7ff;
    box-shadow: inset 15px 0 20px -15px rgba(0, 247, 255, 0.6);
    color: #00f7ff;
}

.sidebar a.active .text {
    text-shadow: 0 0 8px #00f7ff;
    font-weight: bold;
}
"""

if ".sidebar a.active" not in css_content:
    css_content += active_fix

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)

print("Sidebar perfectly aligned and updated in all pages!")
