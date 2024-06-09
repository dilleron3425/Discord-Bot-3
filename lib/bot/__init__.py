import discord
import time
import json
import datetime
from logging import disable, INFO
from discord.ext.commands import Bot as BotBase     
from discord.ext import commands
from discord import Embed
from rich.console import Console
from threading import Thread
from rich.live import Live
from rich.text import Text
from lib.bot.console import console


def animated_loading():
    text = Text()
    dots = ["", ".", "..", "..."]
    with Live(text, refresh_per_second=5) as live:
        while not bot.ready:
            for i in range(100):
                text.plain = f"Loading{dots[i % len(dots)]}"
                live.update(text)
    Thread(target=console, daemon=True).start()

class George(BotBase):
    def __init__(self):
        self.ready = False
        self.console = Console()
        disable(INFO)
        intents = discord.Intents.all()
        intents.message_content = True
        self.current_date = datetime.datetime.now().date()

        with open("./data/json/config.json") as file:
            self.config = json.load(file)

        with open(self.config["paths"]["users_path"]) as f:
            self.data = json.load(f)

        super().__init__(command_prefix=commands.when_mentioned_or('?'), owner_id=self.config["ids"]["owner_id"], intents=intents)
        
    def run(self):
        super().run(self.config["token"], reconnect=True)

    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Ошибка!', color=discord.Colour.from_rgb(255, 0, 0))
            embed.add_field(value=f'{ctx.author.mention}, обязательно укажите аргумент!')
            await ctx.send(embed=embed)
            self.console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] George? says - "{ctx.author} be sure to specify an argument!"')
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Ошибка!', color=discord.Colour.from_rgb(255, 0, 0))
            embed.add_field(name='', value=f'{ctx.author.mention}, у вас не достаточно прав!')
            await ctx.send(embed=embed)
            self.console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] George? says - "{ctx.author} not enough rights!"')
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title='Ошибка!',  color=discord.Colour.from_rgb(255, 0, 0))
            embed.add_field(name='', value=f'{ctx.author.mention}, такой команды нету!')
            await ctx.send(embed=embed)
            self.console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] George? says - "{ctx.author} there is no such command!"')

    async def on_error(self, event, *args, **kwargs):
            embed = discord.Embed(title='Произошла ошибка!',
                                color=discord.Colour.from_rgb(255, 0, 0),
                                timestamp=datetime.datetime.now())
            embed.add_field(name=f'В {event}: ', value=f'{args} {kwargs}')
            embed.add_field(name="Желательно!",value=f'Пожалуйста, отправьте эту ошибку(ссылкой) на канал: {self.config["channels"]["bugs"]} и получите +3 репутации!')
            embed.set_footer(text='\u200b', icon_url=self.config['urls']['url_icon_bug'])
            if event.startswith('on_message'):
                ctx = args[0]
                channel = ctx.channel
            else:
                channel = self.get_channel(self.config["channels"]["errors"])
            await channel.send(embed=embed)
            self.console.print(f'[#FF0000][{self.current_date} {time.strftime("%X")}][/] An error [#FFA500]{event}[/] has occurred:\n {args} {kwargs} \n')
            raise

    async def on_ready(self):
        self.stdout = self.get_channel(self.config["test_channel"])
        if not self.ready:
            self.ready = True
            await super().change_presence(status=discord.Status.online, activity=discord.Activity(name=' ', type=4, state=f'Версия: {self.config["version"]}'))
            embed = Embed(title='George? был только что запущен!!!',
                          colour=discord.Colour.from_rgb(0, 0, 0),
                          timestamp=datetime.datetime.now())
            embed.set_footer(text='\u200b', icon_url=f'{self.config["urls"]["url_icon_clock"]}')
            await self.stdout.send(embed=embed)
        else:
            await super().change_presence(status=discord.Status.online, activity=discord.Activity(name=' ', type=4, state=f'Версия: {self.config["version"]}'))
            embed = Embed(title='George? был только что пере подключён!!!',
                          colour=discord.Colour.from_rgb(255, 0, 0),
                          timestamp=datetime.datetime.now())
            embed.set_footer(text='\u200b', icon_url=self.config["urls"]["url_icon"])
            await self.stdout.send(embed=embed)
            self.console.print(f'[#a0a0a0]{self.current_date}[/] George? just joined up!!!')

    async def logs(self, msg, channel=None, author: str = None):
        with open(self.config['paths']["log_path"], 'a', encoding='utf-8') as logs:
            logs.write(f'[{self.current_date} {time.strftime("%X")}] [{channel}] [{author}] {msg}\n')

    async def on_message(self, message):
        try:
            self.console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] |{message.channel.name}| |{message.author}| {message.content}')
            await self.logs(message.content, message.channel.name, message.author)
        except AttributeError:
            self.console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] |{message.author}| {message.content}')
            return await self.logs(message.content, message.author)

        if message.author == self.user:
            return

        names_dict = {self.config["ids"]["max_id"]: discord.Colour.from_rgb(255, 0, 0),
              self.config["ids"]["dima_id"]: discord.Colour.from_rgb(0, 128, 0),
              self.config["ids"]["leo_id"]: discord.Colour.from_rgb(255, 165, 0),
              self.config["ids"]["egor_id"]: discord.Colour.from_rgb(139, 0, 255)}
        names = self.data['names']

        for name, color in names_dict.items():
            if message.author.name.lower() in [name.lower() for sublist in names.values() for name in sublist]:
                embed = Embed(description=f'  {name} тебя зовут! ', color=color)
                await message.channel.send(embed=embed)
                self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} mentioned {name}")
                break

bot = George()
th1 = Thread(target=animated_loading).start()
