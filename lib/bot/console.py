from os import _exit
from rich.console import Console

def console():
    console = Console()
    logo = '''[#a0a0a0]
          _____                                  ___
         / ____|                                |__ \\
        | |  __   ___   ___   _ __   __ _   ___    ) |
        | | |_ | / _ \ / _ \ | '__| / _` | / _ \  / /
        | |__| ||  __/| (_) || |   | (_| ||  __/ |_|
         \_____| \___| \___/ |_|    \__, | \___| (_)
                                     __/ | V3.2.2.0
                                    |___/  By: DillerTM
    [/]'''
    console.clear()
    console.print(logo)
    while True:
        try:
            console.print(f"[#a0a0a0]George?> [/]", end="")
            root_input = input()
            if root_input.lower() == "exit":
                _exit(0)
            elif root_input.lower() == "help":
                console.print(f'\n[#a0a0a0]George? is the third version of the Discord bot.[/]')
                console.print(f'[#a0a0a0]Version[/]: 3.2.2.0')
                console.print(f'[#a0a0a0]Developer[/]: DillerTM')
                console.print(f'[#a0a0a0]GitHub[/]: https://github.com/dilleron3425')
                console.print(f'------------------------------------------------')
                console.print(f"    | Command | Description            |")
                console.print(f"\n    | help    | Output help window     |")
                console.print(f"    | exit    | Out George?            |")
                console.print(f"    | clear   | Console cleaner        |\n")
            elif root_input.lower() == "clear":
                console.clear()
                console.print(logo)
            else:
                if root_input == "":
                    pass
                else:
                    console.print("[bold red][Error][/bold red] Unknown command")
        except EOFError:
            _exit(0)
