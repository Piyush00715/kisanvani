import os
import re

FRONTEND_DIR = 'frontend'

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Regex to match the user icon container and its contents
    # This covers cases with different classes on the div
    pattern = re.compile(r'<div class="w-10 h-10 rounded-full[^>]*>\s*<span class="material-symbols-outlined[^>]*>account_circle</span>\s*</div>', re.DOTALL)
    
    content = pattern.sub('', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for filename in os.listdir(FRONTEND_DIR):
    if filename.endswith('.html'):
        process_html_file(os.path.join(FRONTEND_DIR, filename))
