import os
import re

FRONTEND_DIR = 'frontend'

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove literal '\n' right before the injected drawer
    content = content.replace('\\n\n<!-- Mobile Sliding Drawer -->', '\n<!-- Mobile Sliding Drawer -->')
    content = content.replace('\\n\n<script>\ndocument.addEventListener("DOMContentLoaded", () => {\n    const mobileDrawer', '\n<script>\ndocument.addEventListener("DOMContentLoaded", () => {\n    const mobileDrawer')

    # 2. Fix Javascript for drawer to find button instead of just span
    old_js = """
    // Find menu button (the one with 'menu' text inside a material-symbols-outlined span)
    const menuSpans = Array.from(document.querySelectorAll('header span.material-symbols-outlined'));
    const menuIcon = menuSpans.find(span => span.innerText.trim() === 'menu');
    
    if (menuIcon && mobileDrawer && mobileDrawerOverlay) {
        const menuBtn = menuIcon.parentElement;
"""
    new_js = """
    // Find menu button
    const menuIcons = Array.from(document.querySelectorAll('header .material-symbols-outlined'));
    const menuIcon = menuIcons.find(el => el.innerText.trim() === 'menu');
    
    if (menuIcon && mobileDrawer && mobileDrawerOverlay) {
        const menuBtn = menuIcon.tagName === 'BUTTON' ? menuIcon : menuIcon.parentElement;
"""
    content = content.replace(old_js, new_js)

    # 3. Remove bottom navbar
    # Search for bottom navbar block
    # It usually starts with <nav class="md:hidden fixed bottom-0" or similar
    nav_pattern = re.compile(r'<!-- BottomNavBar \(Mobile only\) -->\s*<nav[^>]*bottom-0[^>]*>.*?</nav>\s*', re.DOTALL)
    content = nav_pattern.sub('', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Processed {filepath}")

for filename in os.listdir(FRONTEND_DIR):
    if filename.endswith('.html'):
        process_html_file(os.path.join(FRONTEND_DIR, filename))

# 4. Remove Maize badge from disease.html
disease_file = os.path.join(FRONTEND_DIR, 'disease.html')
with open(disease_file, 'r', encoding='utf-8') as f:
    disease_content = f.read()

badge_pattern = re.compile(r'<!-- Recent History \(Asymmetric Accent\) -->\s*<div class="flex flex-wrap gap-4 pt-4">\s*<div class="flex items-center gap-2 px-4 py-2 bg-surface-container rounded-full border border-outline-variant/20">\s*<span class="material-symbols-outlined text-sm">history</span>\s*<span class="text-label-sm font-label-sm">Recent: Maize Rust \(98% match\)</span>\s*</div>\s*</div>\s*', re.DOTALL)
disease_content = badge_pattern.sub('', disease_content)

with open(disease_file, 'w', encoding='utf-8') as f:
    f.write(disease_content)
    
print("Processed Maize badge in disease.html")
