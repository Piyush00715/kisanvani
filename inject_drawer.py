import os
import re

FRONTEND_DIR = 'frontend'

drawer_html = """
<!-- Mobile Sliding Drawer -->
<div id="mobileDrawerOverlay" class="fixed inset-0 bg-black/50 z-[90] hidden opacity-0 transition-opacity duration-300"></div>
<aside id="mobileDrawer" class="fixed top-0 left-0 h-full w-72 bg-surface z-[100] transform -translate-x-full transition-transform duration-300 flex flex-col shadow-2xl">
    <div class="p-6 border-b border-outline-variant/30 flex justify-between items-center bg-surface-container-low">
        <div>
            <h2 class="font-headline-sm text-2xl font-bold text-primary">KisanVani</h2>
            <p class="text-sm text-on-surface-variant mt-1 font-medium">Premium Agri-SaaS</p>
        </div>
        <button id="closeDrawerBtn" class="text-on-surface-variant hover:text-primary transition-colors p-2 rounded-full hover:bg-surface-container">
            <span class="material-symbols-outlined text-2xl">close</span>
        </button>
    </div>
    <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-2 font-body-md text-on-surface-variant">
        <a href="/index.html" class="flex items-center gap-4 px-4 py-3 rounded-xl hover:bg-primary-container/30 hover:text-primary transition-colors {DASH_ACTIVE}">
            <span class="material-symbols-outlined">dashboard</span>
            <span class="font-label-md font-bold">Dashboard</span>
        </a>
        <a href="/crop.html" class="flex items-center gap-4 px-4 py-3 rounded-xl hover:bg-primary-container/30 hover:text-primary transition-colors {CROP_ACTIVE}">
            <span class="material-symbols-outlined">potted_plant</span>
            <span class="font-label-md font-bold">Crop Recommendation</span>
        </a>
        <a href="/disease.html" class="flex items-center gap-4 px-4 py-3 rounded-xl hover:bg-primary-container/30 hover:text-primary transition-colors {DIS_ACTIVE}">
            <span class="material-symbols-outlined">biotech</span>
            <span class="font-label-md font-bold">Disease Detection</span>
        </a>
        <a href="/weather.html" class="flex items-center gap-4 px-4 py-3 rounded-xl hover:bg-primary-container/30 hover:text-primary transition-colors {WEA_ACTIVE}">
            <span class="material-symbols-outlined">wb_sunny</span>
            <span class="font-label-md font-bold">Weather Advisory</span>
        </a>
        <a href="/voice_sms.html" class="flex items-center gap-4 px-4 py-3 rounded-xl hover:bg-primary-container/30 hover:text-primary transition-colors {COM_ACTIVE}">
            <span class="material-symbols-outlined">forum</span>
            <span class="font-label-md font-bold">Communication</span>
        </a>
    </nav>
</aside>
"""

drawer_script = """
<script>
document.addEventListener("DOMContentLoaded", () => {
    const mobileDrawer = document.getElementById('mobileDrawer');
    const mobileDrawerOverlay = document.getElementById('mobileDrawerOverlay');
    const closeDrawerBtn = document.getElementById('closeDrawerBtn');
    
    // Find menu button (the one with 'menu' text inside a material-symbols-outlined span)
    const menuSpans = Array.from(document.querySelectorAll('header span.material-symbols-outlined'));
    const menuIcon = menuSpans.find(span => span.innerText.trim() === 'menu');
    
    if (menuIcon && mobileDrawer && mobileDrawerOverlay) {
        const menuBtn = menuIcon.parentElement;
        
        // Remove old event listeners if any by cloning
        const newMenuBtn = menuBtn.cloneNode(true);
        menuBtn.parentNode.replaceChild(newMenuBtn, menuBtn);
        
        newMenuBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            mobileDrawerOverlay.classList.remove('hidden');
            // small delay for display block to take effect before opacity transition
            setTimeout(() => {
                mobileDrawerOverlay.classList.remove('opacity-0');
                mobileDrawer.classList.remove('-translate-x-full');
            }, 10);
        });
    }

    function closeDrawer() {
        if(mobileDrawer && mobileDrawerOverlay) {
            mobileDrawer.classList.add('-translate-x-full');
            mobileDrawerOverlay.classList.add('opacity-0');
            setTimeout(() => {
                mobileDrawerOverlay.classList.add('hidden');
            }, 300);
        }
    }

    if(closeDrawerBtn) closeDrawerBtn.addEventListener('click', closeDrawer);
    if(mobileDrawerOverlay) mobileDrawerOverlay.addEventListener('click', closeDrawer);
});
</script>
"""

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'id="mobileDrawer"' in content:
        print(f"Skipping {filepath}, drawer already exists.")
        return

    # Determine active states
    dash_act = "bg-primary-container text-on-primary-container" if "index.html" in filepath else ""
    crop_act = "bg-primary-container text-on-primary-container" if "crop.html" in filepath else ""
    dis_act = "bg-primary-container text-on-primary-container" if "disease.html" in filepath else ""
    wea_act = "bg-primary-container text-on-primary-container" if "weather.html" in filepath else ""
    com_act = "bg-primary-container text-on-primary-container" if "voice_sms.html" in filepath else ""
    
    inject_html = drawer_html.replace("{DASH_ACTIVE}", dash_act)\
                             .replace("{CROP_ACTIVE}", crop_act)\
                             .replace("{DIS_ACTIVE}", dis_act)\
                             .replace("{WEA_ACTIVE}", wea_act)\
                             .replace("{COM_ACTIVE}", com_act)

    # Inject HTML right after <body ...>
    body_match = re.search(r'<body[^>]*>', content)
    if not body_match:
        print(f"Skipping {filepath}, no body tag found.")
        return
        
    insert_pos = body_match.end()
    content = content[:insert_pos] + '\\n' + inject_html + content[insert_pos:]
    
    # Inject Script right before </body>
    body_end = content.rfind('</body>')
    if body_end != -1:
        content = content[:body_end] + '\\n' + drawer_script + '\\n' + content[body_end:]
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Injected drawer into {filepath}")

for filename in os.listdir(FRONTEND_DIR):
    if filename.endswith('.html'):
        process_html_file(os.path.join(FRONTEND_DIR, filename))
