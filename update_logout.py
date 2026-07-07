import os
import re

FRONTEND_DIR = 'frontend'

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Replace the profile image with a material icon
    # There are multiple image URLs and alt texts used across files, so regex is best here.
    img_pattern = re.compile(r'<img[^>]+src="https://lh3\.googleusercontent\.com/[^"]+"[^>]*>')
    replacement_icon = '<span class="material-symbols-outlined text-primary !text-3xl">account_circle</span>'
    content = img_pattern.sub(replacement_icon, content)
    
    # Remove cursor-pointer and title="Logout" from the profile parent div if present
    content = content.replace('title="Logout"', '')
    
    # Remove older profile click scripts
    script_pattern1 = re.compile(r'// Profile click to logout\s+const profileImgs[^}]+}\);', re.DOTALL)
    content = script_pattern1.sub('', content)
    
    script_pattern2 = re.compile(r'// Profile Logout\s+const profileBtn[^}]+}\);(\s+}\);)?', re.DOTALL)
    content = script_pattern2.sub('', content)
    
    # 2. Add logout button to drawer
    logout_html = '''
        <div class="mt-6">
            <button onclick="logoutUser()" class="flex items-center justify-center gap-3 px-4 py-3 rounded-xl bg-primary text-white hover:opacity-90 transition-all w-full shadow-md active:scale-95">
                <span class="material-symbols-outlined">logout</span>
                <span class="font-label-md font-bold">Logout</span>
            </button>
        </div>
    </nav>'''
    
    # Only add if not already added
    if 'onclick="logoutUser()"' not in content:
        content = content.replace('</nav>', logout_html, 1)
        
    # 3. Add the logoutUser function
    js_func = '''
<script>
function logoutUser() {
    localStorage.removeItem("kisanvani_token");
    window.location.href = "/login.html";
}
</script>
</body>'''
    if 'function logoutUser()' not in content:
        content = content.replace('</body>', js_func, 1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for filename in os.listdir(FRONTEND_DIR):
    if filename.endswith('.html') and filename != 'login.html':
        process_html_file(os.path.join(FRONTEND_DIR, filename))
