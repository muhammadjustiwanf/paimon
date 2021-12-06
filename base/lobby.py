import os
from pprint import pprint
import nextcord as discord
from nextcord.ext import commands,tasks
from os import listdir
from os.path import isfile, join
import json

from nextcord.member import Member

from core.paimon import Paimon

class Lobby:
    def __init__(self,bot: Paimon):
        self.vcs = {}
        self.bot = bot
        self.guild = 0    

        self.lobby_category = None
        self.lobbycreatevc = None
        self.paimon = None

    
        
        self._load()

    def set_settings(self,guild):
        self.guild = guild
        if self.lobby_category is None:
            self.lobby_category = self.guild.get_channel(self.bot.p_bot_config['lobby_category'])
        if self.lobbycreatevc is None:
            self.lobbycreatevc = self.guild.get_channel(self.bot.p_bot_config['lobby_createvc'])
        if self.paimon is None:
            self.paimon = self.bot.get_user(self.bot.user.id)
       

    def _load(self):
        if os.path.exists('vc.json'):
            with open('vc.json','r') as f:
                self.vcs = json.load(f)

    def _save(self,channelid,authorid):
         with open('vc.json','w') as f:  
            self.vcs[str(channelid)] = authorid           
            json.dump(self.vcs,f)
    
    def _update(self):
         with open('vc.json','w') as f:                  
            json.dump(self.vcs,f)

    async def create_vc(self,owner):
        if self.guild is not None:
            id_ = str(owner.id)
            if id_ in self.vcs:
                return None,None
            else:            
                name = f'🎮 {owner.display_name} Lobby!'
                overwrites = {
                        self.guild.default_role: discord.PermissionOverwrite(view_channel=True,connect=False,speak=False,use_voice_activation=False),
                        self.paimon: discord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                               add_reactions=True,
                                                               embed_links=True, attach_files=True,
                                                               read_message_history=True,
                                                               external_emojis=True,manage_permissions=True, manage_channels=True,
                                                               administrator=True),
                        owner: discord.PermissionOverwrite(view_channel=True, connect=True,speak=True,use_voice_activation=True,manage_permissions=True,mute_members=True,deafen_members=True)
                    }
                vc = await self.lobby_category.create_voice_channel(name,overwrites=overwrites)
                self.vcs[id_] = {'owner': owner.id, 'members': [], 'vc': vc.id}
                self._update()
                return True,vc
    
    async def allow_member(self,owner,member):
        if self.guild != 0:
            owner_ = str(owner.id)      
            if owner_ in self.vcs:
                if 'vc' in self.vcs[owner_]:
                    channel_ = self.bot.get_channel(self.vcs[owner_]['vc'])
                    await channel_.set_permissions(member,connect=True,speak=True,use_voice_activation=True)
                    return channel_
                else:
                    return False
            else:
                return None    
    
    async def lock_vc(self, owner): 
        if self.guild != 0:
            id_ = str(owner.id)
            if id_ in self.vcs:
                vc = self.bot.get_channel(self.vcs[id_]['vc'])
                await vc.set_permissions(self.guild.default_role, read_messages=False, connect=False, speak=False,
                                     use_voice_activation=True)
                return True,vc
            else:
                return False,False

    async def unlock_vc(self, owner):
        if self.guild != 0:
            id_ = str(owner.id)
            if id_ in self.vcs:
                vc = self.bot.get_channel(self.vcs[id_]['vc'])
                await vc.set_permissions(self.guild.default_role, read_messages=True, connect=True, speak=True,
                                     use_voice_activation=True)
                return True,vc
            else:
                return False,False

    async def limit_vc(self,owner,limit):
        if self.guild != 0:
            id_ = str(owner.id)
            if id_ in self.vcs:
                vc = self.bot.get_channel(self.vcs[id_]['vc'])
                if limit == 0:
                    await vc.edit(user_limit=99)
                    return True,vc
                else:
                    await vc.edit(user_limit=limit)
                    return True,vc
            else:
                return None,None

    async def kick_member(self,owner,member):
        if self.guild != 0:
            id_ = str(owner.id)
            if id_ in self.vcs:
                if member != None:                
                    vc = self.bot.get_channel(self.vcs[id_]['vc'])
                    if member in vc.members:                    
                        await member.move_to(None)
                        return vc
                    else:
                        return False
                else:
                    return False
            else:
                return None

    async def unallow_member(self,owner,member):
        if self.guild != 0:
            id_ = str(owner.id)
            if id_ in self.vcs:
                if member != None:                
                    vc = self.bot.get_channel(self.vcs[id_]['vc'])
                    if member in vc.members:      
                        await vc.set_permissions(member,read_messages=True,view_channel=True, connect=False, speak=False, use_voice_activation=True)              
                        await member.move_to(None)
                        return vc
                    else:
                        return False
                else:
                    return False
            else:
                return None
    
    def get_owner_from_vc(self,channel):        
        id_ = str(channel.id)
        for i in self.vcs:
            if self.vcs[i]['vc'] == int(id_):
                return i

    def if_vc_exists(self,channel):
        id_ = channel.id
        for i in self.vcs:
            if self.vcs[i]['vc'] == id_:
                return True          

    async def voice_remove(self,channel):       
        if channel != None:
            members_list = channel.members           
            if self.if_vc_exists(channel) and channel != None:
                if len(members_list) == 0:
                    self.vcs.pop(str(self.get_owner_from_vc(channel)))
                    await channel.delete()   
                    self._update()                 
    
    async def auto_delete_event(self,member: Member,before,after):
        vc = member.voice
        if before.channel is None: 
            if self.lobbycreatevc is not None:
                if after.channel.id == self.lobbycreatevc.id:
                    check,vc_ = await self.create_vc(member)
                    if check != None:
                        await member.move_to(vc_)
        else:
            if after.channel is None:
                del_channel = before.channel
                await self.voice_remove(del_channel)

        
        