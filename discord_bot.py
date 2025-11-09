"""
Discord Bot Module
Handles Discord bot connection and message sending
"""
import os
import discord
from discord.ext import commands, tasks
from typing import Optional
import asyncio


class NewsBot:
    def __init__(self):
        self.token = os.getenv('DISCORD_BOT_TOKEN')
        self.channel_id = os.getenv('DISCORD_CHANNEL_ID')
        
        if not self.token:
            raise ValueError("Missing DISCORD_BOT_TOKEN in .env file")
        if not self.channel_id:
            raise ValueError("Missing DISCORD_CHANNEL_ID in .env file")
        
        # Convert channel_id to integer
        try:
            self.channel_id = int(self.channel_id)
        except ValueError:
            raise ValueError("DISCORD_CHANNEL_ID must be a valid integer")
        
        # Setup bot with intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.bot = commands.Bot(command_prefix='!news', intents=intents)
        self.setup_events()
        
    def setup_events(self):
        """Setup bot events"""
        
        @self.bot.event
        async def on_ready():
            print(f'✅ Discord Bot logged in as {self.bot.user.name} ({self.bot.user.id})')
            print(f'📡 Connected to {len(self.bot.guilds)} server(s)')
            
            # Find and display the target channel
            channel = self.bot.get_channel(self.channel_id)
            if channel:
                print(f'📢 Target channel: #{channel.name} in {channel.guild.name}')
            else:
                print(f'⚠️ Warning: Could not find channel with ID {self.channel_id}')
        
        @self.bot.event
        async def on_message(message):
            # Ignore messages from the bot itself
            if message.author == self.bot.user:
                return
            
            # Process commands
            await self.bot.process_commands(message)
        
        @self.bot.command(name='test')
        async def test_command(ctx):
            """Test command to verify bot is working"""
            await ctx.send('✅ News Bot is online and ready!')
        
        @self.bot.command(name='ping')
        async def ping_command(ctx):
            """Check bot latency"""
            latency = round(self.bot.latency * 1000)
            await ctx.send(f'🏓 Pong! Latency: {latency}ms')
    
    async def send_message(self, content: str) -> bool:
        """
        Send a message to the configured Discord channel
        
        Args:
            content: Message content to send
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            channel = self.bot.get_channel(self.channel_id)
            
            if not channel:
                print(f"❌ Could not find channel with ID {self.channel_id}")
                return False
            
            # Discord has a 2000 character limit per message
            if len(content) > 2000:
                # Split message into chunks
                chunks = self._split_message(content)
                for chunk in chunks:
                    await channel.send(chunk)
                    await asyncio.sleep(1)  # Avoid rate limiting
            else:
                await channel.send(content)
            
            print(f"✅ Message sent to #{channel.name}")
            return True
            
        except discord.errors.Forbidden:
            print("❌ Bot doesn't have permission to send messages in this channel")
            return False
        except discord.errors.HTTPException as e:
            print(f"❌ Failed to send message: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error sending message: {e}")
            return False
    
    def _split_message(self, content: str, max_length: int = 2000) -> list:
        """Split long messages into chunks"""
        chunks = []
        current_chunk = ""
        
        for line in content.split('\n'):
            if len(current_chunk) + len(line) + 1 > max_length:
                chunks.append(current_chunk)
                current_chunk = line + '\n'
            else:
                current_chunk += line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    async def send_embed(self, title: str, description: str, 
                         fields: list = None, color: int = 0x00ff00) -> bool:
        """
        Send a formatted embed message
        
        Args:
            title: Embed title
            description: Embed description
            fields: List of dict with 'name' and 'value' keys
            color: Embed color (hex)
            
        Returns:
            True if sent successfully
        """
        try:
            channel = self.bot.get_channel(self.channel_id)
            
            if not channel:
                print(f"❌ Could not find channel with ID {self.channel_id}")
                return False
            
            embed = discord.Embed(
                title=title,
                description=description[:4096],  # Discord limit
                color=color
            )
            
            if fields:
                for field in fields[:25]:  # Discord allows max 25 fields
                    embed.add_field(
                        name=field.get('name', 'Field')[:256],
                        value=field.get('value', 'No value')[:1024],
                        inline=field.get('inline', False)
                    )
            
            await channel.send(embed=embed)
            print(f"✅ Embed sent to #{channel.name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send embed: {e}")
            return False
    
    def run(self):
        """Start the Discord bot"""
        try:
            print("🚀 Starting Discord bot...")
            self.bot.run(self.token)
        except discord.errors.LoginFailure:
            print("❌ Invalid Discord bot token. Please check your .env file.")
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
    
    async def close(self):
        """Close the bot connection"""
        await self.bot.close()
