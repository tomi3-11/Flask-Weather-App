# Main Flask Logic for The Weather App
from flask import Flask, render_template, request, redirect, url_for
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
    
    if request.method == "POST":
        city = request.form.get('city', '').strip()
        
        return redirect(url_for('details', city=city))
        
    return render_template('index.html')


@app.route('/details/<city>')
def details(city):
    weather_data = None
    error = None
    
    if city:
        url =  f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
            
        if response.status_code == 200:
            weather_data = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].title(),
                "wind_speed": data["wind"]["speed"],
                "visibility": data["visibility"],
                "pressure": data["main"]["pressure"],
                "timezone": data["timezone"]
                
            }
                
        else:
            error = data.get("message", "City Not Found. Please Try Again.")
    
    return render_template('details.html', weather=weather_data, error=error)


@app.route('/detailed-information/<city>/full')
def detailed_information(city):
    weather_data = None
    error = None
    
    if city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "sun_rise": data["sys"]["sunrise"],
                "sun_set": data["sys"]["sunset"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"]["deg"],
                "wind_gust": data["wind"]["gust"],
                "tem_min": data["main"]["temp_min"],
                "tem_max": data["main"]["temp_max"]
            }
        else:
            error = data.get("Message", "City Not Found!")
    
    return render_template('detailed-information.html', weather=weather_data, error=error)

# Run our Application
if __name__ == "__main__":
    app.run(debug=True)
            
            
