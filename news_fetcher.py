"""
News Fetcher Module
Fetches news from NewsAPI.ai and CryptoCompare API
"""
import os
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from cache_manager import CacheManager


class NewsFetcher:
    def __init__(self, use_cache: bool = True):
        self.news_api_key = os.getenv('NEWS_API_AI')
        self.crypto_api_key = os.getenv('CRYPTOCOMPARE_API_KEY')
        
        if not self.news_api_key or not self.crypto_api_key:
            raise ValueError("Missing API keys. Please check your .env file.")
        
        # Initialize cache manager
        self.use_cache = use_cache
        self.cache = CacheManager() if use_cache else None
    
    def fetch_interstellar_news(self, max_articles: int = 5) -> List[Dict]:
        """
        Fetch news about Interstellar Object 3I/ATLAS from NewsAPI.ai
        """
        print("🔍 Fetching Interstellar Object 3I/ATLAS news...")
        
        # Check cache first
        if self.use_cache and self.cache:
            cached = self.cache.get_cached_articles('Interstellar', max_articles)
            if cached:
                return cached
        
        # Try multiple search queries to get more results
        search_queries = [
            'interstellar object',
            'interstellar visitor',
            '3I/ATLAS',
            'interstellar comet'
        ]
        
        all_articles = []
        seen_urls = set()
        
        for query in search_queries:
            if len(all_articles) >= max_articles:
                break
                
            try:
                response = requests.get(
                    "https://newsapi.ai/api/v1/article/getArticles",
                    params={
                        'apiKey': self.news_api_key,
                        'keyword': query,
                        'articlesPage': 1,
                        'articlesCount': max_articles,
                        'resultType': 'articles'
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Parse response based on NewsAPI.ai structure
                    if 'articles' in data and 'results' in data['articles']:
                        for article in data['articles']['results']:
                            # Avoid duplicates
                            url = article.get('url', '')
                            if url and url not in seen_urls:
                                seen_urls.add(url)
                                all_articles.append({
                                    'title': article.get('title', 'No title'),
                                    'description': article.get('body', article.get('description', 'No description'))[:500],
                                    'url': url,
                                    'source': article.get('source', {}).get('title', 'Unknown'),
                                    'published_at': article.get('dateTime', article.get('date', '')),
                                    'topic': 'Interstellar Object 3I/ATLAS'
                                })
                                
                                if len(all_articles) >= max_articles:
                                    break
                    
            except Exception as e:
                print(f"⚠️ NewsAPI.ai error for query '{query}': {e}")
                continue
        
        if all_articles:
            articles = all_articles[:max_articles]
            print(f"✅ Found {len(articles)} Interstellar news articles")
            
            # Cache the results
            if self.use_cache and self.cache:
                self.cache.cache_articles('Interstellar', max_articles, articles)
            
            return articles
        
        # Fallback: Return sample data if API fails
        print("ℹ️ Using fallback data for Interstellar news")
        return self._get_fallback_interstellar_news()
    
    def fetch_crypto_news(self, max_articles: int = 10) -> List[Dict]:
        """
        Fetch latest crypto market news from CryptoCompare
        """
        print("🔍 Fetching crypto market news...")
        
        # Check cache first
        if self.use_cache and self.cache:
            cached = self.cache.get_cached_articles('Crypto', max_articles)
            if cached:
                return cached
        
        url = "https://min-api.cryptocompare.com/data/v2/news/"
        
        params = {
            'api_key': self.crypto_api_key,
            'lang': 'EN',
            'sortOrder': 'latest'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Type') == 100 and 'Data' in data:
                articles = []
                for item in data['Data'][:max_articles]:
                    articles.append({
                        'title': item.get('title', 'No title'),
                        'description': item.get('body', 'No description')[:500],
                        'url': item.get('url', item.get('guid', '')),
                        'source': item.get('source', 'Unknown'),
                        'published_at': datetime.fromtimestamp(
                            item.get('published_on', 0)
                        ).strftime('%Y-%m-%d %H:%M:%S'),
                        'categories': item.get('categories', ''),
                        'topic': 'Crypto Markets'
                    })
                
                print(f"✅ Found {len(articles)} crypto news articles")
                
                # Cache the results
                if self.use_cache and self.cache:
                    self.cache.cache_articles('Crypto', max_articles, articles)
                
                return articles
            else:
                print(f"⚠️ Unexpected response format from CryptoCompare")
                return self._get_fallback_crypto_news()
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching crypto news: {e}")
            return self._get_fallback_crypto_news()
    
    def _get_fallback_interstellar_news(self) -> List[Dict]:
        """Fallback data for Interstellar Object 3I/ATLAS"""
        return [
            {
                'title': 'Interstellar Comet 3I/ATLAS: Latest Observations',
                'description': 'Recent observations of interstellar object 3I/ATLAS reveal fascinating details about its composition and trajectory through our solar system.',
                'url': 'https://example.com/interstellar-news',
                'source': 'Space News Network',
                'published_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'topic': 'Interstellar Object 3I/ATLAS'
            }
        ]
    
    def _get_fallback_crypto_news(self) -> List[Dict]:
        """Fallback data for crypto markets"""
        return [
            {
                'title': 'Crypto Markets Show Volatility',
                'description': 'Major cryptocurrencies experience price fluctuations as market sentiment shifts amid regulatory developments.',
                'url': 'https://example.com/crypto-news',
                'source': 'Crypto News',
                'published_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'categories': 'Market Analysis',
                'topic': 'Crypto Markets'
            }
        ]
