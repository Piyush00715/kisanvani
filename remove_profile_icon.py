import os
import re

FRONTEND_DIR = 'frontend'

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove the profile icon container block
    # It starts with `<div class="[w-10 h-10|h-10 w-10] rounded-full` and ends with `</div>` after the `account_circle` span
    pattern = re.compile(r'<div class="(?:w-10 h-10|h-10 w-10) rounded-full[^>]*>\s*<span class="material-symbols-outlined[^>]*>account_circle</span>\s*</div>', re.DOTALL)
    content = pattern.sub('', content)

    # Fix the accidental previewContainer replacement in disease.html
    if 'disease.html' in filepath:
        bad_preview = '<span class="material-symbols-outlined text-primary !text-3xl">account_circle</span>\n<div class="hidden absolute top-0 left-0 w-full scan-line" id="scanningLine"></div>'
        good_preview = '<img id="previewImage" class="w-full h-full object-cover" src="" alt="Preview">\n<div class="hidden absolute top-0 left-0 w-full scan-line" id="scanningLine"></div>'
        content = content.replace(bad_preview, good_preview)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for filename in os.listdir(FRONTEND_DIR):
    if filename.endswith('.html'):
        process_html_file(os.path.join(FRONTEND_DIR, filename))
