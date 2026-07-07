import os
import re

files = ['index.html', 'crop.html', 'disease.html', 'weather.html', 'voice_sms.html', 'login.html']

for filename in files:
    filepath = os.path.join('frontend', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove google translate widget initialization
    content = re.sub(r'<script type="text/javascript">\s*function googleTranslateElementInit\(\) \{.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script type="text/javascript" src="https://translate\.google\.com/translate_a/element\.js\?cb=googleTranslateElementInit"></script>', '', content)
    
    # Remove the google_translate_element div creation in the script
    content = re.sub(r'// Hidden div for the widget\s*const translateDiv = document\.createElement\(\'div\'\);\s*translateDiv\.id = \'google_translate_element\';\s*translateDiv\.style\.display = \'none\';\s*document\.body\.appendChild\(translateDiv\);', '', content, flags=re.DOTALL)

    # Remove the auto translate trigger interval
    content = re.sub(r'// Auto translate based on state pref\s*const lang = localStorage\.getItem\("kisanvani_lang"\);\s*if \(lang && lang !== "en"\) \{.*?\n    }', '', content, flags=re.DOTALL)

    # Remove cookie fix script
    content = re.sub(r'<script>\s*document\.addEventListener\("DOMContentLoaded", \(\) => \{\s*const lang = localStorage\.getItem\("kisanvani_lang"\);\s*if \(lang && lang !== "en"\) \{.*?</script>', '', content, flags=re.DOTALL)
    
    # Remove document.cookie setting from login.html
    content = re.sub(r'document\.cookie = "googtrans=\/en\/" \+ data\.preferred_language \+ "; path=\/";', '', content)
    
    # Remove cookie clearing from logout
    content = re.sub(r'// Clear cookies for google translate\s*document\.cookie\.split\(";"\)\.forEach\(.*?window\.location\.href', 'window.location.href', content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Google Translate removed.")
