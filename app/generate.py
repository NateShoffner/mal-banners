# -*- coding: utf-8 -*-

import argparse
from jikanpy import Jikan
from PIL import ImageFont
from AnimeCacheManager import AnimeCacheManager
from UserAssetsManager import UserAssetsManager
from SeasonalChartGenerator import Generator

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username of MyAnimeList user to fetch data from")
    parser.add_argument("output_dir", help="Output directory for the renders")
    parser.add_argument("--watching_color", help="Fill color of the watching progress bar", default="#2DB039")

    args = parser.parse_args()
    username = args.username
    output_dir = args.output_dir
    watching_color = args.watching_color

    jikan = Jikan()

    anime_cache_manager = AnimeCacheManager('../cache')
    anime_cache_manager.init()

    user_asset_manager = UserAssetsManager(output_dir)
    user_asset_manager.init()

    title_font = ImageFont.truetype('../assets/fonts/arial-unicode-ms.ttf', 12)
    text_font = ImageFont.truetype('../assets/fonts/verdana.ttf', 11)

    generator = Generator(jikan, anime_cache_manager, user_asset_manager, title_font, text_font)
    generator.generate(username, 'seasonal_chart.png', watching_color)