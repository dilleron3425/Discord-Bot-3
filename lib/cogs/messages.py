import datetime
from discord import Embed, Colour
from time import strftime, sleep
from rich.console import Console

from lib.cogs.game import PterodactylControl

class Messenger():
    def __init__(self, json_loader):
        self.ptero_control = PterodactylControl(json_loader)
        self.json_loader = json_loader
        self.console = Console()
        self.config = self.json_loader.json_data['config']
        self.data = self.json_loader.json_data['data']
        self.bad_words = self.json_loader.json_data['bad_words']
        self.current_date = datetime.datetime.now().date()
    
    async def logs(self, msg, channel=None, author: str = None):
        with open(self.config['paths']["log_path"], 'a', encoding='utf-8') as logs:
            logs.write(f'[{self.current_date} {strftime("%X")}] [{channel}] [{author}] {msg}\n')

    async def on_message(self, message):
            try:
                channel_name = getattr(message.channel, 'name', 'Unknown channel')
                author_name = getattr(message.author, 'name', 'Unknown author')
                if message.embeds:
                    for embed in message.embeds:
                        embed_content = f"{embed.title} | {embed.description}"
                        self.console.print(f'[#a0a0a0][{self.current_date} {strftime("%X")}][/] |{channel_name}| |{author_name}| {embed_content}')
                        await self.logs(embed_content, channel_name, author_name)
                else:
                    self.console.print(f'[#a0a0a0][{self.current_date} {strftime("%X")}][/] |{channel_name}| |{author_name}| {message.content}')
                    await self.logs(message.content, channel_name, author_name)
            except Exception as e:
                print(f'Error in on_message: {e}')

            for k_name, v_names in self.data['names'].items():
                if any(v_name.lower() in message.content.lower() for v_name in v_names):
                    if k_name + "_id" in self.config["ids"]:
                        name_id = self.config["ids"][k_name + "_id"]
                        await message.channel.send(f'{name_id} тебя зовут!')
                        self.console.print(f"[#a0a0a0][{self.current_date} {strftime('%X')}][/] {(message.author.name).capitalize()} mentioned {k_name.capitalize()}")
                        continue
                    break
            
            if any(word in message.content.lower() for word in self.bad_words['bad_words']):
                embed = Embed(title='Не ругайся матом!',
                                description='Ругаться это плохо! -3 репутации',
                                color=Colour.from_rgb(255, 0, 0))
                await message.channel.send(embed=embed)

            elif message.content.startswith("?help"):
                embed = Embed(title='Список команд!?',
                                description='**George? - третья версия Discord бота**',
                                color=Colour.from_rgb(0, 0, 0))
                embed.add_field(name='Версия George?', value=f'**{self.config['version']}**')
                embed.add_field(name='Разработчик', value=f'**{self.config['created_by']}**')
                embed.add_field(name='GitHub', value=f'**{self.config['urls']['url_github']}**')
                embed.add_field(name=':small_red_triangle_down: ?help', value='**Отображает список команд бота George?**', inline=False)
                embed.add_field(name=':small_red_triangle_down: ?start [имя_сервера]', value='**Запускает указанный сервер**', inline=False)
                embed.add_field(name=':small_red_triangle_down: ?restart [имя_сервера]', value='**Перезапускает указанный сервер**', inline=False)
                embed.add_field(name=':small_red_triangle_down: ?stop [имя_сервера]', value='**Останавливает указанный сервер**', inline=False)
                embed.add_field(name=':small_red_triangle_down: ?stat [имя_сервера]', value='**Показывает статистику указанного сервера**', inline=False)
                await message.channel.send(embed=embed)

            elif message.content.startswith("?start ") and message.content[7:].lower() in self.config['pterodactyl']['server_name']:
                server_status = self.ptero_control.server_start(self.config['pterodactyl']['server_name'][message.content[7:].lower()])
                for status in server_status:
                    server_name, server_info = next(iter(status.items()))
                    embed = Embed(title=f":mag_right: Статус {server_name}", color=server_info['color'])
                    embed.add_field(name=f':loudspeaker: {server_info['message']}', value='', inline=False)
                    if "Запускается..." not in server_info['message']:
                        embed.add_field(name=':round_pushpin: IP: dillertm.ru', value='')
                    if server_info.get('port') is not None:
                        embed.add_field(name=f':electric_plug: Порт: {server_info["port"]}', value='')
                    if server_info.get('core_name') is not None and server_info.get('core_version') is not None:
                        embed.add_field(name=f':cd: {server_info["core_name"]}: {server_info["core_version"]}', value='', inline=False)
                    await message.channel.send(embed=embed)

            elif message.content.startswith("?restart ") and message.content[9:].lower() in self.config['pterodactyl']['server_name']:
                server_status = self.ptero_control.server_restart(self.config['pterodactyl']['server_name'][message.content[9:].lower()])
                for status in server_status:
                    server_name, server_info = next(iter(status.items()))
                    embed = Embed(title=f":mag_right: Статус {server_name}", color=server_info['color'])
                    if "Перезапускается..." not in server_info['message']:
                        sleep(32)
                        embed.add_field(name=f':loudspeaker: {server_info['message']}', value='', inline=False)
                        embed.add_field(name=':round_pushpin: IP: dillertm.ru', value='')
                        if server_info.get('port') is not None:
                            embed.add_field(name=f':electric_plug: Порт: {server_info["port"]}', value='')
                        if server_info.get('core_name') is not None and server_info.get('core_version') is not None:
                            embed.add_field(name=f':cd: {server_info["core_name"]}: {server_info["core_version"]}', value='', inline=False)
                    else:
                        embed.add_field(name=f':loudspeaker: {server_info['message']}', value='')
                    await message.channel.send(embed=embed)
            
            elif message.content.startswith("?stop ") and message.content[6:].lower() in self.config['pterodactyl']['server_name']:
                server_status = self.ptero_control.server_stop(self.config['pterodactyl']['server_name'][message.content[6:].lower()])
                for status in server_status:
                    server_name, server_info = next(iter(status.items()))
                    embed = Embed(title=f":mag_right: Статус {server_name}", color=server_info['color'])
                    embed.add_field(name=f':loudspeaker: {server_info['message']}', value='')
                    await message.channel.send(embed=embed)
            
            elif message.content.startswith("?stat ") and message.content[6:].lower() in self.config['pterodactyl']['server_name']:
                server_status = self.ptero_control.server_status(self.config['pterodactyl']['server_name'][message.content[6:].lower()])
                for status in server_status:
                    server_name, server_info = next(iter(status.items()))
                    embed = Embed(title=f":mag_right: Статус {server_name}", color=server_info.get('color'))
                    embed.add_field(name=f':loudspeaker: {server_info['message']}', value='', inline=False)
                    embed.add_field(name=':round_pushpin: IP: dillertm.ru', value='')
                    embed.add_field(name=f':electric_plug: Порт: {server_info.get('port')}', value='')
                    embed.add_field(name=f':cd: {server_info.get('core_name')}: {server_info.get('core_version')}', value='', inline=False)
                    await message.channel.send(embed=embed)

            elif message.content.startswith("?stat all"):
                server_statuses = self.ptero_control.stat_all()
                embed = Embed(title=":mag_right: Статус всех серверов!", color=Colour.from_rgb(0, 0, 0))
                for status in server_statuses.items():
                    server_name, server_status = status
                    embed.add_field(name=f':white_circle:  {server_name}', value=f':loudspeaker: {server_status['message']}', inline=False)
                await message.channel.send(embed=embed)
            
            elif message.content.startswith(tuple(["?start", "?stat", "?restart", "?stop"])):
                for prefix in ["?start", "?stat", "?restart", "?stop"]:
                    if message.content.startswith(prefix):
                        if message.content[len(prefix):].strip().lower() not in [key.lower() for key in self.config['pterodactyl']['server_uuid'].keys()]:
                            embed = Embed(title="Неверный сервер или его не существует!", color=Colour.from_rgb(178,34,34))
                            await message.channel.send(embed=embed)
                        break
