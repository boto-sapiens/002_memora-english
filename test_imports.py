#!/usr/bin/env python3
"""
Simple test script to verify all imports work correctly
"""

import sys

def test_imports():
    """Test all module imports"""
    errors = []
    
    try:
        import config
        print("✅ config imported successfully")
    except Exception as e:
        errors.append(f"❌ config: {e}")
    
    try:
        from storage.models import User, UserCard
        print("✅ storage.models imported successfully")
    except Exception as e:
        errors.append(f"❌ storage.models: {e}")
    
    try:
        from storage.json_storage import storage
        print("✅ storage.json_storage imported successfully")
    except Exception as e:
        errors.append(f"❌ storage.json_storage: {e}")
    
    try:
        from services.anki_algorithm import calculate_next_review, get_current_time
        print("✅ services.anki_algorithm imported successfully")
    except Exception as e:
        errors.append(f"❌ services.anki_algorithm: {e}")
    
    try:
        from services.card_manager import card_manager
        print("✅ services.card_manager imported successfully")
    except Exception as e:
        errors.append(f"❌ services.card_manager: {e}")
    
    try:
        from handlers import start, review
        print("✅ handlers imported successfully")
    except Exception as e:
        errors.append(f"❌ handlers: {e}")
    
    try:
        from scheduler.reminder_scheduler import ReminderScheduler
        print("✅ scheduler.reminder_scheduler imported successfully")
    except Exception as e:
        errors.append(f"❌ scheduler.reminder_scheduler: {e}")
    
    if errors:
        print("\n❌ Import errors found:")
        for error in errors:
            print(f"  {error}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)

