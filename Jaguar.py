import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Коды ANSI для цвета
WHITE = "\033[97m"
RESET = "\033[0m"

# Новый ASCII-арт
JAGUAR_ART = f"""{WHITE}
    ___  ________  ________  ___  ___  ________  ________    
   |\  \|\   __  \|\   ____\|\  \|\  \|\   __  \|\   __  \    
   \ \  \ \  \|\  \ \  \___|\ \  \\\  \ \  \|\  \ \  \|\  \   
 __ \ \  \ \   __  \ \  \  __\ \  \\\  \ \   __  \ \   _  _\  
|\  \\_\  \ \  \ \  \ \  \|\  \ \  \\\  \ \  \ \  \ \  \\  \| 
\ \________\ \__\ \__\ \_______\ \_______\ \__\ \__\ \__\\ _\ 
 \|________|\|__|\|__|\|_______|\|_______|\|__|\|__|\|__|\|__|
{RESET}"""

# База данных для поиска
SITES_DATABASE = {
    "TikTok": "https://www.tiktok.com/@{}",
    "Telegram": "https://t.me/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "WhatsApp": "https://wa.me/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "SoundCloud": "https://soundcloud.com/{}",
    "Steam": "https://steamcommunity.com/id/{}"
}

def check_site(site_name, url_template, username):
    url = url_template.format(username)
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5, verify=False)
        if resp.status_code == 200:
            return f"[+] НАЙДЕН: {site_name} -> {url}"
    except:
        pass
    return None

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(JAGUAR_ART)
    
    username = input("Введите никнейм для поиска: ").strip()
    if not username:
        return

    print(f"\n[*] Сканирование для: {username}...\n")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(check_site, name, url, username) for name, url in SITES_DATABASE.items()]
        for future in as_completed(futures):
            res = future.result()
            if res:
                print(res)
    
    print("\n[*] Поиск завершен.")
    input("\nНажмите Enter, чтобы выйти...")

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()
