"""
LLM Analyzer Module
Uses OpenRouter API to analyze news sentiment and generate summaries
"""
import os
import json
from typing import List, Dict
from openai import OpenAI
from cache_manager import CacheManager


class LLMAnalyzer:
    def __init__(self, use_cache: bool = True):
        # Try ROUTELLM first, fallback to OpenRouter
        self.api_key = os.getenv('ROUTELLM_API_KEY') or os.getenv('OPENROUTER_API_KEY')
        self.base_url = os.getenv('ROUTELLM_ENDPOINT') or os.getenv('OPENROUTER_BASE_URL')
        self.model = os.getenv('ROUTELLM_MODEL') or os.getenv('OPENROUTER_MODEL')
        
        if not all([self.api_key, self.base_url, self.model]):
            raise ValueError("Missing LLM configuration. Please check your .env file.")
        
        # Determine which service we're using
        if os.getenv('ROUTELLM_API_KEY'):
            self.service = "ROUTELLM"
            print(f"🤖 Using ROUTELLM with model: {self.model}")
        else:
            self.service = "OpenRouter"
            print(f"🤖 Using OpenRouter with model: {self.model}")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # Initialize cache manager
        self.use_cache = use_cache
        self.cache = CacheManager() if use_cache else None
    
    def analyze_news_batch(self, articles: List[Dict], topic: str) -> Dict:
        """
        Analyze a batch of news articles for sentiment and generate a summary
        """
        print(f"🤖 Analyzing {len(articles)} articles about {topic}...")
        
        # Check cache first
        if self.use_cache and self.cache:
            cached_analysis = self.cache.get_cached_analysis(articles, topic)
            if cached_analysis:
                return cached_analysis
        
        # Prepare articles for analysis
        articles_text = self._format_articles_for_analysis(articles)
        
        prompt = f"""You are a professional news analyst. Analyze the following news articles about {topic}.

ARTICLES:
{articles_text}

Please provide:
1. **Overall Sentiment**: Classify as POSITIVE, NEGATIVE, NEUTRAL, or MIXED with a brief explanation
2. **Key Insights**: List 3-5 most important insights from these articles
3. **Executive Summary**: A concise 2-3 sentence summary highlighting the most critical information
4. **Trending Themes**: Identify main themes or patterns across the articles

Format your response as JSON with the following structure:
{{
    "sentiment": "POSITIVE/NEGATIVE/NEUTRAL/MIXED",
    "sentiment_explanation": "Brief explanation of the sentiment",
    "key_insights": ["insight 1", "insight 2", "insight 3"],
    "executive_summary": "2-3 sentence summary",
    "trending_themes": ["theme 1", "theme 2", "theme 3"]
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert news analyst specializing in sentiment analysis and summarization. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                # Extract JSON from markdown code blocks if present
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                analysis = json.loads(content)
                print(f"✅ Successfully analyzed {topic} news")
                
                # Cache the analysis
                if self.use_cache and self.cache:
                    self.cache.cache_analysis(articles, topic, analysis)
                
                return analysis
                
            except json.JSONDecodeError:
                print(f"⚠️ Failed to parse JSON response, using text format")
                analysis = self._parse_text_response(content)
                
                # Cache even non-JSON responses
                if self.use_cache and self.cache:
                    self.cache.cache_analysis(articles, topic, analysis)
                
                return analysis
                
        except Exception as e:
            print(f"❌ Error during LLM analysis: {e}")
            return self._get_fallback_analysis(topic)
    
    def _format_articles_for_analysis(self, articles: List[Dict]) -> str:
        """Format articles into a readable text block"""
        formatted = []
        for i, article in enumerate(articles, 1):
            formatted.append(f"""
Article {i}:
Title: {article['title']}
Source: {article['source']}
Published: {article['published_at']}
Content: {article['description'][:400]}...
URL: {article['url']}
---""")
        return "\n".join(formatted)
    
    def _parse_text_response(self, content: str) -> Dict:
        """Parse text response when JSON parsing fails"""
        return {
            "sentiment": "MIXED",
            "sentiment_explanation": "Analysis completed",
            "key_insights": [content[:200]],
            "executive_summary": content[:300],
            "trending_themes": ["Market Analysis"]
        }
    
    def _get_fallback_analysis(self, topic: str) -> Dict:
        """Fallback analysis when LLM fails"""
        return {
            "sentiment": "NEUTRAL",
            "sentiment_explanation": f"Unable to complete detailed analysis for {topic}",
            "key_insights": [
                f"Recent developments in {topic}",
                "Multiple sources reporting on the topic",
                "Ongoing developments expected"
            ],
            "executive_summary": f"Recent news about {topic} shows ongoing developments with multiple sources providing coverage.",
            "trending_themes": ["Breaking News", "Market Updates"]
        }
    
    def generate_discord_message(self, topic: str, articles: List[Dict], analysis: Dict) -> str:
        """
        Generate a formatted Discord message with news summary
        """
        # Emoji selection based on sentiment
        sentiment_emoji = {
            "POSITIVE": "📈",
            "NEGATIVE": "📉",
            "NEUTRAL": "➡️",
            "MIXED": "🔄"
        }
        
        sentiment = analysis.get('sentiment', 'NEUTRAL')
        emoji = sentiment_emoji.get(sentiment, "📰")
        
        # Build the message
        message = f"""
╔══════════════════════════════════════╗
        **{emoji} {topic.upper()} NEWS DIGEST {emoji}**
╚══════════════════════════════════════╝

**📊 Sentiment Analysis:** {sentiment}
_{analysis.get('sentiment_explanation', 'N/A')}_

**📝 Executive Summary:**
{analysis.get('executive_summary', 'No summary available')}

**💡 Key Insights:**
"""
        
        for i, insight in enumerate(analysis.get('key_insights', [])[:5], 1):
            message += f"{i}. {insight}\n"
        
        message += f"\n**🔥 Trending Themes:**\n"
        themes = analysis.get('trending_themes', [])
        message += " • ".join(themes[:5]) if themes else "General News"
        
        message += f"\n\n**📰 Featured Articles ({len(articles)}):**\n"
        
        for i, article in enumerate(articles[:5], 1):
            message += f"""
**{i}. {article['title'][:100]}{'...' if len(article['title']) > 100 else ''}**
    📍 Source: {article['source']}
    🕒 Published: {article['published_at']}
    🔗 [Read More]({article['url']})
"""
        
        message += f"\n\n_Report generated on {self._get_timestamp()}_"
        message += "\n" + "─" * 50
        
        return message
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
