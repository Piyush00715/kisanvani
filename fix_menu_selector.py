import os

FRONTEND_DIR = 'frontend'

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the selector for the menu button so it works on both <header> and <nav>
    old_selector = "document.querySelectorAll('header .material-symbols-outlined')"
    new_selector = "document.querySelectorAll('header .material-symbols-outlined, nav .material-symbols-outlined')"
    
    if old_selector in content:
        content = content.replace(old_selector, new_selector)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")

for filename in os.listdir(FRONTEND_DIR):
    if filename.endswith('.html'):
        process_html_file(os.path.join(FRONTEND_DIR, filename))
