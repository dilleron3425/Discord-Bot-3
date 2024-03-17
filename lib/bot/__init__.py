import discord
import time
import json
import string
import asyncio
import os
import random
from discord.ext.commands import Bot as BotBase
from discord.ext import commands
import datetime
from discord import Embed
from rich.progress import Progress
from rich.console import Console
from threading import Thread


def pr_bar():
    with Progress() as progress:
        processing = progress.add_task('[green]Загрузка...', total=100)
        while not progress.finished:
            progress.update(processing, advance=1)
            time.sleep(0.026)


async def send_photo(channel_id, image_path, scheduled_time):
    current_time = datetime.datetime.now().time()
    scheduled_time = datetime.datetime.strptime(scheduled_time, "%H:%M").time()
    channel = bot.get_channel(channel_id)
    time_diff = (datetime.datetime.combine(datetime.date.today(), scheduled_time) - datetime.datetime.combine(
        datetime.date.today(), current_time)).total_seconds()

    if time_diff > 0:
        await asyncio.sleep(time_diff)

        if channel:
            directory = image_path
            files = os.listdir(directory)
            random_file = random.choice(files)
            file_path = os.path.join(directory, random_file)

            file = discord.File(file_path)
            await channel.send(file=file)
            os.remove(file_path)
        else:
            print("Неверный ID канала!")


class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.console = Console()
        self.current_date = datetime.datetime.now().date()

        super().__init__(command_prefix='!', owner_id='ID', intents=discord.Intents.all())

    def run(self, version):
        with open('PATH', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()
        super().run(self.TOKEN, reconnect=True)

    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Ошибка!', color=discord.Colour.from_rgb(255, 0, 0))
            embed.add_field(value=f'{ctx.author.mention}, обязательно укажите аргумент!')
            await ctx.send(embed=embed)
            self.console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] George? говорит - "{ctx.author} обязательно указать аргумент!"')
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Ошибка!', color=discord.Colour.from_rgb(255, 0, 0))
            embed.add_field(name='', value=f'{ctx.author.mention}, у вас не достаточно прав!')
            await ctx.send(embed=embed)
            self.console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] George? говорит - "{ctx.author} не достаточно прав!"')
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title='Ошибка!',  color=discord.Colour.from_rgb(255, 0, 0))
            embed.add_field(name='', value=f'{ctx.author.mention}, такой команды нету!')
            await ctx.send(embed=embed)
            self.console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] George? говорит - "{ctx.author} такой команды нету!"')

    async def on_error(self, *args, **kwargs):
        embed = discord.Embed(title='Произошла ошибка!',
                              color=discord.Colour.from_rgb(255, 0, 0),
                              timestamp=datetime.datetime.now())
        embed.set_footer(text='\u200b', icon_url='URL')
        await self.stdout.send(embed=embed)
        raise

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.stdout = self.get_channel('CHANNEL')
            await super().change_presence(status=discord.Status.online, activity=discord.Activity(name=' ', type=4, state='Версия: 3.2.1.0'))
            self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] George готов к работе ╰(*°▽°*)╯")
            self.console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] Version: 3.2.1.0')
            embed = Embed(title='George? был только что запущен!!!',
                          colour=discord.Colour.from_rgb(0, 0, 0),
                          timestamp=datetime.datetime.now())
            embed.set_footer(text='\u200b', icon_url='URL')
            await self.stdout.send(embed=embed)
            await send_photo('CHANNEL', "PATH", "TIME")
        else:
            embed = Embed(title='George? был только что пере подключён!!!',
                          colour=discord.Colour.from_rgb(255, 0, 0),
                          timestamp=datetime.datetime.now())
            embed.set_footer(text='\u200b', icon_url='URL')
            await self.stdout.send(embed=embed)
            self.console.print(f'[#a0a0a0]{self.current_date}[/] George? только что пере подключился!!!')

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
            self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} упомянул NAME")

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                .intersection(set(json.load(open('PATH')))) != set()):
            _id = '<@ID>'
            embed = Embed(description='  %s тебя зовут! ' % _id, color=discord.Colour.from_rgb(0, 128, 0))
            await message.channel.send(embed=embed)
            self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} упомянул NAME")

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                .intersection(set(json.load(open('PATH')))) != set()):
            _id = '<@ID>'
            embed = Embed(description='  %s тебя зовут! ' % _id, color=discord.Colour.from_rgb(255, 165, 0))
            await message.channel.send(embed=embed)
            self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} упомянул NAME")

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                .intersection(set(json.load(open('PATH')))) != set()):
            _id = '<@ID>'
            embed = Embed(description='  %s тебя зовут! ' % _id, color=discord.Colour.from_rgb(139, 0, 255))
            await message.channel.send(embed=embed)
            self.console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} упомянул NAME")

th1 = Thread(target=pr_bar).start()
bot = Bot()
