import datetime
import os
import re
from flask import Flask, send_file
from jikanpy import Jikan
from PIL import ImageFont
from .AnimeCacheManager import AnimeCacheManager
from .UserAssetsManager import UserAssetsManager
from .SeasonalChartGenerator import AnimeBanner, SeasonalChart, Generator

app = Flask(__name__)

jikan = Jikan()

cwd = os.getcwd()

anime_cache_manager = AnimeCacheManager(os.path.join(cwd, 'anime_cache'))
anime_cache_manager.init()

user_asset_manager = UserAssetsManager(os.path.join(cwd, 'renders'))
user_asset_manager.init()

title_font = ImageFont.truetype('assets/fonts/arial-unicode-ms.ttf', 12)
text_font = ImageFont.truetype('assets/fonts/verdana.ttf', 11)

generator = Generator(jikan, anime_cache_manager, user_asset_manager, title_font, text_font)

@app.route("/")
def hello():
    return "AYAYA"

@app.route('/seasonal_chart/<username>', methods=['GET'])
@app.route('/seasonal_chart/<username>/<color>', methods=['GET'])
def get_seasonal_chart(username, color='2DB039'):

    filename = "seasonal_chart.png"

    # optional color fill
    hex_color = "#%s" % color
    hex_match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_color)
    if not hex_match:
        hex_color = "#2DB039"

    cache_minutes = 10
    
    path = user_asset_manager.get_asset_path(username, filename)

    # exists but might need regenerated
    if user_asset_manager.user_asset_exists(username, filename):
        age = user_asset_manager.get_file_modification_age(username, filename)
        if (age / 60) >= cache_minutes:
            print("Cache expired: %s [%s]" % (filename, username))
            generator.generate(username, filename, hex_color)
    else: # doesn't exist at all
         print("Cache miss: %s [%s]" % (filename, username))
         p = generator.generate(username, filename, hex_color)

    if not path:
        print("Failed: %s [%s]" % (filename, username))
        abort(404, description="Resource not found")

    else:
        #print("Cache hit: %s [%s]" % (filename, username))
        return send_file(path, mimetype='image/png')

if __name__ == "__main__":
    app.run()
else:
    application = app