import os

files = ['index.html', 'crop.html', 'disease.html', 'weather.html', 'voice_sms.html']

script_to_inject = """
<script>
    document.addEventListener("DOMContentLoaded", () => {
        const navItems = {
            "dashboard": "/index.html",
            "potted_plant": "/crop.html",
            "biotech": "/disease.html",
            "wb_sunny": "/weather.html",
            "forum": "/voice_sms.html"
        };
        
        document.querySelectorAll("nav span.material-symbols-outlined, aside span.material-symbols-outlined, .md\\\\:hidden span.material-symbols-outlined").forEach(span => {
            const iconName = span.innerText.trim();
            if (navItems[iconName]) {
                const parent = span.parentElement;
                parent.style.cursor = "pointer";
                parent.addEventListener("click", (e) => {
                    e.preventDefault();
                    window.location.href = navItems[iconName];
                });
            }
        });
    });
</script>
</body>
"""

for filename in files:
    filepath = os.path.join('frontend', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('</body>', script_to_inject)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
