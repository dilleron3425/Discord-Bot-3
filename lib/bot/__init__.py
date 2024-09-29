from discord import Embed, Intents, Colour, Status, Activity
from time import strftime, perf_counter
from logging import disable, INFO
from discord.ext import commands
from rich.console import Console
from datetime import datetime
from threading import Thread
from rich.live import Live
from rich.text import Text

from lib.cogs.json_loader import JsonLoader
from lib.bot.console import CLI
from lib.cogs.messages import Messenger

def animated_loading() -> None:
    text = Text()
    dots = ["", ".", "..", "..."]
    with Live(text, refresh_per_second=5) as live:
        while not bot.ready:
            for i in range(100):
                text.plain = f"Loading{dots[i % len(dots)]}"
                live.update(text)
    Thread(target=CLI, args=(JsonLoader(), ), daemon=True).start()


class George(commands.Bot):
    def __init__(self) -> None:
        self.ready = False
        disable(INFO)
        intents = Intents.all()
        intents.message_content = True
        self.current_date = datetime.now().date()
        self.console = Console()
        self.json_loader = JsonLoader()
        self.messenger = Messenger(self.json_loader, self.console)
        self.config = self.json_loader.json_data['config']
        self.data = self.json_loader.json_data['users']
        self.bad_words = self.json_loader.json_data['bad_words']
        super().__init__(command_prefix=commands.when_mentioned_or('?'), owner_id=self.config["ids"]["owner_id"], intents=intents)
        
    def run(self) -> None:
        super().run(self.config["token"], reconnect=True)

    async def clear_error(self, ctx, error) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(title='Ошибка!', color=Colour.from_rgb(255, 0, 0))
            embed.add_field(value=f'{ctx.author.mention}, обязательно укажите аргумент!')
            await ctx.send(embed=embed)
            self.console.print(f'[#a0a0a0][{self.current_date} {strftime("%X")}][/] George? says - "{ctx.author} be sure to specify an argument!"')
        if isinstance(error, commands.MissingPermissions):
            embed = Embed(title='Ошибка!', color=Colour.from_rgb(255, 0, 0))
            embed.add_field(name='', value=f'{ctx.author.mention}, у вас не достаточно прав!')
            await ctx.send(embed=embed)
            self.console.print(f'[#a0a0a0][{self.current_date} {strftime("%X")}][/] George? says - "{ctx.author} not enough rights!"')
        if isinstance(error, commands.CommandNotFound):
            embed = Embed(title='Ошибка!',  color=Colour.from_rgb(255, 0, 0))
            embed.add_field(name='', value=f'{ctx.author.mention}, такой команды нету!')
            await ctx.send(embed=embed)
            self.console.print(f'[#a0a0a0][{self.current_date} {strftime("%X")}][/] George? says - "{ctx.author} there is no such command!"')

    async def on_error(self, event, *args, **kwargs) -> None:
            embed = Embed(title='Произошла ошибка!',
                                color=Colour.from_rgb(255, 0, 0),
                                timestamp=datetime.now())
            embed.add_field(name=f'В {event}: ', value=f'{args} {kwargs}')
            embed.add_field(name="Желательно!",value=f'Пожалуйста, отправьте эту ошибку(ссылкой) на канал: {self.config["channels"]["bugs"]} и получите +3 репутации!')
            embed.set_footer(text='\u200b', icon_url=self.config['urls']['url_icon_bug'])
            if event.startswith('on_message'):
                ctx = args[0]
                channel = ctx.channel
            else:
                channel = self.get_channel(self.config["channels"]["errors"])
            await channel.send(embed=embed)
            self.console.print(f'[#FF0000][{self.current_date} {strftime("%X")}][/] An error [#FFA500]{event}[/] has occurred:\n {args} {kwargs} \n')
            raise

    async def on_ready(self) -> None:
        self.stdout = self.get_channel(self.config["test_channel"])
        if not self.ready:
            self.ready = True
            await super().change_presence(status=Status.online, activity=Activity(name=' ', type=4, state=f'Версия: {self.config["version"]}'))
            embed = Embed(title='George? был только что запущен!!!',
                          color=Colour.from_rgb(0, 0, 0),
                          timestamp=datetime.now())
            embed.set_footer(text='\u200b', icon_url=f'{self.config["urls"]["url_icon_clock"]}')
            await self.stdout.send(embed=embed)
        else:
            await super().change_presence(status=Status.online, activity=Activity(name=' ', type=4, state=f'Версия: {self.config["version"]}'))
            embed = Embed(title='George? был только что пере подключён!!!',
                          color=Colour.from_rgb(255, 0, 0),
                          timestamp=datetime.now())
            embed.set_footer(text='\u200b', icon_url=self.config["urls"]["url_icon_clock"])
            await self.stdout.send(embed=embed)
            self.console.print(f'[#a0a0a0]{self.current_date}[/] George? just joined up!!!')

    async def on_message(self, message) -> None:
        await self.messenger.on_message(message)

bot = George()
th1 = Thread(target=animated_loading).start()
