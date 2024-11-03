"""
Falcon - Advanced Open Source Intelligence Framework
Version: 1.0
"""

import asyncio
import aiohttp
import json
import time
import argparse
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import logging
import yaml
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.markdown import Markdown
import tweepy
import praw
from github import Github
import linkedin_api
from bs4 import BeautifulSoup
import shodan
import requests
import dns.resolver
import whois
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import re
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import exifread
from geopy.geocoders import Nominatim
from fastapi import FastAPI
import uvicorn

@dataclass
class PlatformData:
    """Data structure for platform-specific information"""
    platform_name: str
    user_data: Dict[str, Any]
    metadata: Dict[str, Any]
    raw_data: Dict[str, Any]
    timestamp: datetime

class FalconCore:
    """Core functionality for the Falcon OSINT Framework"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.console = Console()
        self.initialize_logging()
        self.load_configuration(config_path)
        self.initialize_apis()
        self.setup_database()
        self.setup_web_driver()

    def initialize_logging(self):
        """Setup advanced logging configuration"""
        log_config = {
            'version': 1,
            'formatters': {
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            },
            'handlers': {
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'falcon.log',
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'formatter': 'detailed',
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'detailed',
                }
            },
            'loggers': {
                'falcon': {
                    'handlers': ['file', 'console'],
                    'level': 'INFO',
                }
            }
        }
        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger('falcon')

    def load_configuration(self, config_path: str):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            self.create_default_configuration(config_path)
            self.logger.warning(f"Created default configuration at {config_path}")

    async def gather_social_media_data(self, username: str) -> Dict[str, PlatformData]:
        """Gather comprehensive social media data"""
        platforms = {
            'twitter': self.gather_twitter_data,
            'github': self.gather_github_data,
            'reddit': self.gather_reddit_data,
            'linkedin': self.gather_linkedin_data,
            'instagram': self.gather_instagram_data,
            'facebook': self.gather_facebook_data,
            'tiktok': self.gather_tiktok_data,
            'youtube': self.gather_youtube_data,
            'telegram': self.gather_telegram_data,
            'discord': self.gather_discord_data
        }
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for platform, func in platforms.items():
                tasks.append(asyncio.create_task(func(username, session)))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {platform: result for platform, result in zip(platforms.keys(), results) 
                   if not isinstance(result, Exception)}

    async def gather_professional_data(self, username: str) -> Dict[str, Any]:
        """Gather professional and business-related data"""
        professional_data = {
            'linkedin_profile': await self.gather_linkedin_details(username),
            'github_projects': await self.gather_github_projects(username),
            'professional_websites': await self.find_professional_websites(username),
            'patents': await self.search_patents(username),
            'academic_papers': await self.search_academic_papers(username),
            'conference_presentations': await self.search_conferences(username)
        }
        return professional_data

    async def gather_technical_footprint(self, username: str) -> Dict[str, Any]:
        """Gather technical information and digital footprint"""
        technical_data = {
            'domains': await self.search_domain_registrations(username),
            'email_addresses': await self.discover_email_addresses(username),
            'ip_addresses': await self.gather_associated_ips(username),
            'crypto_wallets': await self.search_crypto_wallets(username),
            'technical_forums': await self.search_technical_forums(username),
            'code_contributions': await self.analyze_code_contributions(username)
        }
        return technical_data

    async def perform_security_analysis(self, username: str) -> Dict[str, Any]:
        """Perform security analysis and vulnerability assessment"""
        security_data = {
            'exposed_credentials': await self.check_password_breaches(username),
            'security_incidents': await self.search_security_incidents(username),
            'vulnerable_assets': await self.identify_vulnerable_assets(username),
            'security_mentions': await self.search_security_mentions(username)
        }
        return security_data

    def generate_comprehensive_report(self, username: str, data: Dict[str, Any]) -> str:
        """Generate detailed HTML report with visualizations"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = f"falcon_reports/{username}_{timestamp}"
        os.makedirs(report_dir, exist_ok=True)

        # Generate main HTML report
        html_report = self.create_html_report(username, data, report_dir)
        
        # Generate additional report formats
        self.generate_pdf_report(data, report_dir)
        self.generate_json_report(data, report_dir)
        self.generate_csv_report(data, report_dir)
        
        return report_dir

    async def analyze_behavioral_patterns(self, username: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze behavioral patterns and user activity"""
        patterns = {
            'activity_hours': self.analyze_activity_timing(data),
            'communication_style': self.analyze_communication_patterns(data),
            'interests': self.analyze_user_interests(data),
            'connections': self.analyze_social_connections(data),
            'influence_metrics': self.calculate_influence_metrics(data)
        }
        return patterns

    async def gather_location_intelligence(self, username: str) -> Dict[str, Any]:
        """Gather and analyze location-based intelligence"""
        location_data = {
            'mentioned_locations': await self.extract_mentioned_locations(username),
            'photo_locations': await self.analyze_photo_metadata(username),
            'frequent_locations': await self.analyze_checkins(username),
            'travel_patterns': await self.analyze_travel_patterns(username),
            'location_timeline': await self.create_location_timeline(username)
        }
        return location_data

    def visualize_data(self, data: Dict[str, Any], output_dir: str):
        """Create various visualizations of the gathered data"""
        self.create_activity_heatmap(data, output_dir)
        self.create_connection_graph(data, output_dir)
        self.create_location_map(data, output_dir)
        self.create_timeline_visualization(data, output_dir)
        self.create_word_cloud(data, output_dir)

    def export_data(self, data: Dict[str, Any], format_type: str) -> str:
        """Export data in various formats"""
        exporters = {
            'json': self.export_json,
            'csv': self.export_csv,
            'xlsx': self.export_excel,
            'pdf': self.export_pdf,
            'html': self.export_html
        }
        
        if format_type in exporters:
            return exporters[format_type](data)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")

    async def start_scan(self, username: str, scan_type: str = 'full'):
        """Main scanning function with progress tracking"""
        start_time = time.time()
        
        with Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task(f"[cyan]Scanning {username}...", total=100)
            
            # Gather all data types
            social_data = await self.gather_social_media_data(username)
            progress.update(task, advance=20)
            
            professional_data = await self.gather_professional_data(username)
            progress.update(task, advance=20)
            
            technical_data = await self.gather_technical_footprint(username)
            progress.update(task, advance=20)
            
            security_data = await self.perform_security_analysis(username)
            progress.update(task, advance=20)
            
            location_data = await self.gather_location_intelligence(username)
            progress.update(task, advance=20)

            # Compile all data
            complete_data = {
                'social_media': social_data,
                'professional': professional_data,
                'technical': technical_data,
                'security': security_data,
                'location': location_data,
                'metadata': {
                    'scan_time': time.time() - start_time,
                    'timestamp': datetime.now().isoformat(),
                    'scan_type': scan_type,
                    'falcon_version': '3.0'
                }
            }

            # Generate reports
            report_dir = self.generate_comprehensive_report(username, complete_data)
            
            return report_dir, complete_data

def main():
    parser = argparse.ArgumentParser(
        description='Falcon - Advanced Open Source Intelligence Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-u', '--username', required=True, help='Target username')
    parser.add_argument('-t', '--type', choices=['full', 'quick', 'stealth'], 
                       default='full', help='Scan type')
    parser.add_argument('-o', '--output', choices=['all', 'json', 'pdf', 'html'],
                       default='all', help='Output format')
    parser.add_argument('-c', '--config', default='config.yaml', 
                       help='Path to configuration file')
    parser.add_argument('--api', action='store_true', 
                       help='Start API server instead of CLI mode')
    
    args = parser.parse_args()
    
    # Initialize Falcon
    falcon = FalconCore(config_path=args.config)
    
    if args.api:
        # Start API server
        app = FastAPI(title="Falcon OSINT API", version="3.0")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # Run CLI mode
        try:
            report_dir, data = asyncio.run(falcon.start_scan(args.username, args.type))
            falcon.console.print(f"\n[bold green]Scan complete! Reports saved to: {report_dir}[/bold green]")
        except Exception as e:
            falcon.console.print(f"\n[bold red]Error during scan: {str(e)}[/bold red]")
            sys.exit(1)

if __name__ == "__main__":
    main()
