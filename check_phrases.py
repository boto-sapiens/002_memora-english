#!/usr/bin/env python3
"""Check loaded phrases"""

from config import DEFAULT_PHRASES

print("=" * 60)
print("DEFAULT_PHRASES Configuration")
print("=" * 60)
print(f"\nTotal phrases: {len(DEFAULT_PHRASES)}")
print("\n" + "=" * 60)
print("List of phrases:")
print("=" * 60)

for i, phrase in enumerate(DEFAULT_PHRASES, 1):
    print(f"\n{i:2d}. {phrase}")

print("\n" + "=" * 60)
print(f"✅ Loaded {len(DEFAULT_PHRASES)} phrases successfully!")
print("=" * 60)

