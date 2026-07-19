
import os
import requests
import msvcrt
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init

# Initialize colorama
init(autoreset=True)

# ANSI code for Bright White
WHITE = "\033[97m"

# ASCII Art
JAGUAR_ART = f"""{WHITE}
    ___  ________  ________  ___  ___  ________  ________    
   |\  \|\   __  \|\   ____\|\  \|\  \|\   __  \|\   __  \    
   \ \  \ \  \|\  \ \  \___|\ \  \\\  \ \  \|\  \ \  \|\  \   
 __ \ \  \ \   __  \ \  \  __\ \  \\\  \ \   __  \ \   _  _\  
|\  \\_\  \ \  \ \  \ \  \|\  \ \  \\\  \ \  \ \  \ \  \\  \| 
\ \________\ \__\ \__\ \_______\ \_______\ \__\ \__\ \__\\ _\ 
 \|________|\|__|\|__|\|_______|\|_______|\|__|\|__|\|__|\|__|
"""

# Database of sites
SITES_DATABASE = {
    "Spotify": "https://open.spotify.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Telegram": "https://t.me/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "GitHub": "https://github.com/{}",
    "Twitter/X": "https://twitter.com/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Discord": "https://discord.com/users/{}"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Keywords to detect fake positive results
NEGATIVE_KEYWORDS = ["not found", "doesn't exist", "does not exist", "page not found", "user not found", "profile not found"]

def check_site(site_name, url_template, username):
    url = url_template.format(username)
    try:
        # allow_redirects=False prevents automatic redirection to homepages
        resp = requests.get(url, headers=HEADERS, timeout=10, verify=False, allow_redirects=False)
        
        # Check if status code is 200 (Success)
        if resp.status_code == 200:
            # Check content for negative keywords
            content = resp.text.lower()
            if any(phrase in content for phrase in NEGATIVE_KEYWORDS):
                return f"{WHITE}[-] NOT FOUND: {site_name}"
            return f"{WHITE}[+] FOUND: {site_name} -> {url}"
        
        return f"{WHITE}[-] NOT FOUND: {site_name}"
        
    except:
        return f"{WHITE}[-] NOT FOUND: {site_name}"

def run_scan():
    # Clear console
    os.system('cls' if os.name == 'nt' else 'clear')
    print(JAGUAR_ART)
    
    username = input(f"{WHITE}Enter username to search: ").strip()
    if not username: return

    print(f"\n{WHITE}[*] Scanning...")
    results = []
    
    # Multithreaded execution
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_site, name, url, username): name for name, url in SITES_DATABASE.items()}
        for future in as_completed(futures):
            res = future.result()
            print(res) 
            if "[+]" in res:
                results.append(res)
    
    # Saving results
    if results:
        file_name = f"result_{username}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join([r.replace(WHITE, "") for r in results]))
        print(f"\n{WHITE}[!] Success! Results saved to {file_name}")
    
    print(f"\n{WHITE}--- Scan complete ---")

def main():
    while True:
        run_scan()
        print(f"\n{WHITE}Press [Space] to search again or any other key to exit...")
        if ord(msvcrt.getch()) != 32: 
            break

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()
