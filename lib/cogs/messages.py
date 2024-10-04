from discord import Embed, Colour, TextChannel, Member, Message
from time import strftime, sleep
from asyncio import create_task
from re import search, escape
from os import path, makedirs
from datetime import datetime

from lib.cogs.game import PterodactylControl

class Messenger():
    def __init__(self, json_loader: dict, console: object) -> None:
        self.ptero_control = PterodactylControl(json_loader)
        self.console = console
        self.config = json_loader.json_data['config']
        self.data = json_loader.json_data['users']
        self.bad_words = json_loader.json_data['bad_words']
        self.current_date = datetime.now().date()

    async def logs(self, message: Message, channel: TextChannel = None, author: Member = None, embeds: list = None) ->  None:

        log_path = self.config['paths']["log_path"]
        channel_name = getattr(channel, 'name', 'Unknown channel')
        author_name = getattr(author, 'name', 'Unknown author')
        try:
            if not path.exists(log_path):
                makedirs(path.dirname(log_path))
                self.console.print(f'\n[#ff8700][Warning][/#ff8700] Файл журнала по пути "{log_path}" не найден, но был успешно создан.')        
            with open(log_path, 'a', encoding='utf-8') as logs:
                if embeds:
                    for embed in embeds:
                        embed_content = f"{embed.title} | {embed.description}"
                        logs.write(f'[{self.current_date} {strftime("%X")}] [{channel_name}] [{author_name}] {embed_content}\n')
                        self.console.print(f'[#a0a0a0][{self.current_date} {strftime("%X")}][/] |{channel_name}| |{author_name}| {embed_content}')
                else:
                    logs.write(f'[{self.current_date} {strftime("%X")}] [{channel_name}] [{author_name}] {message}\n')
                    self.console.print(f'[#a0a0a0][{self.current_date} {strftime("%X")}][/] |{channel_name}| |{author_name}| {message}')
        except PermissionError:
            self.console.print(f'\n[bold red][Error][/bold red] Разрешение отклонено: невозможно выполнить запись в файл журнала. "{log_path}"')

    async def names(self, message: Message) -> None:
        for k_name, v_names in self.data['names'].items():
            if any(search(r'\b' + escape(v_name.lower()) + r'(?:[^а-я]|$)', message.content.lower()) for v_name in v_names):
                if k_name + "_id" in self.config["ids"]:
                    name_id = self.config["ids"][k_name + "_id"]
                    await message.channel.send(f'{name_id} тебя зовут!')
                    self.console.print(f"[#a0a0a0][{self.current_date} {strftime('%X')}][/] {(message.author.name).capitalize()} mentioned {k_name.capitalize()}")
                    continue
                break
        
    async def help(self, message: Message) -> Embed:
        embed = Embed(title='Список команд!?',
                        description='**George? - третья версия Discord бота**',
                        color=Colour.from_rgb(0, 0, 0))
        embed.add_field(name='Версия George?', value=f'**{self.config["version"]}**')
        embed.add_field(name='Разработчик', value=f'**{self.config["created_by"]}**')
        embed.add_field(name='GitHub', value=f'**{self.config["urls"]["url_github"]}**')
        embed.add_field(name=':small_red_triangle_down: ?help', value='**Отображает список команд бота George?**', inline=False)
        embed.add_field(name=':small_red_triangle_down: ?start [имя_сервера]', value='**Запускает указанный сервер**', inline=False)
        embed.add_field(name=':small_red_triangle_down: ?restart [имя_сервера]', value='**Перезапускает указанный сервер**', inline=False)
        embed.add_field(name=':small_red_triangle_down: ?stop [имя_сервера]', value='**Останавливает указанный сервер**', inline=False)
        embed.add_field(name=':small_red_triangle_down: ?stat [имя_сервера]', value='**Показывает статистику указанного сервера**', inline=False)
        await message.channel.send(embed=embed)
  
    async def start_server(self, message: Message) -> Embed:
        server_status = self.ptero_control.server_start(self.config['pterodactyl']['server_name'][message.content[7:].lower()])
        starting_message = None
        for status in server_status:
            server_name, server_info = next(iter(status.items()))
            embed = Embed(title=f":mag_right: Статус {server_name}", color=server_info['color'])
            embed.add_field(name=f':loudspeaker: {server_info["message"]}', value='', inline=False)
            if "Запускается..." in server_info['message']:
                starting_message = await message.channel.send(embed=embed)
            elif "Уже запущен" in server_info['message']:
                await message.channel.send(embed=embed)
                return
            else:
                if starting_message:
                    await starting_message.delete()
                embed.add_field(name=':round_pushpin: IP: dillertm.ru', value='')
                if server_info.get('port') is not None:
                    embed.add_field(name=f':electric_plug: Порт: {server_info["port"]}', value='')
                if server_info.get('core_name') is not None and server_info.get('core_version') is not None:
                    embed.add_field(name=f':cd: {server_info["core_name"]}: {server_info["core_version"]}', value='', inline=False)
                await message.channel.send(embed=embed)
    
    async def restart_server(self, message: Message) -> Embed:
        server_status = self.ptero_control.server_restart(self.config['pterodactyl']['server_name'][message.content[9:].lower()])
        starting_message = None
        for status in server_status:
            server_name, server_info = next(iter(status.items()))
            embed = Embed(title=f":mag_right: Статус {server_name}", color=server_info['color'])
            embed.add_field(name=f':loudspeaker: {server_info["message"]}', value='', inline=False)
            if "Перезапускается..." in server_info['message']:
                starting_message = await message.channel.send(embed=embed)
            elif "Уже перезапускается..." in server_info['message']:
                await message.channel.send(embed=embed)
                return
            else:
                sleep(5)
                if starting_message:
                    await starting_message.delete()
                embed.add_field(name=':round_pushpin: IP: dillertm.ru', value='')
                if server_info.get('port') is not None:
                    embed.add_field(name=f':electric_plug: Порт: {server_info["port"]}', value='')
                if server_info.get('core_name') is not None and server_info.get('core_version') is not None:
                    embed.add_field(name=f':cd: {server_info["core_name"]}: {server_info["core_version"]}', value='', inline=False)
                await message.channel.send(embed=embed)
    
    async def stop_server(self,  message: Message) -> Embed:
        server_status = self.ptero_control.server_stop(self.config['pterodactyl']['server_name'][message.content[6:].lower()])
        starting_message = None
        for status in server_status:
            server_name, server_info = next(iter(status.items()))
            embed = Embed(title=f":mag_right: Статус {server_name}", color=server_info['color'])
            if  "Остановка..." in server_info['message']:
                starting_message = await message.channel.send(embed=embed)
            elif "Уже остановлен" in server_info['message']:
                await message.channel.send(embed=embed)
                return
            else:
                if starting_message:
                    await starting_message.delete()
                embed.add_field(name=f':loudspeaker: {server_info["message"]}', value='')
            await message.channel.send(embed=embed)

    async def stat_server(self, message: Message) -> Embed:
        server_status = self.ptero_control.server_status(self.config['pterodactyl']['server_name'][message.content[6:].lower()])
        for status in server_status:
            server_name, server_info = next(iter(status.items()))
            embed = Embed(title=f":mag_right: Статус {server_name}", color=server_info.get('color')) # embed.add_field(name=f"Кол. игроков: {server_info["player_list"]}", value=' ')
            embed.add_field(name=f':loudspeaker: {server_info["message"]}', value='', inline=False)
            embed.add_field(name=':round_pushpin: IP: dillertm.ru', value='')
            embed.add_field(name=f':electric_plug: Порт: {server_info.get("port")}', value='')
            embed.add_field(name=f':cd: {server_info.get("core_name")}: {server_info.get("core_version")}', value='', inline=False)
            await message.channel.send(embed=embed)

    async def stat_all_servers(self, message: Message) -> Embed:
        server_statuses = self.ptero_control.stat_all()
        embed = Embed(title=":mag_right: Статус всех серверов!", color=Colour.from_rgb(0, 0, 0))
        for status in server_statuses.items():
            server_name, server_status = status
            embed.add_field(name=f':white_circle:  {server_name}', value=f':loudspeaker: {server_status["message"]}', inline=False)
        await message.channel.send(embed=embed)
    
    async def send_bad_word_warning(self, message: Message) -> Embed:
        embed = Embed(title='Не ругайся матом!',
                        description='Ругаться это плохо! -3 репутации',
                        color=Colour.from_rgb(178,34,34))
        await message.channel.send(embed=embed)
    
    async def wrong_command(self,  message: Message) -> Embed:
        embed = Embed(title='Неправильная команда',
                      description='Взгляните на доступные команды с помощью команды ?help',
                      color=Colour.from_rgb(178,34,34))
        await message.channel.send(embed=embed)
        await self.help(message)

    async def on_message(self, message: Message) ->  None:
        create_task(self.logs(message.content, message.channel, message.author, message.embeds))
        create_task(self.names(message))

        if any(word in message.content.lower() for word in self.bad_words['bad_words']):
            create_task(self.send_bad_word_warning(message))

        elif message.content.startswith("?"):
            try:
                command = message.content[1:].split()[0].lower()
                if command == "help":
                    create_task(self.help(message))
                elif command in ["start", "stat", "stop", "restart"]:
                    server_name = message.content[len(command) + 2:].lower()
                    if server_name not in self.config['pterodactyl']['server_name']:
                        embed = Embed(title="Неверный сервер или его не существует!",
                                      color=Colour.from_rgb(178,34,34))
                        await message.channel.send(embed=embed)
                        return
                    if command == "start":
                        create_task(self.start_server(message))
                    elif command == "restart":
                        create_task(self.restart_server(message))
                    elif command == "stop":
                        create_task(self.stop_server(message))
                    elif command == "stat":
                        if server_name == "all":
                            create_task(self.stat_all_servers(message))
                        else:
                            create_task(self.stat_server(message))
                else:
                    create_task(self.wrong_command(message))
            except IndexError:
                await self.wrong_command(message)