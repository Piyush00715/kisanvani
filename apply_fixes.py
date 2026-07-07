import os
import re

# 1. Fix crop.html soil type
crop_file = os.path.join('frontend', 'crop.html')
with open(crop_file, 'r', encoding='utf-8') as f:
    crop_content = f.read()

# Replace Black with Clayey in span and in the text
crop_content = crop_content.replace('<span class="font-label-md text-label-md">Black</span>', '<span class="font-label-md text-label-md">Clayey</span>')
crop_content = crop_content.replace('Black Soil', 'Clayey Soil')
with open(crop_file, 'w', encoding='utf-8') as f:
    f.write(crop_content)

# 2. Fix navigation (Header & logo links to dashboard)
# We will inject a script into all files to handle the header click
header_nav_script = """
<script>
document.addEventListener("DOMContentLoaded", () => {
    const headerTitle = document.querySelector('h1.text-primary, h1.text-headline-md');
    if (headerTitle) {
        headerTitle.style.cursor = 'pointer';
        headerTitle.addEventListener('click', () => { window.location.href = '/index.html'; });
    }
    const menuBtn = document.querySelector('header button span.material-symbols-outlined');
    if (menuBtn && menuBtn.innerText.includes('menu')) {
        menuBtn.parentElement.addEventListener('click', () => {
            // For mobile, just go to dashboard if menu clicked
            window.location.href = '/index.html';
        });
    }
});
</script>
"""

files = ['index.html', 'crop.html', 'disease.html', 'weather.html', 'voice_sms.html', 'login.html']
for filename in files:
    filepath = os.path.join('frontend', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'headerTitle.style.cursor' not in content:
        content = content.replace('</body>', header_nav_script + '\n</body>')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 3. Fix Google Translate Cookie in login.html
login_file = os.path.join('frontend', 'login.html')
with open(login_file, 'r', encoding='utf-8') as f:
    login_content = f.read()

# Set cookie when login is successful
login_content = login_content.replace(
    'localStorage.setItem("kisanvani_lang", data.preferred_language);',
    'localStorage.setItem("kisanvani_lang", data.preferred_language);\ndocument.cookie = "googtrans=/en/" + data.preferred_language + "; path=/";'
)
with open(login_file, 'w', encoding='utf-8') as f:
    f.write(login_content)

print("Fixes applied successfully.")
