import os
import time

class UserAssetsManager:

    def __init__(self, asset_dir):
        self.asset_dir = asset_dir

    def init(self):
        if not os.path.isdir(self.asset_dir ):
            os.makedirs(self.asset_dir)

    def get_user_dir(self, username):
        return os.path.join(self.asset_dir, username)

    def user_dir_exists(self, username):
        return os.path.isdir(self.get_user_dir(username))

    def create_user_dir(self, username):
        d = self.get_user_dir(username)
        if not os.path.isdir(d):
            os.makedirs(d)

    def get_asset_path(self, username, filename):
        return os.path.join(self.get_user_dir(username), filename)

    def user_asset_exists(self, username, filename):
        return os.path.isfile(self.get_asset_path(username, filename))

    def get_file_modification_age(self, username, filename):
        modified = os.path.getmtime(self.get_asset_path(username, filename))
        return time.time() - modified


