from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from requests import get

from os import getcwd

from aiohttp import request

class ImageGenerator:
    
    def __init__(self):
        '''
        Initializes Image Generator
        '''
        self.font = ImageFont.truetype(getcwd()+'/assets/misc/font.otf', 25)
        self.base_width = 256
        self.base_height = 256
    
    def calculate_image_wh(self, images_list : list, vertical: bool = False):
        '''
        calculate image width and height according to images provided
        '''
        w,h = 0,0
        margin_right = 45
        margin_bottom = 55
        for i in range(len(images_list)):
            if vertical:
                h += (self.base_height + margin_bottom)
            else:
                w += (self.base_height + margin_right)
        if w == 0:
            w = self.base_width
        if h == 0:
            h = self.base_height

        return w,h

    def create_blank_image(self, size: tuple):
        '''
        creates a blank image
        '''

        w,h = size
        return Image.new('RGBA', size, color=(0,0,0))



    def image_from_url(self, url: str): 
        '''
        generates a PIL Image object from url
        '''
        if url.startswith('http') and url.split('/')[-1].split('.')[-1] in ['png','jpg', 'jpeg']:
            bytes_ = get(url).content
            return Image.open(BytesIO(bytes_), 'r').convert('RGBA')
    
    def create_image(self, images_list: list, text_list: list, to_save: bool = False, **kwargs):
        '''
        creates a image object
        and saves to filename provided in kwarg if to_save is set to true
        '''

        filename = kwargs.get('filename', 'temp.png')

        #   calculates image height
        #   and width from images_list

        w,h = self.calculate_image_wh(images_list)
        image_blank = self.create_blank_image((w,h))

        for img in images_list:
            index_ = images_list.index(img)
            temp_img = self.image_from_url(img)
            img_width, img_height =  temp_img.size
            if temp_img is not None:
                image_blank.paste(temp_img, ((index_ * self.base_width)+ (45 * index_) +15, 17 ), temp_img)
                ImageDraw.Draw(image_blank).text(((index_ * self.base_width)+ (45 * index_)+ img_width+20, 25 ), text_list[index_].replace(' ','\n',10), fill=(255,255,255),font=self.font)
                
        return image_blank



imgs = ['https://static.wikia.nocookie.net/gensin-impact/images/2/29/Constellation_Flower_of_Eden.png','https://static.wikia.nocookie.net/gensin-impact/images/d/d8/Constellation_Opening_of_Phanerozoic.png','https://static.wikia.nocookie.net/gensin-impact/images/e/e8/Constellation_Grace_of_Helios.png','https://static.wikia.nocookie.net/gensin-impact/images/8/8f/Constellation_Descent_of_Divinity.png','https://static.wikia.nocookie.net/gensin-impact/images/a/a1/Constellation_Tide_of_Hadean.png','https://static.wikia.nocookie.net/gensin-impact/images/5/52/Constellation_Dust_of_Purification.png']
text = ['Flower of Eden', 'Opening of Phanerozoic','Grace of Helios','Grace of Helios','Tide of Hadean','Dust of Purification']
img_m = ImageGenerator()
test = img_m.create_image(imgs,text)
test.show()