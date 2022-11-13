import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

API_KEY = '932ad200713d0d59dcafdea4a1efa141'

@app.route('/')
def index():
    city = 'Hamburg'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
    
    r = requests.get(url.format(city)).json()
    print(r)

    weather = {
        'city' : city,
        'temperature' : r['main']['temp'] ,
        'description' : r['weather'][0]['description'] ,
        'icon' : r[weather][0]['icon'],
    }
    return render_template('weather.html')