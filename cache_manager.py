"""
Cache Manager Module
Handles caching of articles and LLM analysis to reduce API costs
"""
import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path


class CacheManager:
    def __init__(self, cache_dir: str = None):
        """Initialize cache manager"""
        if cache_dir is None:
            cache_dir = os.path.join(os.path.dirname(__file__), '.cache')
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Cache file paths
        self.articles_cache = self.cache_dir / 'articles_cache.json'
        self.analysis_cache = self.cache_dir / 'analysis_cache.json'
        self.sent_articles = self.cache_dir / 'sent_articles.json'
        
        # Cache expiry (in hours)
        self.article_cache_expiry = 24  # Articles valid for 24 hours
        self.analysis_cache_expiry = 24  # Analysis valid for 24 hours
        
        print(f"📂 Cache directory: {self.cache_dir}")
    
    def _load_cache(self, cache_file: Path) -> Dict:
        """Load cache from file"""
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading cache {cache_file.name}: {e}")
                return {}
        return {}
    
    def _save_cache(self, cache_file: Path, data: Dict):
        """Save cache to file"""
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving cache {cache_file.name}: {e}")
    
    def _is_expired(self, timestamp: str, expiry_hours: int) -> bool:
        """Check if cache entry is expired"""
        try:
            cached_time = datetime.fromisoformat(timestamp)
            expiry_time = cached_time + timedelta(hours=expiry_hours)
            return datetime.now() > expiry_time
        except:
            return True
    
    def _generate_cache_key(self, topic: str, max_articles: int) -> str:
        """Generate cache key for articles"""
        key = f"{topic}_{max_articles}_{datetime.now().strftime('%Y-%m-%d')}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def get_cached_articles(self, topic: str, max_articles: int) -> Optional[List[Dict]]:
        """Get cached articles if available and not expired"""
        cache_key = self._generate_cache_key(topic, max_articles)
        cache = self._load_cache(self.articles_cache)
        
        if cache_key in cache:
            entry = cache[cache_key]
            if not self._is_expired(entry['timestamp'], self.article_cache_expiry):
                print(f"✅ Using cached articles for {topic} (cached at {entry['timestamp']})")
                return entry['articles']
            else:
                print(f"⏰ Cache expired for {topic}")
        
        return None
    
    def cache_articles(self, topic: str, max_articles: int, articles: List[Dict]):
        """Cache fetched articles"""
        cache_key = self._generate_cache_key(topic, max_articles)
        cache = self._load_cache(self.articles_cache)
        
        cache[cache_key] = {
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'articles': articles
        }
        
        self._save_cache(self.articles_cache, cache)
        print(f"💾 Cached {len(articles)} articles for {topic}")
    
    def get_cached_analysis(self, articles: List[Dict], topic: str) -> Optional[Dict]:
        """Get cached LLM analysis if available"""
        # Create a hash of article URLs to identify this specific set
        article_urls = sorted([a['url'] for a in articles])
        cache_key = hashlib.md5(''.join(article_urls).encode()).hexdigest()
        
        cache = self._load_cache(self.analysis_cache)
        
        if cache_key in cache:
            entry = cache[cache_key]
            if not self._is_expired(entry['timestamp'], self.analysis_cache_expiry):
                print(f"✅ Using cached analysis for {topic} (saves LLM tokens!)")
                return entry['analysis']
            else:
                print(f"⏰ Analysis cache expired for {topic}")
        
        return None
    
    def cache_analysis(self, articles: List[Dict], topic: str, analysis: Dict):
        """Cache LLM analysis"""
        article_urls = sorted([a['url'] for a in articles])
        cache_key = hashlib.md5(''.join(article_urls).encode()).hexdigest()
        
        cache = self._load_cache(self.analysis_cache)
        
        cache[cache_key] = {
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'article_count': len(articles),
            'analysis': analysis
        }
        
        self._save_cache(self.analysis_cache, cache)
        print(f"💾 Cached LLM analysis for {topic} (saves tokens!)")
    
    def is_article_sent(self, article_url: str) -> bool:
        """Check if article was already sent to Discord"""
        sent = self._load_cache(self.sent_articles)
        return article_url in sent
    
    def mark_article_sent(self, article_url: str, topic: str):
        """Mark article as sent to Discord"""
        sent = self._load_cache(self.sent_articles)
        sent[article_url] = {
            'topic': topic,
            'sent_at': datetime.now().isoformat()
        }
        self._save_cache(self.sent_articles, sent)
    
    def filter_new_articles(self, articles: List[Dict]) -> List[Dict]:
        """Filter out articles that were already sent"""
        new_articles = [a for a in articles if not self.is_article_sent(a['url'])]
        
        filtered_count = len(articles) - len(new_articles)
        if filtered_count > 0:
            print(f"🔍 Filtered out {filtered_count} previously sent articles")
        
        return new_articles
    
    def mark_articles_sent(self, articles: List[Dict], topic: str):
        """Mark multiple articles as sent"""
        for article in articles:
            self.mark_article_sent(article['url'], topic)
        
        if articles:
            print(f"✅ Marked {len(articles)} articles as sent for {topic}")
    
    def cleanup_old_cache(self, days: int = 7):
        """Clean up cache entries older than specified days"""
        cleaned = 0
        
        # Clean article cache
        cache = self._load_cache(self.articles_cache)
        new_cache = {}
        for key, entry in cache.items():
            if not self._is_expired(entry['timestamp'], days * 24):
                new_cache[key] = entry
            else:
                cleaned += 1
        
        if cleaned > 0:
            self._save_cache(self.articles_cache, new_cache)
        
        # Clean analysis cache
        cache = self._load_cache(self.analysis_cache)
        new_cache = {}
        analysis_cleaned = 0
        for key, entry in cache.items():
            if not self._is_expired(entry['timestamp'], days * 24):
                new_cache[key] = entry
            else:
                analysis_cleaned += 1
        
        if analysis_cleaned > 0:
            self._save_cache(self.analysis_cache, new_cache)
            cleaned += analysis_cleaned
        
        # Clean sent articles older than 30 days
        sent = self._load_cache(self.sent_articles)
        new_sent = {}
        sent_cleaned = 0
        for url, entry in sent.items():
            if not self._is_expired(entry['sent_at'], 30 * 24):
                new_sent[url] = entry
            else:
                sent_cleaned += 1
        
        if sent_cleaned > 0:
            self._save_cache(self.sent_articles, new_sent)
            cleaned += sent_cleaned
        
        if cleaned > 0:
            print(f"🧹 Cleaned up {cleaned} old cache entries")
        
        return cleaned
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        articles = self._load_cache(self.articles_cache)
        analysis = self._load_cache(self.analysis_cache)
        sent = self._load_cache(self.sent_articles)
        
        return {
            'cached_articles': len(articles),
            'cached_analyses': len(analysis),
            'sent_articles': len(sent),
            'cache_directory': str(self.cache_dir)
        }
    
    def clear_cache(self):
        """Clear all cache files"""
        for cache_file in [self.articles_cache, self.analysis_cache, self.sent_articles]:
            if cache_file.exists():
                cache_file.unlink()
        
        print("🗑️ All cache cleared")
