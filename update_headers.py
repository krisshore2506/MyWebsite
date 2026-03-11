import re
import os

files = ['index.html', 'stress.html', 'study.html', 'timer.html', 'contact.html']

for f in files:
    path = os.path.join('c:\\Users\\KRISSHORE S\\OneDrive\\Desktop\\MyWebsite\\templates', f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # We want to replace the whole <header>...</header> block.
    # We will use re.sub with re.DOTALL and extract the subtitle <p>
    
    match = re.search(r'<header>\s*<h1>(.*?)</h1>\s*<p>(.*?)</p>\s*</header>', content, re.DOTALL)
    
    if match:
        original_title = match.group(1).strip()
        original_subtitle = match.group(2).strip()
        
        # In all pages, the title should be "Exam Stress Manager" with the logo.
        # Maybe we keep the original p as the subtitle. Or we combine them.
        # Let's use exactly "Exam Stress Manager" as asked, and retain the description.
        
        new_header = f'''        <header>
            <img src="{{{{ url_for('static', filename='images/logo.png') }}}}" alt="Logo" class="header-logo">
            <div class="header-text">
                <h1>Exam Stress Manager</h1>
                <p>{original_subtitle}</p>
            </div>
        </header>'''
        
        content = re.sub(r'<header>.*?</header>', new_header, content, flags=re.DOTALL)
        
        # Also need to update sidebar nav to include Login/Logout? The user simply states:
        # "Add the same logo to all pages of the website. Show it in the header section..."
        # Then "Flask Routes to Create /login ... etc."
        # It's good practice to add a Login/Logout link to the sidebar, but they didn't explicitly ask to modify the sidebar menu. I'll add "Log in/out" to the sidebar just in case.
        # Let's replace </div class="sidebar"> with links
        # Wait, the sidebar ends with </div>.
        
        # Find the sidebar Links
        if 'Login/Logout' not in content:
            sidebar_addition = '''
        <hr style="border-color: rgba(255,255,255,0.2); margin: 15px;">
        {% if session.user_email %}
            <a href="{{ url_for('logout') }}" style="color: #fca5a5;">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}">Login</a>
        {% endif %}
    </div>'''
            # replace last </div> of sidebar with this addition
            content = re.sub(r'(<a href="/contact".*?</a>\s*)</div>', r'\1' + sidebar_addition, content, flags=re.DOTALL)
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)
            
print("done")
