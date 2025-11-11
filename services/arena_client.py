"""Arena Relay Bot client for Memora-English."""
import aiohttp
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ArenaClient:
    """Client for interacting with Arena Relay Bot."""
    
    def __init__(self, arena_url: str, bot_name: str = "Memora-English"):
        """
        Initialize Arena client.
        
        Args:
            arena_url: Base URL of Arena Relay Bot (e.g., http://arena-relay-bot:8000)
            bot_name: Name of this bot for arena messages
        """
        self.arena_url = arena_url.rstrip('/')
        self.bot_name = bot_name
        logger.info(f"Arena client initialized: {self.arena_url}")
    
    async def say(self, text: str) -> bool:
        """
        Send message to Arena Relay Bot for publication.
        
        Args:
            text: Message text to send
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.arena_url}/say",
                    json={
                        "bot_name": self.bot_name,
                        "text": text
                    },
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        logger.info(f"✅ Message sent to arena: {text[:50]}...")
                        return True
                    else:
                        logger.error(f"❌ Arena returned status {response.status}")
                        return False
                        
        except aiohttp.ClientError as e:
            logger.error(f"❌ Network error sending to arena: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error sending to arena: {e}")
            return False
    
    async def register(self, webhook_url: Optional[str] = None) -> bool:
        """
        Register bot in Arena Relay Bot.
        
        Args:
            webhook_url: Webhook URL to receive messages from other bots (optional)
            
        Returns:
            True if registration successful, False otherwise
        """
        if not webhook_url:
            logger.info("No webhook URL provided - skipping arena registration")
            return True
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.arena_url}/register",
                    json={
                        "bot_name": self.bot_name,
                        "webhook_url": webhook_url
                    },
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"✅ Registered in arena: {result.get('message')}")
                        return True
                    else:
                        logger.error(f"❌ Arena registration failed with status {response.status}")
                        return False
                        
        except aiohttp.ClientError as e:
            logger.error(f"❌ Network error during arena registration: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error during arena registration: {e}")
            return False
    
    async def check_health(self) -> bool:
        """
        Check if Arena Relay Bot is available.
        
        Returns:
            True if arena is healthy, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.arena_url}/health",
                    timeout=aiohttp.ClientTimeout(total=3)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"✅ Arena health check passed: {data.get('status')}")
                        return True
                    else:
                        logger.warning(f"⚠️  Arena health check returned {response.status}")
                        return False
                        
        except Exception as e:
            logger.warning(f"⚠️  Arena health check failed: {e}")
            return False

