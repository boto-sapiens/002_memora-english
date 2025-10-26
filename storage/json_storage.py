import json
import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import asyncio
from storage.models import User, UserCard
from services.anki_algorithm import get_current_time
from config import DATA_DIR, DEFAULT_PHRASES


class JSONStorage:
    def __init__(self):
        self.data_dir = Path(DATA_DIR)
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.lock = asyncio.Lock()
        self._ensure_files()
    
    def _ensure_files(self):
        """Ensure data files exist"""
        if not self.users_file.exists():
            self._write_json(self.users_file, {"users": {}})
    
    def _read_json(self, file_path: Path) -> dict:
        """Read JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _write_json(self, file_path: Path, data: dict):
        """Write JSON file atomically"""
        temp_file = file_path.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp_file.replace(file_path)
    
    async def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram_id"""
        async with self.lock:
            data = self._read_json(self.users_file)
            user_data = data.get("users", {}).get(str(telegram_id))
            if user_data:
                return User.from_dict(user_data["info"])
            return None
    
    async def save_user(self, user: User):
        """Save or update user"""
        async with self.lock:
            data = self._read_json(self.users_file)
            if "users" not in data:
                data["users"] = {}
            
            user_id = str(user.telegram_id)
            if user_id not in data["users"]:
                data["users"][user_id] = {"info": user.to_dict(), "cards": []}
            else:
                data["users"][user_id]["info"] = user.to_dict()
            
            self._write_json(self.users_file, data)
    
    async def get_user_cards(self, telegram_id: int) -> List[UserCard]:
        """Get all cards for user"""
        async with self.lock:
            data = self._read_json(self.users_file)
            user_data = data.get("users", {}).get(str(telegram_id))
            if user_data and "cards" in user_data:
                return [UserCard.from_dict(card) for card in user_data["cards"]]
            return []
    
    async def save_user_card(self, card: UserCard):
        """Save or update a user card"""
        async with self.lock:
            data = self._read_json(self.users_file)
            user_id = str(card.user_id)
            
            if user_id not in data["users"]:
                return
            
            cards = data["users"][user_id]["cards"]
            # Find and update existing card or append new one
            found = False
            for i, existing_card in enumerate(cards):
                if existing_card["card_id"] == card.card_id:
                    cards[i] = card.to_dict()
                    found = True
                    break
            
            if not found:
                cards.append(card.to_dict())
            
            self._write_json(self.users_file, data)
    
    async def init_learning_cards(self, telegram_id: int):
        """Initialize all 21 cards for a new user in learning phase"""
        now = get_current_time().isoformat()
        cards = []
        
        for phrase_data in DEFAULT_PHRASES:
            card = UserCard(
                user_id=telegram_id,
                card_id=phrase_data['id'],
                text=phrase_data['text_en'],
                interval_index=0,
                next_review_time=now,
                status='learning',
                created_at=now,
                last_reviewed=None,
                text_ru=phrase_data.get('text_ru'),
                text_en=phrase_data.get('text_en'),
                transcription=phrase_data.get('transcription'),
                audio_teacher=phrase_data.get('audio_teacher'),
                audio_actor=phrase_data.get('audio_actor'),
                file_id_teacher=None,
                file_id_actor=None
            )
            cards.append(card)
        
        # Save all cards at once
        async with self.lock:
            data = self._read_json(self.users_file)
            user_id = str(telegram_id)
            if user_id in data["users"]:
                data["users"][user_id]["cards"] = [card.to_dict() for card in cards]
                self._write_json(self.users_file, data)
    
    async def get_due_cards(self, telegram_id: int) -> List[UserCard]:
        """Get cards that are due for review"""
        cards = await self.get_user_cards(telegram_id)
        now = get_current_time()
        
        due_cards = []
        for card in cards:
            if card.status == 'review':
                next_review = datetime.fromisoformat(card.next_review_time)
                if next_review <= now:
                    due_cards.append(card)
        
        return due_cards
    
    async def get_all_users(self) -> List[User]:
        """Get all users"""
        async with self.lock:
            data = self._read_json(self.users_file)
            users = []
            for user_data in data.get("users", {}).values():
                if "info" in user_data:
                    users.append(User.from_dict(user_data["info"]))
            return users


# Global storage instance
storage = JSONStorage()

