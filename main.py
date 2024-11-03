import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures
import time
from urllib.parse import urlparse
import sys
import argparse
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from fake_useragent import UserAgent

class Falcon:
    def __init__(self):
        self.console = Console()
        self.ua = UserAgent()
        self.results = {}
        
        # Common social media and platforms to check
        self.platforms = {
            'GitHub': 'https://github.com/{}',
            'Twitter': 'https://twitter.com/{}',
            'Instagram': 'https://www.instagram.com/{}',
            'Reddit': 'https://www.reddit.com/user/{}',
            'LinkedIn': 'https://www.linkedin.com/in/{}',
            'Medium': 'https://medium.com/@{}',
            'DeviantArt': 'https://www.deviantart.com/{}',
            'Pinterest': 'https://www.pinterest.com/{}',
            'Spotify': 'https://open.spotify.com/user/{}',
            'Steam': 'https://steamcommunity.com/id/{}'
        }

    def make_request(self, url):
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            return response
        except requests.RequestException:
            return None

    def extract_info(self, platform, username, response):
        info = {'exists': False, 'details': {}}
        
        if response and response.status_code == 200:
            info['exists'] = True
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Platform-specific extraction logic
            if platform == 'GitHub':
                info['details']['name'] = soup.find('span', {'itemprop': 'name'})
                info['details']['bio'] = soup.find('div', {'class': 'p-note'})
                repos = soup.find('span', {'class': 'Counter'})
                if repos:
                    info['details']['repositories'] = repos.text.strip()
                
            elif platform == 'Twitter':
                bio = soup.find('div', {'data-testid': 'UserDescription'})
                if bio:
                    info['details']['bio'] = bio.text.strip()
                    
            # Add more platform-specific extraction as needed
            
        return info

    def check_username(self, username):
        self.console.print(f"\n[bold blue]🦅 Falcon OSINT - Scanning username: {username}[/bold blue]\n")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {
                executor.submit(self.make_request, url.format(username)): (platform, url.format(username))
                for platform, url in self.platforms.items()
            }
            
            for future in concurrent.futures.as_completed(future_to_url):
                platform, url = future_to_url[future]
                response = future.result()
                info = self.extract_info(platform, username, response)
                self.results[platform] = info

    def display_results(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Platform")
        table.add_column("Status")
        table.add_column("Details")

        for platform, info in self.results.items():
            status = "✅ Found" if info['exists'] else "❌ Not Found"
            details = ""
            if info['exists'] and info['details']:
                details = ", ".join(f"{k}: {v}" for k, v in info['details'].items() if v)
            
            table.add_row(
                platform,
                status,
                details or "No additional information"
            )

        self.console.print(table)

def main():
    parser = argparse.ArgumentParser(description='Falcon OSINT - Username Reconnaissance Tool')
    parser.add_argument('username', help='Username to investigate')
    parser.add_argument('-o', '--output', help='Output results to a file')
    args = parser.parse_args()

    falcon = Falcon()
    falcon.check_username(args.username)
    falcon.display_results()

if __name__ == "__main__":
    main()
