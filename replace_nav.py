import os
import re

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    original = content
    
    # Replace in nav bar links
    content = content.replace('voice_sms.html', 'news.html')
    content = content.replace('Communication', 'Agri-News & Schemes')
    content = content.replace('>forum<', '>newspaper<')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

def main():
    frontend_dir = 'frontend'
    for filename in os.listdir(frontend_dir):
        if filename.endswith('.html'):
            process_html_file(os.path.join(frontend_dir, filename))
            
    # Update main.py
    main_path = 'app/main.py'
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace('from app.routers import voice_sms', 'from app.routers import news')
    content = content.replace('app.include_router(voice_sms.router, prefix="/api/voice-sms", tags=["Voice & SMS"])', 'app.include_router(news.router, prefix="/api/news", tags=["Agri-News"])')
    
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated main.py")

if __name__ == '__main__':
    main()
