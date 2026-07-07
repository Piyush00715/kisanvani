import os

files = ['index.html', 'crop.html', 'disease.html', 'weather.html', 'voice_sms.html']

auth_check = """
    <script>
        if (!localStorage.getItem('kisanvani_token')) {
            window.location.href = '/login.html';
        }
    </script>
</head>
"""

lang_logout_scripts = """
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: 'en,hi,pa,mr,gu,kn,ta,ml,te',
      layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
      autoDisplay: false
  }, 'google_translate_element');
}
</script>
<script type="text/javascript" src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>

<script>
document.addEventListener("DOMContentLoaded", () => {
    // Hidden div for the widget
    const translateDiv = document.createElement('div');
    translateDiv.id = 'google_translate_element';
    translateDiv.style.display = 'none';
    document.body.appendChild(translateDiv);

    // Profile click to logout
    const profileImgs = document.querySelectorAll('.w-10.h-10.rounded-full');
    profileImgs.forEach(img => {
        img.style.cursor = 'pointer';
        img.title = 'Logout';
        img.addEventListener('click', () => {
            if(confirm("Are you sure you want to logout?")) {
                localStorage.removeItem("kisanvani_token");
                localStorage.removeItem("kisanvani_lang");
                // Clear cookies for google translate
                document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
                window.location.href = "/login.html";
            }
        });
    });

    // Auto translate based on state pref
    const lang = localStorage.getItem("kisanvani_lang");
    if (lang && lang !== "en") {
        const translateInterval = setInterval(() => {
            const selectField = document.querySelector(".goog-te-combo");
            if (selectField) {
                selectField.value = lang;
                selectField.dispatchEvent(new Event("change"));
                clearInterval(translateInterval);
            }
        }, 300); 
    }
});
</script>
</body>
"""

for filename in files:
    filepath = os.path.join('frontend', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Avoid double injection
    if 'kisanvani_token' not in content:
        content = content.replace('</head>', auth_check)
        content = content.replace('</body>', lang_logout_scripts)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f"Skipping {filename}, already injected.")

print("Done injecting auth and lang scripts.")
