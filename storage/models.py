from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class User:
    telegram_id: int
    username: Optional[str]
    created_at: str
    learning_phase_completed: bool = False
    last_notification_time: Optional[str] = None
    last_activity_date: Optional[str] = None
    current_streak: int = 0
    total_reviews: int = 0
    knew_count: int = 0
    doubt_count: int = 0
    forgot_count: int = 0
    # last_audio_message_id removed - using inline playback now
    current_session_total: Optional[int] = None
    current_session_index: int = 0
    # Training mode fields
    training_list_message_id: Optional[int] = None
    training_card_message_id: Optional[int] = None
    training_current_page: int = 1
    training_selected_card_id: Optional[int] = None
    training_current_audio: str = "teacher"  # "teacher" or "actor"
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class UserCard:
    user_id: int
    card_id: int
    text: str
    interval_index: int
    next_review_time: str
    status: str  # 'learning' or 'review'
    created_at: str
    last_reviewed: Optional[str] = None
    text_ru: Optional[str] = None
    text_en: Optional[str] = None
    transcription: Optional[str] = None
    audio_teacher: Optional[str] = None
    audio_actor: Optional[str] = None
    file_id_teacher: Optional[str] = None
    file_id_actor: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class SessionState:
    """State of current learning/review session"""
    current_index: int
    total_in_session: int
    phase: str  # 'learning' or 'review'
    is_completed: bool = False
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

