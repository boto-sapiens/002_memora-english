#!/usr/bin/env python3
"""Test timezone conversion in progress"""

import asyncio
from datetime import datetime
import pytz
from config import TIMEZONE
from services.progress_service import progress_service


async def test():
    stats = await progress_service.get_progress_stats(7742103512)
    
    if stats and stats['next_review_time']:
        next_time = stats['next_review_time']
        
        print("=" * 70)
        print("TIMEZONE CONVERSION TEST")
        print("=" * 70)
        
        print(f"\n1. Next review time (from data):")
        print(f"   {next_time}")
        print(f"   Type: {type(next_time)}")
        
        print(f"\n2. Configured TIMEZONE: {TIMEZONE}")
        
        tz = pytz.timezone(TIMEZONE)
        next_time_converted = next_time.astimezone(tz)
        
        print(f"\n3. After .astimezone(tz):")
        print(f"   {next_time_converted}")
        
        formatted = next_time_converted.strftime("%d.%m.%Y %H:%M")
        print(f"\n4. Formatted string:")
        print(f"   {formatted}")
        
        print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(test())

