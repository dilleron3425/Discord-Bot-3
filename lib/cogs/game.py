from pydactyl import PterodactylClient
from requests.exceptions import HTTPError
from discord import Colour

class PterodactylControl():
    def __init__(self, json_loader):
        self.json_loader = json_loader
        self.config = self.json_loader.json_data['config']
        self.api = PterodactylClient(self.config["urls"]["game_server"], self.config["ptero_api"])
        self.no_server = {"message": f"Ошибка, не удалось найти сервер. Возможно, проблема в конфигурации сервера или у бота George?\n Пожалуйста отметьте это сообщение в {self.config['channels']['bugs']}", "color": Colour.from_rgb(0, 128, 0)}

    def handle_error(self, server_status: dict, server_name: str, server_error: Exception) -> None:
        error_messages = {
            409: "Ошибка 409, не удается обработать запрос из-за конфликта в текущем состоянии сервера.",
            500: "Ошибка 500, неисправность конфигурации сервера или запрос был отказан."
        }
        if isinstance(server_error, HTTPError):
            error_code = server_error.response.status_code
            message = error_messages.get(error_code, f"Ошибка {error_code} при извлечении данных из сервера.")
        elif isinstance(server_error, KeyError):
            message = "Ошибка, не найдена конфигурация для Pterodactyl на сервере или у бота George?"
        else:
            message = f"Не известная ошибка: {server_error}"
        message += f"\nПожалуйста отметьте это сообщение в {self.config['channels']['bugs']}"
        server_status[server_name] = {"message": message, "color": Colour.from_rgb(178,34,34)}
    
    def server_status(self, server_name: str):
        server_status = {}
        try:
            server_uuid = self.config['pterodactyl']['server_uuid'].get(server_name)
            if server_uuid:
                try:
                    server_data = self.api.client.servers.get_server_utilization(server_uuid)
                    parameters = self.api.client.servers.get_server(server_uuid)
                    core_name = parameters['relationships']['variables']['data'][3]['attributes']['name']
                    core_version = parameters['relationships']['variables']['data'][3]['attributes']['server_value']
                    port = parameters['relationships']['allocations']['data'][0]['attributes']['port']
                    server_status[server_name] = {
                        "message": 'Запущен' if server_data['current_state'] == 'running' else 'Остановлен',
                        "color": Colour.from_rgb(0, 128, 0) if server_data['current_state'] == 'running' else Colour.from_rgb(128, 128, 128),
                        "port": port,
                        "core_name": core_name,
                        "core_version": core_version
                    }
                except Exception as server_error:
                    self.handle_error(server_status, server_name, server_error)
            else:
                server_status[server_name] = self.no_server
        except Exception as server_error:
            self.handle_error(server_status, server_name, server_error)
        yield server_status

    def server_start(self, server_name):
        server_status_generator = self.server_status(server_name)
        server_status = next(server_status_generator)
        current_state = server_status[server_name]['message']
        core_name = server_status[server_name]['core_name']
        core_version = server_status[server_name]['core_version']
        port = server_status[server_name]['port']
        try:
            server_uuid = self.config['pterodactyl']['server_uuid'].get(server_name)
            if server_uuid:
                try:
                    if current_state == 'Запущен':
                        server_status[server_name] = {
                        "message": f'Уже запущен',
                        "color": Colour.from_rgb(0, 128, 0),
                        "port": port,
                        "core_name": core_name,
                        "core_version": core_version
                        }
                    else:
                        self.api.client.servers.send_power_action(server_uuid, 'start')
                        server_status[server_name] = {"message": "Запускается...", "color": Colour.from_rgb(128, 128, 128)}
                        yield server_status
                        while self.api.client.servers.get_server_utilization(server_uuid)['current_state'] != 'running':
                            self.api.client.servers.get_server_utilization(server_uuid)['current_state']
                        server_status[server_name] = {
                        "message": 'Запущен',
                        "color": Colour.from_rgb(0, 128, 0),
                        "port": port,
                        "core_name": core_name,
                        "core_version": core_version
                        }
                except Exception as server_error:
                    self.handle_error(server_status, server_name, server_error)
            else:
                server_status[server_name] = self.no_server
        except Exception as server_error:
            self.handle_error(server_status, server_name, server_error)
        yield server_status

    def server_restart(self, server_name):
        server_status_generator = self.server_status(server_name)
        server_status = next(server_status_generator)
        core_name = server_status[server_name]['core_name']
        core_version = server_status[server_name]['core_version']
        port = server_status[server_name]['port']
        try:
            server_uuid = self.config['pterodactyl']['server_uuid'].get(server_name)
            if server_uuid:
                try:
                    if self.api.client.servers.get_server_utilization(server_uuid)['current_state'] == 'starting':
                        server_status[server_name] = {"message": "Уже перезапускается...", "color": Colour.from_rgb(128, 128, 128)}
                    else:
                        self.api.client.servers.send_power_action(server_uuid, 'restart')
                        server_status[server_name] = {"message": "Перезапускается...", "color": Colour.from_rgb(128, 128, 128)}
                        yield server_status
                        while self.api.client.servers.get_server_utilization(server_uuid)['current_state'] != 'running':
                            self.api.client.servers.get_server_utilization(server_uuid)['current_state']
                        server_status[server_name] = {
                        "message": 'Запущен',
                        "color": Colour.from_rgb(0, 128, 0),
                        "port": port,
                        "core_name": core_name,
                        "core_version": core_version
                        }
                except Exception as server_error:
                    self.handle_error(server_status, server_name, server_error)
            else:
                server_status[server_name] = self.no_server
        except Exception as server_error:
            self.handle_error(server_status, server_name, server_error)
        yield server_status

    def server_stop(self, server_name):
        server_status_generator = self.server_status(server_name)
        server_status = next(server_status_generator)
        current_state = server_status[server_name]['message']
        try:
            server_uuid = self.config['pterodactyl']['server_uuid'].get(server_name)
            if server_uuid:
                try:
                    if current_state == 'Остановлен':
                        server_status[server_name] = {"message": "Уже остановлен", "color": Colour.from_rgb(128, 128, 128)}
                    else:
                        self.api.client.servers.send_power_action(server_uuid, 'stop')
                        server_status[server_name] = {"message": "Останавливается...", "color": Colour.from_rgb(0, 128, 0)}
                        yield server_status
                        while self.api.client.servers.get_server_utilization(server_uuid)['current_state'] != 'offline':
                            self.api.client.servers.get_server_utilization(server_uuid)['current_state']
                        server_status[server_name] = {"message": "Остановлен", "color": Colour.from_rgb(128, 128, 128)}
                except Exception as server_error:
                    self.handle_error(server_status, server_name, server_error)
            else:
                server_status[server_name] = self.no_server
        except Exception as server_error:
            self.handle_error(server_status, server_name, server_error)
        yield server_status

    def stat_all(self):
        server_list = self.api.client.servers.list_servers()
        server_statuses = {}
        for inner_list in server_list:
            for server in inner_list:
                server_name = server['attributes']['name']
                server_uuid = server['attributes']['uuid']
                try:
                    server_info = self.api.client.servers.get_server_utilization(server_uuid)
                    server_statuses[server_name] = {
                        "message": 'Запущен' if server_info['current_state'] == 'running' else 'Остановлен',
                        "color": Colour.from_rgb(0, 128, 0) if server_info['current_state'] == 'running' else Colour.from_rgb(128, 128, 128)
                    }  
                except HTTPError as server_error:
                    self.handle_error(server_statuses, server_name, server_error)
        return server_statuses
