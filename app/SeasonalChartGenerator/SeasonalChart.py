from PIL import Image, ImageDraw
import datetime

class SeasonalChart:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.img = Image.new('RGB', (width, height), color = 'white')

    def draw(self, banners, footer_font):
        even_count = 0
        odd_count = 0

        for indexer, banner in enumerate(banners):
            banner_img = banner.get_image()

            banner_width = banner_img.size[0]
            banner_height = banner_img.size[1]

            if (indexer % 2) == 0: # first column
                odd_count += 1
                if indexer == 0:
                    coord = (0, 0)
                else: 
                    coord = (0, banner_height * (odd_count - 1))
            else: # second column
                even_count += 1
                coord = (banner_width, banner_height * (even_count - 1))
            self.img.paste(banner_img, coord, banner_img.convert('RGBA'))

        # footer
        now = datetime.datetime.now()
        updated = now.strftime("%c")
        footer_str = 'Seasonal Chart Generator by Syntack. Last Updated: ' + updated
        footer_size = footer_font.getsize(footer_str)
        footer_pos = (self.width - footer_size[0], self.height - footer_size[1])
        d = ImageDraw.Draw(self.img)
        d.text(footer_pos, footer_str, font=footer_font, fill=(120,120,120))    

    def save(self, filename):
        self.img.save(filename)