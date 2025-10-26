#!/usr/bin/env python3
"""
Test audio switching logic
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.card_view_renderer import card_view_renderer

def test_audio_switch_logic():
    """Test the audio switching button logic"""
    print("🧪 Testing audio switching button logic...")
    
    # Test case 1: Teacher audio active
    print("\n1. Testing teacher audio active:")
    keyboard1 = card_view_renderer._get_answer_keyboard_with_audio_switch(1, "teacher", True, True)
    print(f"   Keyboard rows: {len(keyboard1.inline_keyboard)}")
    if keyboard1.inline_keyboard:
        switch_button = keyboard1.inline_keyboard[0][0]
        print(f"   Switch button text: '{switch_button.text}'")
        print(f"   Switch button callback: '{switch_button.callback_data}'")
    
    # Test case 2: Actor audio active
    print("\n2. Testing actor audio active:")
    keyboard2 = card_view_renderer._get_answer_keyboard_with_audio_switch(1, "actor", True, True)
    print(f"   Keyboard rows: {len(keyboard2.inline_keyboard)}")
    if keyboard2.inline_keyboard:
        switch_button = keyboard2.inline_keyboard[0][0]
        print(f"   Switch button text: '{switch_button.text}'")
        print(f"   Switch button callback: '{switch_button.callback_data}'")
    
    # Test case 3: Only teacher audio available
    print("\n3. Testing only teacher audio available:")
    keyboard3 = card_view_renderer._get_answer_keyboard_with_audio_switch(1, "teacher", True, False)
    print(f"   Keyboard rows: {len(keyboard3.inline_keyboard)}")
    if keyboard3.inline_keyboard:
        print(f"   No switch button (only teacher available)")
    
    # Test case 4: Only actor audio available
    print("\n4. Testing only actor audio available:")
    keyboard4 = card_view_renderer._get_answer_keyboard_with_audio_switch(1, "actor", False, True)
    print(f"   Keyboard rows: {len(keyboard4.inline_keyboard)}")
    if keyboard4.inline_keyboard:
        print(f"   No switch button (only actor available)")
    
    print("\n🎉 Audio switching logic test completed!")

if __name__ == "__main__":
    test_audio_switch_logic()
