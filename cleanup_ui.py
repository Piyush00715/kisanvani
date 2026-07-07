import os
import re

FRONTEND_DIR = 'frontend'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove desktop sidebar
    # Usually matches: <aside class="hidden md:flex fixed left-0 top-0 h-full w-80 ...">...</aside>
    # Note: it could span multiple lines.
    sidebar_pattern = re.compile(r'<!-- NavigationDrawer \(Desktop\) -->\s*<aside class="hidden md:flex[^>]*>.*?</aside>\s*', re.DOTALL)
    content = sidebar_pattern.sub('', content)

    # Sometimes it's just <aside class="hidden md:flex...
    sidebar_pattern2 = re.compile(r'<aside class="hidden md:flex[^>]*>.*?</aside>\s*', re.DOTALL)
    content = sidebar_pattern2.sub('', content)

    # Remove classes that pushed content to the right of the sidebar
    content = content.replace('md:left-80', '')
    content = content.replace('md:pl-80', '')
    content = content.replace('md:px-margin-desktop', 'md:px-8')
    content = content.replace('max-w-container-max', 'max-w-7xl')

    # Remove any extra spaces inside class attributes created by replacements
    content = re.sub(r'class="([^"]*)\s{2,}([^"]*)"', r'class="\1 \2"', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Cleaned up {filepath}")

for filename in os.listdir(FRONTEND_DIR):
    if filename.endswith('.html'):
        process_file(os.path.join(FRONTEND_DIR, filename))
