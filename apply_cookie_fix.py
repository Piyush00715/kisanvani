import os

fix_cookie_script = """
<script>
document.addEventListener("DOMContentLoaded", () => {
    const lang = localStorage.getItem("kisanvani_lang");
    if (lang && lang !== "en") {
        const expectedCookie = "googtrans=/en/" + lang;
        if (!document.cookie.includes(expectedCookie)) {
            document.cookie = expectedCookie + "; path=/";
            window.location.reload(); // Reload once to apply translation
        }
    }
});
</script>
"""

files = ['index.html', 'crop.html', 'disease.html', 'weather.html', 'voice_sms.html']
for filename in files:
    filepath = os.path.join('frontend', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'window.location.reload();' not in content:
        content = content.replace('</body>', fix_cookie_script + '\n</body>')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Cookie fix applied.")
