import os
import re

FRONTEND_DIR = 'frontend'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the old script that redirects menu to dashboard
    old_script_pattern = re.compile(
        r'const menuBtn = document\.querySelector\([^)]+\);\s*'
        r'if\s*\(menuBtn\s*&&\s*menuBtn\.innerText\.includes\(\'menu\'\)\)\s*\{\s*'
        r'menuBtn\.parentElement\.addEventListener\(\'click\',\s*\(\)\s*=>\s*\{\s*'
        r'// For mobile, just go to dashboard if menu clicked\s*'
        r'window\.location\.href\s*=\s*\'/index\.html\';\s*'
        r'\}\);\s*'
        r'\}',
        re.DOTALL
    )
    
    if old_script_pattern.search(content):
        content = old_script_pattern.sub('', content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed old menu click in {filepath}")

for filename in os.listdir(FRONTEND_DIR):
    if filename.endswith('.html'):
        process_file(os.path.join(FRONTEND_DIR, filename))
