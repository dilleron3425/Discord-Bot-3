from os import _exit, system
from rich.console import Console

def CLI(json_loader):
    console = Console()
    config = json_loader.json_data['config']
    logo = f'''[#a0a0a0]
          _____                                  ___
         / ____|                                |__ \\
        | |  __   ___   ___   _ __   __ _   ___    ) |
        | | |_ | / _ \ / _ \ | '__| / _` | / _ \  / /
        | |__| ||  __/| (_) || |   | (_| ||  __/ |_|
         \_____| \___| \___/ |_|    \__, | \___| (_)
                                     __/ | V{config["version"]}
                                    |___/  By: {config["created_by"]}
    [/]'''
    system("clear")
    console.print(logo)
    while True:
        try:
            console.print(f"[#a0a0a0]George?> [/]", end="")
            root_input = input()
            if root_input.lower() == "exit":
                _exit(0)
            elif root_input.lower() == "help":
                console.print(f'\n------------------------------------------------')
                console.print(f'[#a0a0a0]George? is the third version of the Discord bot.[/]')
                console.print(f'[#a0a0a0]Version[/]: {config["version"]}')
                console.print(f'[#a0a0a0]Developer[/]: {config["created_by"]}')
                console.print(f'[#a0a0a0]GitHub[/]: {config["urls"]["url_github"]}')
                console.print(f'------------------------------------------------')
                console.print(f"    |         Command       |                Description               |\n")
                console.print(f"    | help                  | Output help window                       |")
                console.print(f"    | clear                 | Console cleaner                          |")
                console.print(f"    | exit                  | Out George?                              |\n")
            elif root_input.lower() in ["clear", "cls"]:
                system("clear")
                console.print(logo)
            else:
                if root_input == "":
                    pass
                else:
                    console.print("[bold red][Error][/bold red] Unknown command")
        except EOFError:
            _exit(0)
