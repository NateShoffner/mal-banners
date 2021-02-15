from PIL import Image, ImageDraw

class AnimeBanner:

    padding = 5
    cover_thumbnail_width = 40
    cover_thumbnail_height = 60

    def __init__(self, anime, width, height, cover_path, watching_color):
        self.anime = anime
        self.width = width
        self.height = height
        self.cover_path = cover_path
        self.watching_color = watching_color

    def initialize(self):
        self.img = Image.new('RGB', (self.width, self.height), color = 'white')

    def draw(self, title_font, text_font):

        # covers seem to be 225x317, but not sure if enforced
        cover_image = Image.open(self.cover_path)
        cover_image_width, cover_image_height = cover_image.size
        cover_image.thumbnail((self.cover_thumbnail_width, self.cover_thumbnail_height))
        self.img.paste(cover_image, (self.padding, self.padding), cover_image.convert('RGBA'))

        d = ImageDraw.Draw(self.img)
        #title
        title_size = title_font.getsize(self.anime['title'])
        title_pos = ((self.padding * 2) + self.cover_thumbnail_width, self.padding)
        title = d.text(title_pos, self.anime['title'], font=title_font, fill=(0,0,0))        
    
        # progress bar
        bar = ImageDraw.Draw(self.img)
        max_width = 399
        max_height = 10
        watched = self.anime['watched_episodes']
        total = self.anime['total_episodes']
        # just assume 24 episode total is not defined
        width = (watched / 24) * max_width if total == 0 else (watched / total) * max_width

        # progress bar
        progress_pos = ((self.padding * 2) + self.cover_thumbnail_width, title_pos[1] + title_size[1] + (self.padding * 2))
        progress_bounds = (progress_pos[0] + width, 30 + max_height)
        bar.rectangle([progress_pos, progress_bounds], fill=self.watching_color)

        # status
        d = ImageDraw.Draw(self.img)
        status_pos = ((self.padding * 2) + self.cover_thumbnail_width, progress_pos[1] + max_height + (self.padding * 2))
        d.text(status_pos, "Watching %d/%s" % (watched, '?' if total == 0 else str(total)), font=text_font, fill=(120,120,120))
    
    def save(self, filename):
        self.img.save(filename)

    def get_image(self):
        return self.img
