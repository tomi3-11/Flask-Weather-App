# Main Flask Logic for The Weather App
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

# Loading the environmental variables
load_dotenv()

app = Flask(__name__)

# Getting our API_KEY.
API_KEY = os.getenv("API_KEY")

# Defining Routes
@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None
    
    if request.method == "POST":
        city = request.form.get('city', '').strip()
        
        
        if city:
            url =  f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                weather_data = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].title()
                }
                
        else:
            error = data.get("message", "City Not Found. Please Try Again.")
            
    # Render Our templates
    return render_template('index.html', error=error, weather=weather_data)


# Run our Application
# if __name__ == "__main__":
#     app.run(debug=True)
            
            
