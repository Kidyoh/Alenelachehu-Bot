from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    user_id: int
    nickname: str
    age: int
    gender: str
    nationality: str

@dataclass
class Vent:
    id: int
    user_id: int
    content: str
    timestamp: datetime
    allow_reactions: bool
    allow_public_comments: bool
    allow_professional_comments: bool