#!/usr/bin/env python3
"""Test audio service functionality"""

import asyncio
from pathlib import Path
from services.audio_service import AudioService


async def test_audio_paths():
    """Test audio service path resolution"""
    service = AudioService()
    
    print("=" * 70)
    print("Audio Service Test")
    print("=" * 70)
    print()
    
    print(f"Audio directory: {service.audio_dir}")
    print(f"  Exists: {service.audio_dir.exists()}")
    print()
    
    print(f"Teacher directory: {service.teacher_dir}")
    print(f"  Exists: {service.teacher_dir.exists()}")
    
    if service.teacher_dir.exists():
        teacher_files = list(service.teacher_dir.glob("*.mp3"))
        print(f"  Files: {len(teacher_files)}")
        if teacher_files:
            for f in teacher_files[:5]:
                print(f"    - {f.name}")
    print()
    
    print(f"Actor directory: {service.actor_dir}")
    print(f"  Exists: {service.actor_dir.exists()}")
    
    if service.actor_dir.exists():
        actor_files = list(service.actor_dir.glob("*.mp3"))
        print(f"  Files: {len(actor_files)}")
        if actor_files:
            for f in actor_files[:5]:
                print(f"    - {f.name}")
    print()
    
    # Test file name formatting
    print("Expected file names:")
    for i in range(1, 6):
        teacher_file = service.teacher_dir / f"{i}_myvoiceEarn.mp3"
        actor_file = service.actor_dir / f"{i}_Earnest.mp3"
        print(f"  Card {i}:")
        print(f"    Teacher: {teacher_file.name} - {'✅' if teacher_file.exists() else '❌'}")
        print(f"    Actor:   {actor_file.name} - {'✅' if actor_file.exists() else '❌'}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_audio_paths())

