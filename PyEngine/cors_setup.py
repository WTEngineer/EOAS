from truckpad.bottle.cors import CorsPlugin
from api import app

# Set CORS
app.install(CorsPlugin(
    origins=['http://localhost:8082', 'http://localhost:8081'],
    headers=['Content-Type', 'Authorization']
))
