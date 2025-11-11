"""
Check for expired pending cards and reset them to new status.

A pending card becomes expired if user doesn't review it within grace period:
- forgot (❌): 8 hours grace
- uncertain (🤔): 12 hours grace  
- knew (✅): 24 hours grace
"""

import asyncio
from datetime import datetime, timedelta
import pytz
import logging
from storage.json_storage import storage
from services.anki_algorithm import get_current_time

logger = logging.getLogger(__name__)

# Grace periods in seconds based on last response type
GRACE_PERIODS = {
    'forgot': 8 * 3600,      # 8 hours
    'uncertain': 12 * 3600,  # 12 hours
    'knew': 24 * 3600,       # 24 hours
    None: 24 * 3600          # Default for cards without response history
}


async def check_and_reset_expired_cards():
    """Check all pending cards and reset expired ones to new status"""
    now = get_current_time()
    logger.info(f"Checking for expired cards at {now}")
    
    # Get all users
    users = await storage.get_all_users()
    total_reset = 0
    
    for user in users:
        cards = await storage.get_user_cards(user.telegram_id)
        
        for card in cards:
            # Only check pending cards
            if card.status != 'pending':
                continue
            
            # Check if card has deadline_time
            if not card.deadline_time:
                logger.warning(f"Pending card {card.card_id} for user {user.telegram_id} has no deadline_time, skipping")
                continue
            
            # Parse deadline time
            deadline = datetime.fromisoformat(card.deadline_time)
            
            # Check if expired
            if now > deadline:
                grace_hours = GRACE_PERIODS.get(card.last_response_type, GRACE_PERIODS[None]) / 3600
                logger.info(f"Card {card.card_id} for user {user.telegram_id} expired. "
                           f"Last response: {card.last_response_type}, grace: {grace_hours}h")
                
                # Reset card to new
                card.interval_index = 0
                card.status = 'new'
                card.next_review_time = None
                card.last_reviewed = None
                card.last_response_type = None
                card.deadline_time = None
                
                await storage.save_user_card(card)
                total_reset += 1
    
    if total_reset > 0:
        logger.info(f"✅ Reset {total_reset} expired cards to new status")
    else:
        logger.debug("No expired cards found")
    
    return total_reset


async def run_expired_checker_loop(check_interval: int = 300):
    """Run expired card checker in loop"""
    logger.info(f"Starting expired card checker (interval: {check_interval}s)")
    
    while True:
        try:
            await check_and_reset_expired_cards()
        except Exception as e:
            logger.error(f"Error checking expired cards: {e}")
        
        await asyncio.sleep(check_interval)


if __name__ == "__main__":
    # For testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    asyncio.run(check_and_reset_expired_cards())

