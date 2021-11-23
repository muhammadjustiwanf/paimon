# paimon-bot
 

![Logo](https://github.com/reko-beep/paimon-bot/blob/main/logo.gif?raw=true)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/reko-beep/)


Paimon bot mainly created for discord community of Pakistan Genshin Impact server, but now being built for self hosting now, you are free to use it, if you want!
it contains

    🔸 Paimon soundboard! (sounds provided | genshin fandom voiceovers)
    🔸 Support for build and ascension commands (you need to add yours own in the respective folder)
    🔸 Paimon quotes (taken from paimonquotes twitter handle!)
    🔸 Quests with chapters and acts. (Guides taken from Genshin Impact fandom page!)    
    🔸 Shows genshin stats and characters from hoyolab (api wrapper by thesadru on github)
 


# Being worked on

[Logo](https://flevix.com/wp-content/uploads/2019/12/Barline-Loading-Images-1.gif?raw=true)

Wish History (Almost done!)
Users custom builds creator. 
Build Notes. 
Quests Code rewriting. 
     
     
# Setting up the bot
 
  Will be updated soon ![In Progress](https://flevix.com/wp-content/uploads/2019/12/Barline-Loading-Images-1.gif?raw=true))
# How can I get my cookies?
**Taken from thesadru/genshinstats github**
1. go to [hoyolab.com](https://www.hoyolab.com/genshin/)
2. login to your account
3. press `F12` to open inspect mode (aka Developer Tools)
4. go to `Application`, `Cookies`, `https://www.hoyolab.com`.
5. copy `ltuid` and `ltoken`
6. use `set_cookie(ltuid=..., ltoken=...)` in your code
> It is possible that ltuid or ltoken are for some reason not avalible in your cookies (blame it on mihoyo).
> In this case there are probably the old `account_id` and `cookie_token` cookies, so use those with `set_cookie(account_id=..., cookie_token=...)`.


# Guides setup

**Delete** delete_this_file.txt in builds and ascension_talents folder.

**Adding new characters**

    Adding folders name for additional characters in characters.json, will add them to bot!

**File Naming**

    builds folder should have character builds whether in jpg or png.
        Naming should be like this for build.

            sub_dps.jpg, its title would translate to Sub DPS in discord embeds.
            main_dps.jpg, its title would translate to Main DPS in discord embeds.
            support.jpg, its title would translate to Support in discord embeds.
            healer.jpg etc, its title would translate to Healer in discord embeds.

    ascension files can be named as you want as their titles are not translated in discord embeds.

 
 
**Guides found on Net**
[GDrive](https://drive.google.com/drive/folders/1482z0uMPGM__NXoThBYboShYEodiXOwT?usp=sharing)

**NOTE**: These were made by world.of.teyvat on instagram, be sure to follow him. No copyrights reserved.
 
