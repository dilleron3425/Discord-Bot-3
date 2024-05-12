import discord
import time
import json
import string
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

        super().__init__(command_prefix=commands.when_mentioned_or('?'), owner_id='ID', intents=intents)

    def run(self):
        with open('PATH', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()
        super().run(self.TOKEN, reconnect=True)

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

    async def on_error(self):
            embed = discord.Embed(title='Произошла ошибка!',
                                color=discord.Colour.from_rgb(255, 0, 0),
                                timestamp=datetime.datetime.now())
            embed.set_footer(text='\u200b', icon_url='PATH')
            await self.stdout.send(embed=embed)
            raise

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.stdout = self.get_channel('CHANNEL')
            await super().change_presence(status=discord.Status.online, activity=discord.Activity(name=' ', type=4, state='Версия: 3.2.2.0'))
        else:
            await super().change_presence(status=discord.Status.online, activity=discord.Activity(name=' ', type=4, state='Версия: 3.2.2.0'))
            embed = Embed(title='George? был только что пере подключён!!!',
                          colour=discord.Colour.from_rgb(255, 0, 0),
                          timestamp=datetime.datetime.now())
            embed.set_footer(text='\u200b', icon_url='URL')
            await self.stdout.send(embed=embed)
            self.console.print(f'[#a0a0a0]{self.current_date}[/] George? just joined up!!!')

    async def logs(self, msg, channel=None, author: str = None):
        with open('PATH', 'a', encoding='utf-8') as logs:
            logs.write(f'[{self.current_date} {time.strftime("%X")}] [{channel}] [{author}] {msg}\n')

    async def on_message(self, message):
        try:
            print(f'[{self.current_date} {time.strftime("%X")}] [{message.channel.name}] [{message.author}] {message.content}')
            await self.logs(message.content, message.channel.name, message.author)
        except AttributeError:
            print(f'[{self.current_date} {time.strftime("%X")}] [{message.author}] {message.content}')
            return await self.logs(message.content, message.author)

        if message.author == self.user:
            return

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                    .intersection(set(json.load(open('PATH')))) != set()) and message.author:
            _id = '<@ID>'
            embed = Embed(description='  %s тебя зовут! ' % _id, color=discord.Colour.from_rgb(255, 0, 0))
            await message.channel.send(embed=embed)
            self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} mentioned NAME")

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                .intersection(set(json.load(open('PATH')))) != set()):
            _id = '<@ID>'
            embed = Embed(description='  %s тебя зовут! ' % _id, color=discord.Colour.from_rgb(0, 128, 0))
            await message.channel.send(embed=embed)
            self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} mentioned NAME")

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                .intersection(set(json.load(open('PATH')))) != set()):
            _id = '<@ID>'
            embed = Embed(description='  %s тебя зовут! ' % _id, color=discord.Colour.from_rgb(255, 165, 0))
            await message.channel.send(embed=embed)
            self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} mentioned NAME")

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                .intersection(set(json.load(open('PATH')))) != set()):
            _id = '<@ID>'
            embed = Embed(description='  %s тебя зовут! ' % _id, color=discord.Colour.from_rgb(139, 0, 255))
            await message.channel.send(embed=embed)
            self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} mentioned NAME")

th1 = Thread(target=animated_loading).start()
bot = George()
