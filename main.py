#!/usr/bin/env python3
"""
News Bot - Main Orchestrator
Fetches news about Interstellar Objects and Crypto Markets,
analyzes sentiment using LLM, and sends to Discord
"""
import os
import sys
import asyncio
from dotenv import load_dotenv
from datetime import datetime

from news_fetcher import NewsFetcher
from llm_analyzer import LLMAnalyzer
from discord_bot import NewsBot


class NewscasterBot:
    def __init__(self):
        print("=" * 60)
        print("🤖 NEWSCASTER BOT INITIALIZING")
        print("=" * 60)
        
        # Load environment variables
        load_dotenv()
        
        # Initialize components
        try:
            self.news_fetcher = NewsFetcher(use_cache=True)
            self.llm_analyzer = LLMAnalyzer(use_cache=True)
            self.discord_bot = NewsBot()
            print("✅ All components initialized successfully")
            
            # Clean up old cache on startup
            from cache_manager import CacheManager
            cache = CacheManager()
            cache.cleanup_old_cache(days=7)
        except Exception as e:
            print(f"❌ Initialization error: {e}")
            sys.exit(1)
    
    async def fetch_and_send_news(self):
        """
        Main workflow: Fetch news, analyze, and send to Discord
        """
        print("\n" + "=" * 60)
        print(f"📰 NEWS DIGEST - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # 1. Fetch Interstellar Object news
            print("\n🌌 TOPIC 1: Interstellar Object 3I/ATLAS")
            print("-" * 60)
            interstellar_articles = self.news_fetcher.fetch_interstellar_news(max_articles=10)
            
            if interstellar_articles:
                # Analyze with LLM
                interstellar_analysis = self.llm_analyzer.analyze_news_batch(
                    interstellar_articles, 
                    "Interstellar Object 3I/ATLAS"
                )
                
                # Generate Discord message
                interstellar_message = self.llm_analyzer.generate_discord_message(
                    "Interstellar Object 3I/ATLAS",
                    interstellar_articles,
                    interstellar_analysis
                )
                
                # Send to Discord
                await self.discord_bot.send_message(interstellar_message)
                
                # Small delay between messages
                await asyncio.sleep(2)
            
            # 2. Fetch Crypto Market news
            print("\n💰 TOPIC 2: Crypto Markets")
            print("-" * 60)
            crypto_articles = self.news_fetcher.fetch_crypto_news(max_articles=10)
            
            if crypto_articles:
                # Analyze with LLM
                crypto_analysis = self.llm_analyzer.analyze_news_batch(
                    crypto_articles,
                    "Crypto Markets"
                )
                
                # Generate Discord message
                crypto_message = self.llm_analyzer.generate_discord_message(
                    "Crypto Markets",
                    crypto_articles,
                    crypto_analysis
                )
                
                # Send to Discord
                await self.discord_bot.send_message(crypto_message)
            
            print("\n✅ News digest completed successfully!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error during news processing: {e}")
            import traceback
            traceback.print_exc()
    
    async def run_once(self):
        """
        Run the bot once (fetch and send news immediately)
        """
        print("\n🎯 Running in SINGLE-RUN mode")
        
        # Wait for bot to be ready
        await self.discord_bot.bot.wait_until_ready()
        
        # Fetch and send news
        await self.fetch_and_send_news()
        
        print("\n✅ Single run completed. Bot will continue listening for commands.")
        print("💡 Use Ctrl+C to stop the bot\n")
    
    async def start_with_schedule(self):
        """
        Start the bot with scheduled news updates
        """
        print("\n⏰ Running in SCHEDULED mode")
        print("📅 News will be fetched and sent every 6 hours")
        
        # Wait for bot to be ready
        await self.discord_bot.bot.wait_until_ready()
        
        # Initial run
        await self.fetch_and_send_news()
        
        # Schedule periodic updates (every 6 hours)
        while not self.discord_bot.bot.is_closed():
            await asyncio.sleep(21600)  # 6 hours = 21600 seconds
            await self.fetch_and_send_news()
    
    def run(self, mode='once'):
        """
        Run the bot
        
        Args:
            mode: 'once' for single run, 'schedule' for periodic updates
        """
        async def main():
            # Start the Discord bot in the background
            bot_task = asyncio.create_task(self.discord_bot.bot.start(self.discord_bot.token))
            
            # Run the news fetching task
            if mode == 'schedule':
                news_task = asyncio.create_task(self.start_with_schedule())
            else:
                news_task = asyncio.create_task(self.run_once())
            
            # Wait for tasks
            try:
                await asyncio.gather(bot_task, news_task)
            except KeyboardInterrupt:
                print("\n\n👋 Shutting down bot...")
                await self.discord_bot.close()
        
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n👋 Bot stopped by user")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Newscaster Bot - Fetch and analyze news')
    parser.add_argument(
        '--mode',
        choices=['once', 'schedule'],
        default='once',
        help='Run mode: "once" for single run, "schedule" for periodic updates (default: once)'
    )
    
    args = parser.parse_args()
    
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🤖 NEWSCASTER BOT v1.0                     ║
║                                                          ║
║  Topics: Interstellar Objects & Crypto Markets          ║
║  Powered by: OpenRouter LLM + NewsAPI + CryptoCompare   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Create and run bot
    bot = NewscasterBot()
    bot.run(mode=args.mode)


if __name__ == "__main__":
    main()
