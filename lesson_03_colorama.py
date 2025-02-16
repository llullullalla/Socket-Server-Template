import colorama as cr
from colorama import Back

# cahnge this for MacOS and Linux
# cr.init()
cr.just_fix_windows_console()

print(cr.Fore.RED + "hello everyone")
print(Back.CYAN + "this is cyan")
print(cr.Style.RESET_ALL)
print("this is normal")
