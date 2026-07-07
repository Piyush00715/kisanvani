import os
import re

WEATHER_FILE = 'frontend/weather.html'

def process_weather_html():
    with open(WEATHER_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update location displays
    content = content.replace('<span id="topLocationDisplay" class="text-label-md font-label-md text-on-surface">Punjab, India</span>', 
                              '<span id="topLocationDisplay" class="text-label-md font-label-md text-on-surface">Locating...</span>')
    content = content.replace('<h2 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface mb-2">Ludhiana, Punjab</h2>', 
                              '<h2 id="mainLocationDisplay" class="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface mb-2">Detecting Location...</h2>')

    # 2. Update temp and condition displays
    content = content.replace('<span class="block font-headline-xl text-[56px] leading-tight text-on-surface">28<span class="text-headline-md align-top">°C</span></span>',
                              '<span class="block font-headline-xl text-[56px] leading-tight text-on-surface"><span id="mainTempDisplay">--</span><span class="text-headline-md align-top">°C</span></span>')
    content = content.replace('<span class="text-label-md font-label-md text-on-surface-variant">Partly Cloudy</span>',
                              '<span id="mainConditionDisplay" class="text-label-md font-label-md text-on-surface-variant">Scanning...</span>')

    # 3. Replace Regional Rain Map with dynamic widget
    old_map_pattern = re.compile(r'<!-- Precipitation Map Placeholder Section -->\s*<section class="mt-gutter-md">.*?</section>', re.DOTALL)
    
    new_widget = """
<!-- Smart Satellite Rain Prediction Widget -->
<section class="mt-8">
    <div class="glass-card rounded-[32px] overflow-hidden shadow-sm relative border-2 border-primary/20">
        <div class="p-6 md:p-8 flex flex-col md:flex-row justify-between items-center gap-6 relative z-10">
            <div class="flex items-center gap-4">
                <div class="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center relative">
                    <div class="absolute inset-0 bg-primary/20 rounded-full animate-ping" id="radarPing"></div>
                    <span class="material-symbols-outlined text-primary text-3xl z-10">satellite_alt</span>
                </div>
                <div>
                    <h3 class="text-on-surface font-headline-md text-2xl font-bold">Smart Rain Prediction</h3>
                    <p class="text-on-surface-variant font-body-md mt-1" id="predictionStatusText">Initializing satellite scan...</p>
                </div>
            </div>
            
            <div id="rainResultBadge" class="hidden px-6 py-3 bg-surface-container rounded-2xl flex items-center gap-3">
                <span class="material-symbols-outlined text-primary" id="rainResultIcon">rainy</span>
                <span class="text-label-lg font-bold text-on-surface" id="rainResultText">Checking...</span>
            </div>
        </div>
    </div>
</section>

<!-- Weather Script -->
<script>
    async function predictRain() {
        const topLocation = document.getElementById('topLocationDisplay');
        const mainLocation = document.getElementById('mainLocationDisplay');
        const mainTemp = document.getElementById('mainTempDisplay');
        const mainCondition = document.getElementById('mainConditionDisplay');
        const statusText = document.getElementById('predictionStatusText');
        const rainBadge = document.getElementById('rainResultBadge');
        const rainIcon = document.getElementById('rainResultIcon');
        const rainText = document.getElementById('rainResultText');
        const radarPing = document.getElementById('radarPing');

        try {
            statusText.innerText = "Connecting to GPS satellites...";
            
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {timeout: 10000});
            });
            
            statusText.innerText = "Analyzing atmospheric data...";
            
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            const token = localStorage.getItem("kisanvani_token") || "";
            const phone_number = token.replace("token_", "");

            const response = await fetch('/api/weather/predict-rain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    lat: lat,
                    lon: lon,
                    phone_number: phone_number
                })
            });

            if (!response.ok) throw new Error("Failed to fetch");

            const data = await response.json();
            
            // Stop radar animation
            radarPing.classList.remove('animate-ping');
            radarPing.classList.add('hidden');
            
            // Update UI
            topLocation.innerText = data.location;
            mainLocation.innerText = data.location;
            mainTemp.innerText = Math.round(data.temp);
            mainCondition.innerText = data.condition;
            
            statusText.innerText = `Live data synced for ${data.location}`;
            
            // Show rain prediction
            rainBadge.classList.remove('hidden');
            if(data.rain_probability > 50) {
                rainBadge.classList.add('bg-error/10', 'text-error');
                rainIcon.innerText = 'thunderstorm';
                rainIcon.classList.replace('text-primary', 'text-error');
                rainText.innerText = data.prediction_msg;
                rainText.classList.add('text-error');
            } else {
                rainBadge.classList.add('bg-primary/10', 'text-primary');
                rainIcon.innerText = 'wb_sunny';
                rainText.innerText = data.prediction_msg;
                rainText.classList.add('text-primary');
            }
            
        } catch(e) {
            statusText.innerText = "Could not fetch satellite data. Please allow location access.";
            radarPing.classList.remove('animate-ping');
            radarPing.classList.add('hidden');
        }
    }

    document.addEventListener("DOMContentLoaded", () => {
        predictRain();
    });
</script>
"""
    content = old_map_pattern.sub(new_widget, content)

    with open(WEATHER_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Updated weather.html")

process_weather_html()
