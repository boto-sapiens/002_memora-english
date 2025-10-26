import asyncio
import logging
from scheduler.reminder_scheduler import start_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        logger.info("Starting scheduler...")
        asyncio.run(start_scheduler())
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")

