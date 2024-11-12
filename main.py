import shodan
import whois
from googlesearch import search
import requests
import argparse
import json
from datetime import datetime

class FalconOSINT:
    def __init__(self):
        # Shodan API key (replace with your own key)
        self.shodan_key = 'pHHlgpFt8Ka3Stb5UlTxcaEwciOeF2QM'
        self.shodan_client = shodan.Shodan(self.shodan_key)

        # User-Agent for HTTP requests
        self.headers = {'User-Agent': 'Mozilla/5.0 (Falcon-OSINT/2.0)'}

        # Platforms for username checks
        self.platforms = {
            'GitHub': 'https://github.com/{}',
            'Twitter': 'https://twitter.com/{}',
            'Reddit': 'https://reddit.com/user/{}',
            'LinkedIn': 'https://linkedin.com/in/{}',
            'Instagram': 'https://instagram.com/{}'
        }

    def check_username(self, platform, url_template, username):
        """Check if the username exists on a specific platform."""
        try:
            url = url_template.format(username)
            response = requests.get(url, headers=self.headers, timeout=10)
            return {
                'platform': platform,
                'url': url,
                'exists': response.status_code == 200
            }
        except Exception as e:
            return {'platform': platform, 'error': str(e)}

    def check_shodan(self, ip):
        """IP analysis using Shodan Python package."""
        try:
            host_info = self.shodan_client.host(ip)
            return {
                'ip': ip,
                'hostnames': host_info.get('hostnames', []),
                'ports': host_info.get('ports', []),
                'os': host_info.get('os'),
                'vulns': host_info.get('vulns', []),
                'data': host_info.get('data', [])
            }
        except shodan.APIError as e:
            return {'error': str(e)}

    def check_whois(self, domain):
        """Domain WHOIS lookup using python-whois."""
        try:
            domain_info = whois.whois(domain)
            return {
                'domain': domain,
                'registrar': domain_info.registrar,
                'creation_date': str(domain_info.creation_date),
                'expiration_date': str(domain_info.expiration_date),
                'emails': domain_info.emails,
                'name_servers': domain_info.name_servers
            }
        except Exception as e:
            return {'error': str(e)}

    def google_dorking(self, query):
        """Basic Google dorking using googlesearch-python."""
        try:
            results = list(search(query, num_results=5))
            return {'query': query, 'results': results}
        except Exception as e:
            return {'error': str(e)}

    def analyze(self, username, ip=None, domain=None):
        print(f"\n[+] Starting analysis for username: {username}")
        results = {'username': username, 'timestamp': datetime.now().isoformat()}
        
        # Username checks on common platforms
        platform_results = []
        for platform, url_template in self.platforms.items():
            result = self.check_username(platform, url_template, username)
            platform_results.append(result)

        results['platform_checks'] = platform_results

        # Shodan IP analysis
        if ip:
            results['shodan'] = self.check_shodan(ip)

        # WHOIS domain analysis
        if domain:
            results['whois'] = self.check_whois(domain)

        # Google dorking
        dork_query = f"site:{username}.com"
        results['google_dorking'] = self.google_dorking(dork_query)

        return results

    def export_results(self, data, format='json'):
        filename = f"falcon_report_{data['username']}.{format}"
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        print(f"[+] Results exported to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Falcon OSINT Analyzer with Shodan, WHOIS, and Google Dorking')
    parser.add_argument('username', help='Username to analyze')
    parser.add_argument('--ip', help='IP address for Shodan analysis (optional)')
    parser.add_argument('--domain', help='Domain for WHOIS lookup (optional)')
    parser.add_argument('--format', choices=['json'], default='json', help='Export format (default: json)')
    args = parser.parse_args()

    analyzer = FalconOSINT()
    try:
        results = analyzer.analyze(args.username, args.ip, args.domain)
        analyzer.export_results(results, args.format)
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {str(e)}")

if __name__ == "__main__":
    exit(main())
