import os

css_path = r"c:\Users\KRISSHORE S\OneDrive\Desktop\MyWebsite\static\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    content = f.read()

# We can replace chunks
chunk1_start = content.find("/* ===== Sidebar ===== */")
chunk1_end = content.find("/* ===== Main Content ===== */")

if chunk1_start != -1 and chunk1_end != -1:
    content = content[:chunk1_start] + "/* (Legacy Sidebar Styles Removed) */\n\n" + content[chunk1_end:]

chunk2_start = content.find("/* ===== Menu Toggle Button ===== */")
chunk2_end = content.find("body {", chunk2_start)

# In case there are multiple body tags, find the one near line 363. 
# Better: just use the last occurrence of /* ===== Content Adjustment ===== */ and then to body {
new_styles = """/* ===== Sidebar Modern Neon Style ===== */
.sidebar {
    position: fixed;
    width: 250px;
    height: 100%;
    background: linear-gradient(180deg, rgba(15,32,39,0.95), rgba(32,58,67,0.95), rgba(44,83,100,0.95));
    backdrop-filter: blur(15px);
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    left: 0;
    top: 0;
    box-shadow: 2px 0 20px rgba(0, 247, 255, 0.2);
    display: flex;
    flex-direction: column;
    z-index: 999;
}

/* Sidebar Closed Mode */
.sidebar.closed {
    transform: translateX(-100%);
}

.sidebar-header {
    text-align: center;
    padding: 30px 20px 10px;
}

.sidebar-logo {
    width: 80px;
    height: auto;
    filter: drop-shadow(0 0 10px #00f7ff);
    margin-bottom: 15px;
}

.sidebar h2 {
    color: #00f7ff;
    text-shadow: 0 0 10px #00f7ff;
    letter-spacing: 2px;
    font-size: 22px;
    margin: 0;
}

.sidebar-links {
    display: flex;
    flex-direction: column;
    padding: 20px 0;
    flex-grow: 1;
}

.sidebar a {
    display: flex;
    align-items: center;
    padding: 15px 25px;
    color: white;
    text-decoration: none;
    transition: 0.3s;
    border-left: 4px solid transparent;
}

/* Icon Style */
.sidebar .icon {
    font-size: 22px;
    width: 35px;
    text-align: center;
}

/* Text Style */
.sidebar .text {
    font-size: 16px;
    transition: 0.3s;
    letter-spacing: 1px;
}

/* Hover Neon Glow */
.sidebar a:hover {
    background: rgba(0, 247, 255, 0.1);
    border-left: 4px solid #00f7ff;
    box-shadow: inset 15px 0 20px -15px rgba(0, 247, 255, 0.5);
    color: #00f7ff;
}

.sidebar a:hover .text {
    text-shadow: 0 0 8px #00f7ff;
}

.sidebar-footer {
    padding-bottom: 30px;
}

.logout-link .icon, .logout-link .text {
    color: #fca5a5;
    text-shadow: 0 0 5px #fca5a5;
}

.login-link .icon, .login-link .text {
    color: #86efac;
    text-shadow: 0 0 5px #86efac;
}

.sidebar a.logout-link:hover {
    background: rgba(252, 165, 165, 0.1);
    border-left-color: #fca5a5;
    box-shadow: inset 15px 0 20px -15px rgba(252, 165, 165, 0.5);
    color: #fca5a5;
}

.sidebar a.login-link:hover {
    background: rgba(134, 239, 172, 0.1);
    border-left-color: #86efac;
    box-shadow: inset 15px 0 20px -15px rgba(134, 239, 172, 0.5);
    color: #86efac;
}

/* ===== Menu Toggle Button ===== */
.menu-toggle {
    position: fixed;
    top: 20px;
    left: 20px;
    font-size: 22px;
    cursor: pointer;
    z-index: 1000;
    background: rgba(0, 0, 0, 0.6);
    color: #00f7ff;
    width: 45px;
    height: 45px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 247, 255, 0.3);
    border: 1px solid rgba(0, 247, 255, 0.5);
    transition: 0.3s;
}

.menu-toggle:hover {
    background: #00f7ff;
    color: black;
    box-shadow: 0 0 20px #00f7ff;
    transform: scale(1.05);
}

/* ===== Content Adjustment ===== */
.content {
    margin-left: 250px;
    padding: 30px;
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Content Full Width When Sidebar Closed */
.content.full {
    margin-left: 0;
}

"""

if chunk2_start != -1:
    body_idx = content.find("body {", chunk2_start)
    if body_idx != -1:
        content = content[:chunk2_start] + new_styles + content[body_idx:]

with open(css_path, "w", encoding="utf-8") as f:
    f.write(content)

print("CSS updated!")
