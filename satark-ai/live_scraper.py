"""
Satark.ai - Live Scammer Database
Real-time scam intelligence from REAL cybercrime databases
Sources: 
- cybercrime.gov.in (Indian Government)
- Consumer Complaints India
- Google News RSS
- Public scam report datasets
"""

import requests
from datetime import datetime, timedelta
import json
import re
import os
from typing import List, Dict
import time
from bs4 import BeautifulSoup


class LiveScammerDB:
    """Real-time scammer database with multiple data sources"""
    
    def __init__(self):
        self.cache_file = "scam_cache.json"
        self.cache_duration = 3600  # 1 hour cache
        self.scam_data = self.load_cache()
    
    def load_cache(self) -> dict:
        """Load cached scam data if recent"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cache_time = datetime.fromisoformat(data.get('last_updated', '2020-01-01'))
                    
                    # Check if cache is still valid (within 1 hour)
                    if datetime.now() - cache_time < timedelta(seconds=self.cache_duration):
                        return data
            except Exception as e:
                pass
        
        return self.initialize_empty_db()
    
    def initialize_empty_db(self) -> dict:
        """Initialize with known scam patterns"""
        return {
            'last_updated': datetime.now().isoformat(),
            'reported_numbers': {},
            'reported_upis': {},
            'scam_keywords': [
                'digital arrest', 'cyber cell arrest', 'rbi approved loan',
                'lottery winner', 'pay now or jail', 'court summons',
                'suspended account', 'verify otp', 'customs seized',
                'income tax notice', 'legal action', 'warrant issued'
            ],
            'live_reports': [],
            'total_reports': 0
        }
    
    def save_cache(self):
        """Save current data to cache"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.scam_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Cache save failed: {e}")
    
    def fetch_google_news_scams(self) -> List[Dict]:
        """
        Fetch recent scam news from Google News
        Uses Google News RSS feed (no API key needed)
        """
        scam_reports = []
        
        try:
            # Google News RSS for scam-related queries
            queries = [
                "cyber+scam+india",
                "whatsapp+fraud+india",
                "upi+scam+india",
                "digital+arrest+scam"
            ]
            
            for query in queries:
                url = f"https://news.google.com/rss/search?q={query}+when:1d&hl=en-IN&gl=IN&ceid=IN:en"
                
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        # Parse RSS feed for titles and links
                        content = response.text
                        
                        # Extract titles (simplified parsing)
                        titles = re.findall(r'<title>(.*?)</title>', content)
                        links = re.findall(r'<link>(.*?)</link>', content)
                        
                        for i, title in enumerate(titles[1:6]):  # Skip first title (feed title)
                            if i < len(links) - 1:
                                scam_reports.append({
                                    'title': title,
                                    'link': links[i + 1],
                                    'source': 'Google News',
                                    'timestamp': datetime.now().isoformat()
                                })
                except Exception as e:
                    continue
            
            return scam_reports[:10]  # Return top 10
            
        except Exception as e:
            return []
    
    def fetch_consumer_complaints(self) -> List[Dict]:
        """
        Fetch from Indian consumer complaint forums
        Sources: Consumer Complaints India, Voxya, Complain Book
        """
        complaints = []
        
        try:
            # Source 1: Consumer Complaints India (public data)
            urls_to_scrape = [
                "https://www.consumercomplaints.in/by-company/financial-fraud",
                "https://www.consumercomplaints.in/by-company/banking-services"
            ]
            
            for url in urls_to_scrape[:1]:  # Limit to avoid rate limiting
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Find complaint titles/descriptions
                        complaint_items = soup.find_all(['div', 'article'], class_=re.compile('complaint|post', re.I), limit=5)
                        
                        for item in complaint_items:
                            title = item.find(['h2', 'h3', 'a'])
                            if title:
                                text = title.get_text(strip=True)
                                # Extract phone numbers from complaint text
                                phones = self.extract_phone_numbers(text)
                                
                                complaints.append({
                                    'title': text[:200],
                                    'source': 'Consumer Complaints India',
                                    'phones_found': phones,
                                    'timestamp': datetime.now().isoformat()
                                })
                        
                        # Small delay to be respectful
                        time.sleep(1)
                except Exception as e:
                    continue
            
            return complaints
        except Exception as e:
            return []
    
    def fetch_cybercrime_advisories(self) -> List[Dict]:
        """
        Fetch from cybercrime.gov.in and RBI advisory pages
        Real government sources for scam alerts
        """
        advisories = []
        
        try:
            # Cybercrime.gov.in advisories (if accessible)
            advisory_sources = [
                {
                    'url': 'https://cybercrime.gov.in/Webform/Whatsnew.aspx',
                    'source': 'National Cyber Crime Portal'
                },
                {
                    'url': 'https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx',
                    'source': 'RBI Press Releases'
                }
            ]
            
            for source_data in advisory_sources[:1]:  # Limit to 1 to avoid rate limiting
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    response = requests.get(source_data['url'], headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Look for advisory text containing scam keywords
                        text_elements = soup.find_all(['p', 'div', 'li'], limit=20)
                        
                        for elem in text_elements:
                            text = elem.get_text(strip=True)
                            # Check if text contains scam-related keywords
                            if any(keyword in text.lower() for keyword in ['scam', 'fraud', 'cyber', 'phishing']):
                                advisories.append({
                                    'title': text[:200],
                                    'source': source_data['source'],
                                    'url': source_data['url'],
                                    'timestamp': datetime.now().isoformat()
                                })
                        
                        time.sleep(2)  # Be respectful to government servers
                except Exception as e:
                    continue
            
            return advisories[:5]
        except Exception as e:
            return []
    
    def fetch_twitter_scam_reports(self) -> List[Dict]:
        """
        Fetch scam reports from Twitter/X public search
        Uses Nitter (Twitter frontend) for public access
        """
        reports = []
        
        try:
            # Nitter instances (public Twitter frontend)
            nitter_instances = [
                'https://nitter.net',
                'https://nitter.it',
                'https://nitter.poast.org'
            ]
            
            search_queries = [
                '#CyberScam',
                '#FraudAlert India',
                'scam phone number india'
            ]
            
            for instance in nitter_instances[:1]:  # Try first available instance
                try:
                    query = search_queries[0].replace(' ', '+').replace('#', '%23')
                    url = f"{instance}/search?f=tweets&q={query}"
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Find tweet content
                        tweets = soup.find_all('div', class_='tweet-content', limit=5)
                        
                        for tweet in tweets:
                            text = tweet.get_text(strip=True)
                            phones = self.extract_phone_numbers(text)
                            
                            if phones or any(word in text.lower() for word in ['scam', 'fraud', 'fake']):
                                reports.append({
                                    'title': text[:200],
                                    'source': 'Twitter/X',
                                    'phones_found': phones,
                                    'timestamp': datetime.now().isoformat()
                                })
                    
                    break  # Exit loop if successful
                except Exception as e:
                    continue
            
            return reports
        except Exception as e:
            return []
    
    def extract_phone_numbers(self, text: str) -> List[str]:
        """Extract Indian phone numbers from text"""
        # Indian phone patterns: +91XXXXXXXXXX, 0XXXXXXXXXX, XXXXXXXXXX
        patterns = [
            r'\+91[\s-]?\d{10}',
            r'\b0\d{10}\b',
            r'\b[6-9]\d{9}\b'
        ]
        
        numbers = []
        for pattern in patterns:
            found = re.findall(pattern, text)
            numbers.extend(found)
        
        return list(set(numbers))  # Remove duplicates
    
    def check_phone_number(self, phone: str) -> Dict:
        """Check if phone number is in reported scams"""
        # Normalize phone number
        normalized = re.sub(r'[\s\-\+]', '', phone)
        normalized = normalized[-10:]  # Get last 10 digits
        
        if normalized in self.scam_data['reported_numbers']:
            report = self.scam_data['reported_numbers'][normalized]
            return {
                'found': True,
                'reports': report['count'],
                'first_seen': report['first_seen'],
                'last_seen': report['last_seen'],
                'scam_types': report['scam_types']
            }
        
        return {'found': False}
    
    def check_upi_id(self, upi_id: str) -> Dict:
        """Check if UPI ID is in reported scams"""
        if upi_id and upi_id.lower() in self.scam_data['reported_upis']:
            report = self.scam_data['reported_upis'][upi_id.lower()]
            return {
                'found': True,
                'reports': report['count'],
                'first_seen': report['first_seen'],
                'scam_types': report['scam_types']
            }
        
        return {'found': False}
    
    def add_report(self, phone: str = None, upi_id: str = None, scam_type: str = "Unknown"):
        """Add a new scam report to the database"""
        now = datetime.now().isoformat()
        
        if phone:
            normalized = re.sub(r'[\s\-\+]', '', phone)[-10:]
            
            if normalized in self.scam_data['reported_numbers']:
                self.scam_data['reported_numbers'][normalized]['count'] += 1
                self.scam_data['reported_numbers'][normalized]['last_seen'] = now
                if scam_type not in self.scam_data['reported_numbers'][normalized]['scam_types']:
                    self.scam_data['reported_numbers'][normalized]['scam_types'].append(scam_type)
            else:
                self.scam_data['reported_numbers'][normalized] = {
                    'count': 1,
                    'first_seen': now,
                    'last_seen': now,
                    'scam_types': [scam_type]
                }
        
        if upi_id:
            upi_lower = upi_id.lower()
            if upi_lower in self.scam_data['reported_upis']:
                self.scam_data['reported_upis'][upi_lower]['count'] += 1
            else:
                self.scam_data['reported_upis'][upi_lower] = {
                    'count': 1,
                    'first_seen': now,
                    'scam_types': [scam_type]
                }
        
        self.scam_data['total_reports'] += 1
        self.save_cache()
    
    def update_database(self) -> Dict:
        """
        Update database with latest scam reports from REAL sources:
        - Google News RSS
        - Consumer Complaint Forums
        - Cybercrime.gov.in Advisories
        - Twitter/X Public Reports
        
        Returns statistics about the update
        """
        start_time = time.time()
        
        all_reports = []
        new_numbers = 0
        new_upis = 0
        
        # Source 1: Google News (Fast, reliable)
        try:
            news_reports = self.fetch_google_news_scams()
            all_reports.extend(news_reports)
            
            for report in news_reports:
                text = report.get('title', '')
                numbers = self.extract_phone_numbers(text)
                for number in numbers:
                    if number not in self.scam_data['reported_numbers']:
                        new_numbers += 1
                    self.add_report(phone=number, scam_type="News Report")
        except Exception as e:
            pass
        
        # Source 2: Consumer Complaints (Real user reports)
        try:
            complaints = self.fetch_consumer_complaints()
            all_reports.extend(complaints)
            
            for complaint in complaints:
                phones = complaint.get('phones_found', [])
                for phone in phones:
                    if phone not in self.scam_data['reported_numbers']:
                        new_numbers += 1
                    self.add_report(phone=phone, scam_type="Consumer Complaint")
        except Exception as e:
            pass
        
        # Source 3: Government Cybercrime Advisories
        try:
            advisories = self.fetch_cybercrime_advisories()
            all_reports.extend(advisories)
            
            for advisory in advisories:
                text = advisory.get('title', '')
                numbers = self.extract_phone_numbers(text)
                for number in numbers:
                    if number not in self.scam_data['reported_numbers']:
                        new_numbers += 1
                    self.add_report(phone=number, scam_type="Govt Advisory")
        except Exception as e:
            pass
        
        # Source 4: Twitter/X Reports (Real-time)
        try:
            twitter_reports = self.fetch_twitter_scam_reports()
            all_reports.extend(twitter_reports)
            
            for report in twitter_reports:
                phones = report.get('phones_found', [])
                for phone in phones:
                    if phone not in self.scam_data['reported_numbers']:
                        new_numbers += 1
                    self.add_report(phone=phone, scam_type="Social Media Report")
        except Exception as e:
            pass
        
        # Update live reports
        self.scam_data['live_reports'] = all_reports[:15]  # Store top 15
        self.scam_data['last_updated'] = datetime.now().isoformat()
        
        # Add source breakdown
        self.scam_data['sources'] = {
            'google_news': len([r for r in all_reports if r.get('source') == 'Google News']),
            'consumer_complaints': len([r for r in all_reports if r.get('source') == 'Consumer Complaints India']),
            'govt_advisory': len([r for r in all_reports if 'Cyber Crime' in r.get('source', '') or 'RBI' in r.get('source', '')]),
            'social_media': len([r for r in all_reports if r.get('source') == 'Twitter/X'])
        }
        
        # Save to cache
        self.save_cache()
        
        return {
            'success': True,
            'total_reports_fetched': len(all_reports),
            'new_numbers': new_numbers,
            'total_numbers': len(self.scam_data['reported_numbers']),
            'total_upis': len(self.scam_data['reported_upis']),
            'update_time_ms': round((time.time() - start_time) * 1000, 2),
            'last_updated': self.scam_data['last_updated'],
            'sources': self.scam_data.get('sources', {})
        }
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        now = datetime.now()
        last_update = datetime.fromisoformat(self.scam_data['last_updated'])
        hours_since_update = (now - last_update).total_seconds() / 3600
        
        return {
            'total_reports': self.scam_data['total_reports'],
            'reported_numbers': len(self.scam_data['reported_numbers']),
            'reported_upis': len(self.scam_data['reported_upis']),
            'last_updated': self.scam_data['last_updated'],
            'hours_since_update': round(hours_since_update, 1),
            'cache_valid': hours_since_update < 1.0,
            'recent_news': len(self.scam_data.get('live_reports', []))
        }
    
    def get_recent_reports(self, limit: int = 5) -> List[Dict]:
        """Get most recent scam reports"""
        return self.scam_data.get('live_reports', [])[:limit]


# Initialize global instance
live_db = LiveScammerDB()


# Convenience functions
def check_phone(phone: str) -> Dict:
    """Quick check for phone number"""
    return live_db.check_phone_number(phone)


def check_upi(upi_id: str) -> Dict:
    """Quick check for UPI ID"""
    return live_db.check_upi_id(upi_id)


def update_db() -> Dict:
    """Update the live database"""
    return live_db.update_database()


def get_db_stats() -> Dict:
    """Get database statistics"""
    return live_db.get_stats()


if __name__ == "__main__":
    # Test the live database
    print("🔄 Updating Live Scammer Database...")
    result = update_db()
    print(f"✅ Update complete!")
    print(f"   News found: {result['news_found']}")
    print(f"   Total numbers: {result['total_numbers']}")
    print(f"   Update time: {result['update_time_ms']}ms")
    
    stats = get_db_stats()
    print(f"\n📊 Database Stats:")
    print(f"   Total reports: {stats['total_reports']}")
    print(f"   Reported numbers: {stats['reported_numbers']}")
    print(f"   Last update: {stats['hours_since_update']:.1f} hours ago")
