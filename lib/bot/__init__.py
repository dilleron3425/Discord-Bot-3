import discord
import time
import json
import string
from discord.ext.commands import Bot as BotBase
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from discord import Embed, File
from rich.progress import Progress
from rich.console import Console
from threading import Thread

PREFIX = '!'
OWNER_IDS = [609046827328733195]
console = Console()
boter = commands.Bot(command_prefix='!', intents=discord.Intents.all())


def pr_bar():
    with Progress() as progress:
        processing = progress.add_task('[green]Загрузка...', total=100)
        while not progress.finished:
            progress.update(processing, advance=1)
            time.sleep(0.027)


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.current_date = datetime.now().date()
        self.client = discord.Client(intents=discord.Intents.all())

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, intents=discord.Intents.all())

    def run(self, version):
        self.VERSION = version

        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print('George? подключился!!!')

    async def on_disconnect(self):
        channel = self.get_channel(1147910681488797819)
        embed = Embed(title='George? был только что отключён!!!')
        embed.set_footer(text='\u200b', icon_url='https://cdn-icons-png.flaticon.com/512/7704/7704523.png')
        await channel.send(embed=embed)
        console.print(f'[#a0a0a0]{self.current_date}[/] George? только что отключился!!!')

    async def on_ready(self):
        console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] George готов к работе ╰(*°▽°*)╯")
        console.print(f'[#a0a0a0][{self.current_date} {time.strftime("%X")}][/] Version: 3.1.0.0')
        if not self.ready:
            self.ready = True
            channel = self.get_channel(1147910681488797819)
            embed = Embed(title='George? был только что запущен!!!',
                          colour=discord.Colour.from_rgb(0, 0, 0),
                          timestamp=datetime.now())
            embed.set_footer(text='\u200b', icon_url='https://cdn-icons-png.flaticon.com/512/11338/11338063.png')
            await channel.send(embed=embed)

        else:
            channel = self.get_channel(1147910681488797819)
            embed = Embed(title='George? был только что пере подключён!!!',
                          colour=discord.Colour.from_rgb(255, 0, 0),
                          timestamp=datetime.now())
            embed.set_footer(text='\u200b', icon_url='https://cdn-icons-png.flaticon.com/512/7704/7704523.png')
            await channel.send(embed=embed)
            console.print(f'[#a0a0a0]{self.current_date}[/] George? был только что пере подключился!!!')

    async def on_message(self, message):
        if message.author.bot == self.client.user:
            return

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                    .intersection(set(json.load(open('./lib/json/max.json')))) != set()) and message.author:
            max_id = '<@609046827328733195>'
            embed = Embed(description='  %s тебя зовут! ' % max_id, color=discord.Colour.from_rgb(255, 0, 0))
            await message.channel.send(embed=embed)
            console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} упомянул Макса")

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                .intersection(set(json.load(open('./lib/json/dima.json')))) != set()):
            dima_id = '<@673532888834244608>'
            embed = Embed(description='  %s тебя зовут! ' % dima_id, color=discord.Colour.from_rgb(0, 128, 0))
            await message.channel.send(embed=embed)
            console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} упомянул Диму")

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                .intersection(set(json.load(open('./lib/json/leo.json')))) != set()):
            leo_id = '<@1079416902830534767>'
            embed = Embed(description='  %s тебя зовут! ' % leo_id, color=discord.Colour.from_rgb(255, 165, 0))
            await message.channel.send(embed=embed)
            console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} упомянул  Лёню")

        if ({i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.content.split(' ')}
                .intersection(set(json.load(open('./lib/json/egor.json')))) != set()):
            egor_id = '<@678631868018589696>'
            embed = Embed(description='  %s тебя зовут! ' % egor_id, color=discord.Colour.from_rgb(139, 0, 255))
            await message.channel.send(embed=embed)
            console.print(f"[#a0a0a0][{self.current_date} {time.strftime('%X')}][/] {message.author} упомянул Егора")

th1 = Thread(target=pr_bar).start()
bot = Bot()
