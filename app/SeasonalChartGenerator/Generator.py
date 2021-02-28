from PIL import ImageFont
from . import AnimeBanner
from . import SeasonalChart
import math 
import os

class Generator:

    def __init__(self, jikan, anime_cache, user_asset_manager, title_font, text_font):
        self.jikan = jikan
        self.anime_cache = anime_cache
        self.user_asset_manager = user_asset_manager
        self.title_font = title_font
        self.text_font = text_font

    def get_seasonal_watching(self, user):
        watching = self.jikan.user(username=user, request='animelist', argument='watching')

        #todo cache this
        seasonal = self.jikan.season()

        user_seasonal = []

        for anime in watching['anime']:
            if any(x['mal_id'] == anime['mal_id'] for x in seasonal['anime']):
                user_seasonal.append(anime)
        return user_seasonal

    def generate(self, username, filename, watching_fill_color = '#2DB039'):
        print("Fetching seasonal: %s" % username)
        seasonal = self.get_seasonal_watching(username)
        print("Fetched seasonal: %s" % username)

        banners = []

        banner_width = 399
        banner_height = 86

        for anime in seasonal:
            # create respective anime directories
            self.anime_cache.create_directory(str(anime['mal_id']))

            # download cover art
            cover_path = self.anime_cache.get_anime_cover(anime['mal_id'], anime['image_url'])

            banner = AnimeBanner(anime, banner_width, banner_height, cover_path, watching_fill_color)
            banner.initialize()
            banner.draw(self.title_font, self.text_font)
            banners.append(banner)

        chart = SeasonalChart(banner_width * 2, max(banner_height, (int(math.ceil(len(banners) / 2))) * banner_height))
        chart.draw(banners, self.text_font)
        self.user_asset_manager.create_user_dir(username)
        save_path = self.user_asset_manager.get_asset_path(username, filename)
        chart.save(save_path)
        return save_path