import requests


print("Performing auto-update...")

url = 'https://raw.githubusercontent.com/Braslerl/Economy-Bot-Discord/main/Discord_Economy_Bot.py'
r = requests.get(url, allow_redirects=True)

open('Discord_Economy_Bot.py', 'wb').write(r.content)


print("Finished, you can close this now.")
