import os

from nextcord.ext import commands
from nextcord.ext.commands.bot import Bot

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from util.logging import logc


class ExtensionManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ext_path = "extensions.extra."
        self.name = 'Extension Manager'
        self.description = 'Handles all Extensions'
        self.loadext_all()

    
    @commands.command(aliases=['lext'],description='lext( extension name)\nLoads extension')
    async def loadext(self, ctx, arg):
        # todo: check if that file exists 
        # todo: add error handling.
        logc("loading extension", arg)
        self.bot.load_extension(self.ext_path + arg)


    @commands.command(aliases=['unlext'],description='unlext( extension name)\nUnloads extension')
    async def uloadext(self, ctx, arg):
        logc("unloading extension", arg)
        self.bot.unload_extension(self.ext_path + arg)

    @commands.command(aliases=['rlext'],description='lext( extension name)\nReloads extension')
    async def rloadext(self, ctx, arg):
        logc("reloading extension", arg)
        self.bot.reload_extension(self.ext_path + arg)


    def loadext_all(self):
        """finds modules from disk and loads them"""

        ## find all modules.
        extensions_dir = "extensions/extra" # folder containing all modules.         
        extensions = []


        for ext in os.listdir(extensions_dir):
            rootpkg = extensions_dir.replace('/', '.')

            # consider root module as extension.
            if ext.endswith('.py'):
                extpath =  ".".join([rootpkg, ext[:-3]])
                extensions.append(extpath)

            # consider folder type module (with __init__.py) as extension. 
            test_path = os.path.join(extensions_dir, ext, '__init__.py')
            if os.path.exists(test_path):
                extpath =  ".".join([rootpkg, ext])
                
                extensions.append(extpath)

        for ext in extensions:
            print(ext)
            self.client.load_extension(ext)
            logc('loaded extension:',  ext)



def setup(bot: Bot):
    bot.add_cog(ExtensionManager(bot))


    # extension file watcher: reloads when extra extension modules are modified
    class ExtensionFileChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            super().on_modified(event)
            if not event.is_directory:
                _, filename = os.path.split(event.src_path)
                module_name = filename[:-3]
                logc("reloading ", module_name)
                bot.reload_extension('extensions.extra.' + module_name)

    event_handler = ExtensionFileChangeHandler()
    observer = Observer()

    watch_path = os.path.join('extensions', 'extra')
    observer.schedule(event_handler, watch_path)
    observer.start()



def teardown(bot: Bot):
    bot.remove_cog("ExtensionManager")
