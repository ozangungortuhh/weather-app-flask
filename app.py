import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

# Create db
db = SQLAlchemy(app)
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Front page
@app.route('/', methods = ['GET', 'POST'])
def index():
    cities = City.query.all()
    
    # New city request
    if request.method == 'POST':
            new_city = request.form.get('city')
            new_city_obj = City(name=new_city)
            city_names = [city.name for city in cities]
            if new_city not in city_names:
                db.session.add(new_city_obj) 
                db.session.commit()   
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=932ad200713d0d59dcafdea4a1efa141'
    
    weather_data = list()

    for city in cities:
        r = requests.get(url.format(city.name)).json()
        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)