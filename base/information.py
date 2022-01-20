from json import load,dump
from os.path import exists, isfile, join
from os import listdir,mkdir, getcwd
from bs4 import BeautifulSoup
import requests
from nextcord import Embed
import random
import time 
from datetime import datetime, date
from calendar import monthrange

class GenshinInformation:
    def __init__(self) -> None:
        self.path = f'{getcwd()}/assets/Information/'
    
    def get_options(self):
        '''
        options
        files in self.path
        '''
        options = [f.split('.')[0].title() for f in listdir(self.path) if isfile(join(self.path,f))]
        return options
    
    def get_names_list(self, option: str):
        '''
        gets items names from option -> option.json
        '''

        option = option.lower()
        if exists(self.path + "/" + option+ ".json"):
            with open(self.path + "/" + option+ ".json",'r') as f:
                names = list(load(f).keys())
                return names
        return []
    
    def get_data(self, option: str, name: str):
        '''
        gets data of an item
        '''
        data = {}
        if exists(self.path + "/" + option+ ".json"):
            with open(self.path + "/" + option+ ".json",'r') as f:
                data = load(f)
        if name in data:
            return data[name]

    def create_artifact_embeds(self, option: str,name: str):
        '''
        create artifacts embed
        '''
        
        data = self.get_data(option,name)
        embeds = {}
        if data is not None:
            main_embed = Embed(title=f'{name}',color=0xf5e0d0)       
            if bool(data['obtain']):
                for star in data['obtain']:
                    obtain_text = ''
                    for sources in data['obtain'][star]:
                        obtain_text += '\n'.join(data['obtain'][star][sources])
                        obtain_text += '\n'
                    main_embed.add_field(name=f'{star} stars artifact obtained from:',value=obtain_text)
            else:
                main_embed.add_field(name=f'Obtain from:',value='Sorry its no where to be found!')
            if bool(data['rarity']):
                text = f"{data['rarity'][0]} - {data['rarity'][-1]} "
                main_embed.add_field(name=f'Rarity:',value=text)
            else:
                main_embed.add_field(name=f'Rarity:',value=':(')
            if 'bonus' in data and bool(data['bonus']):
                bonuses = ['2','4']
                for bonus in bonuses:
                    if bonus in data['bonus']:
                        main_embed.add_field(name=f'{bonus} pc Bonus',value=data['bonus'][bonus])
            if bool(data['pieces']):
                for piece in data['pieces']:
                    piece_embed = Embed(title=f"{name} {piece['type']}",color=0xf5e0d0)    
                    piece_embed.add_field(name='Name',value=piece['name'])
                    if 'description' in piece:
                        piece_embed.add_field(name='Lore',value=piece['description'])   
                    piece_embed.set_thumbnail(url=piece['img'])
                    embeds[piece['type']] = piece_embed
            else:
                main_embed.add_field(name='Pieces',value='None found!')
            embeds['Main Information'] = main_embed
        return embeds
        
    def create_weapon_embeds(self, option: str,name: str):

        '''
        create weapon embeds
        '''
        
                

        data = self.get_data(option,name)
        embeds = {}
        def minimum_information(data, embed):
            information = ['type','obtain','rarity','series']
            for inf in information:
                if inf in data:
                    if inf == 'rarity':
                        embed.add_field(name=inf.title(),value='⭐' * int(data[inf]))
                    else:
                        embed.add_field(name=inf.title(),value=data[inf])
                else:
                    embed.add_field(name=inf.title(),value='nothing found anything in database')
        if data is not None:
            main_embed = Embed(title=f'{name}',color=0xf5e0d0)       
            minimum_information(data,main_embed)
            if 'stats' in data:
                stats = data['stats']
                for stat in stats:
                    main_embed.add_field(name=stat,value=stats[stat])
            
            if 'image' in data:
                main_embed.set_image(url=data['image'][0])
            embeds['Main Information'] = main_embed

            # refinement

            if 'refinement' in data:
                if bool(data['refinement']):
                    text = data['refinement']['text']
                    for refinement in data['refinement']:                        
                        if type(data['refinement'][refinement]) == dict:                            
                            text_modified = text
                            for values in data['refinement'][refinement]:
                                text_modified = text_modified.replace(values,data['refinement'][refinement][values],1)
                            embed = Embed(title=f'{name} Refinement level {refinement}',color=0xf5e0d0)       
                            minimum_information(data,embed)
                            embed.add_field(name='Refinement Description',value=text_modified,inline=False)
                            if 'image' in data:
                                embed.set_thumbnail(url=data['image'][0])
                            embeds[f'{name} Refinement level {refinement}'] = embed
            
            #ascension

            if 'ascension' in data:
                if bool(data['ascension']):
                    for level in data['ascension']:
                        items = data['ascension'][level]
                        embed = Embed(title=f'{name} Ascension level {level}',color=0xf5e0d0)
                        minimum_information(data,embed)
                        text_ = ''
                        for item in items:
                            text_ +=  f"**{item['name']}** {item['amount']}\n"
                        embed.add_field(name=f'Ascension Materials required',value=text_,inline=False)
                        if 'image' in data:
                            embed.set_thumbnail(url=data['image'][0])
                        embeds[f'{name} Ascension level {level}'] = embed
            
            return embeds

    def create_character_embeds(self,  option: str,name: str):
        '''
        create character embeds
        '''
        def minimum_information(data, embed):
            information = ['element','sex','rarity','weapon']
            for inf in information:
                if inf in data:
                    if inf == 'rarity':
                        embed.add_field(name=inf.title(),value='⭐' * int(data[inf]))
                    else:
                        embed.add_field(name=inf.title(),value=data[inf])
                else:
                    embed.add_field(name=inf.title(),value='found anything in database')
                

        data = self.get_data(option,name)
        embeds = {}
        if data is not None:
            if 'description' in data:
                description = data['description']
            else:
                description = ''
            main_embed = Embed(title=f'{name}',description=description,color=0xf5e0d0)       
            minimum_information(data,main_embed)
            others = ['constellation','birthday','region','affiliation','dish','parents','obtain','releaseDate','siblings']
            for other in others:
                if other in data:
                    value_ = data[other]
                    if type(data[other]) == list:
                        value_ = '\n'.join(data[other])
                    main_embed.add_field(name=other.title(),value=value_)

            if 'image' in data:
                main_embed.set_image(url=data['image'][0])
            embeds['Main Information'] = main_embed

            # constellation

            if 'constellations' in data:
                if bool(data['constellations']):
                    constellations = data['constellations']
                    for level in constellations:                        
                        if type(constellations[level]) == dict:                            
                            
                            embed = Embed(title=f'{name} Constellation level {level}',color=0xf5e0d0)       
                            minimum_information(data,embed)
                            
                            embed.add_field(name=constellations[level]['name'],value=constellations[level]['effect'],inline=False)
                            if 'image' in data:
                                embed.set_thumbnail(url=data['image'][0])
                            embeds[f'{name} Constellation level {level}'] = embed
            
            #talents

            if 'talents' in data:
                talents = data['talents']                
                embed = Embed(title=f'{name} Talents',color=0xf5e0d0)       
                minimum_information(data,embed)
                for talent in talents:
                    embed.add_field(name=talent['type'],value=talent['name'],inline=False)       
                embeds[f'{name} Talents'] = embed


            #ascension

            if 'ascension' in data:
                if bool(data['ascension']):
                    for level in data['ascension']:
                        items = data['ascension'][level]
                        embed = Embed(title=f'{name} Ascension level {level}',color=0xf5e0d0)       
                        minimum_information(data,embed)
                        text_ = ''
                        for item in items:
                            text_ +=  f"**{item['name']}** {item['amount']}\n"
                        embed.add_field(name=f'Ascension Materials required',value=text_)
                        if 'image' in data:
                                embed.set_thumbnail(url=data['image'][0])
                        embeds[f'{name} Ascension level {level}'] = embed
            
            return embeds
                            
       
    def daily_posts(self ,sub, flair):
        link = f'https://www.reddit.com/r/{sub}/search.rss?q=flair:{flair}&restrict_sr=on&sort=new&t=all'
        headers_ = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        r = requests.get(link,headers=headers_).content    
        bs = BeautifulSoup(r,'lxml')
        items = bs.find_all("content",{"type":"html"})    
        images_ = []
        for i in items:      
            text_ = i.text                     
            parser = text_
            while "href" in parser:
                s = str(self.find_href(parser))
                parser = parser.replace("href","",1)            
                s = s.strip('"')
                if '.jpg' in s:
                    images_.append(s)
                else:
                    if '.png' in s:
                        images_.append(s)           
        return [img for img in images_ if 'preview' not in img]

    
    def load_daily_posts(self):
        correct_path = self.path[:self.path.find(self.path.split('/')[-2])]
        with open(correct_path + '/wallpapers.json', 'r') as f:
            return load(f)

    def search_list(self, dict, search):
        for key in dict:
            if search.lower() in key.lower():
                return dict[key]

    def find_href(self, text):
        s = text.find("href")+len("href=")
        t_s = text[s:]
        t_s_s = t_s.find(">")
        t_s_s_s = t_s[:t_s_s]
        return t_s_s_s                    

    def all_lists(self, dict):
        lists =[]
        for key in dict:
            lists += dict[key]
        return lists



    def embeds_daily_posts(self, char: str = None):
        
        dict_ = self.load_daily_posts()
        lists = self.all_lists(dict_)
        if char is not None:
            list_img = self.search_list(dict_, char)
        random.seed(time.perf_counter())
        random.shuffle(list_img)
        list_ = random.sample(list_img,20)       
        embeds = {}
        for c,img in enumerate(list_,1):
            embed = Embed(title='Daily Genshin Post',color=0xf5e0d0)       
            embed.set_image(url=img)       
            embeds[f'Daily Post {c}'] = embed
        if len(embeds) == 0:
            embeds['Nothing Found'] = Embed(title='Nothing found',color=0xf5e0d0)    
        return embeds 


    def get_date(self, string, year):
        
        s = string.lower().split(' ')
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(s[0])+1
        date_ = int(s[1][:-2]) if s[1][:-2].isdigit() else 1
        return month, date_

    def calculate_difference(self, from_, to, year):
        
        to_month, to_date = to
        from_month, from_date = from_

        days_diff = -1
        if to_month == from_month:
            days_diff = to_date- from_date
        else:
            if to_month > from_month:
                ds = []
                for m in range(from_month, to_month+1,1):

                    days = monthrange(year, m)[1]
                    ds.append(days)
                ds[0] = ds[0] - from_date  
                ds[-1] = to_date    
                days_diff = sum(ds)
        if days_diff < 0:
            return None
        return days_diff
       

    def get_bday(self, month, day):
        current = datetime.now()
        current_date = date(current.year, month, day)
        with open(self.path+ '/characters.json','r') as f:
            data = load(f)
        bday_characters = []
        bday_date = []
        bday_difference = []
        bday_thumb_links = []
        for b in data:
            if b != 'Traveler':
                if 'birthday' in data[b]:
                    m,d = self.get_date(data[b]['birthday'], current_date.year)            
                    
                    diff = self.calculate_difference((current_date.month, current_date.day), (m,d), current_date.year)
                    if diff is not None:
                        bday_characters.append(b)
                        bday_thumb_links.append(data[b]['image'][-1])
                        bday_date.append(data[b]['birthday'])
                        bday_difference.append(diff)


        bday_close = bday_difference.index(min(bday_difference))

        return bday_characters[bday_close], bday_date[bday_close], bday_thumb_links[bday_close]




