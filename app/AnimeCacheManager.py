import os
import requests
import shutil

class CacheManagerBase:

    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    def init(self):
        if not os.path.isdir(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_cache_root(self):
        return self.cache_dir

class AnimeCacheManager(CacheManagerBase):

    def __init__(self, cache_dir):
        super().__init__(cache_dir)

    # todo async this
    def download_cover(self, image_url, filename):
        r = requests.get(image_url, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True 
            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    def create_directory(self, name):
        d = os.path.join(self.cache_dir, name)
        if not os.path.isdir(d):
            os.makedirs(d)

    def get_anime_cover(self, anime_id, cover_url):
        cache_path = self.get_anime_cover_path(anime_id)

        if not os.path.isfile(cache_path):
            self.download_cover(cover_url, cache_path)

        return cache_path

    def get_anime_cover_path(self, anime_id):
        return os.path.join(self.get_cache_dir(str(anime_id)), "cover.png")

    def get_cache_dir(self, anime_id):
        return os.path.join(self.get_cache_root(), str(anime_id))