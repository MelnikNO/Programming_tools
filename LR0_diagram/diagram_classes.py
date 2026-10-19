from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
import uuid


class UserRole(Enum):
    ADMIN = "ADMIN"
    HEAD_TEACHER = "HEAD_TEACHER"
    TEACHER = "TEACHER"

class ConversationStatus(Enum):
    PLANNED = "PLANNED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class User:
    id: uuid.UUID
    full_name: str
    email: str
    password_hash: str
    role: UserRole = field(init=False) 
    def login(self, email: str, password: str) -> bool:
        return self.email == email 

    def logout(self) -> None:
        pass


@dataclass
class Teacher(User):
    position: str = "Учитель"
    role: UserRole = field(default=UserRole.TEACHER, init=False)

    def __post_init__(self):
        object.__setattr__(self, 'role', UserRole.TEACHER)

    def open_student_card(self, student: Student) -> None:
        print(f"Открыта карточка ученика: {student.full_name}")

    def create_conversation(self, student: Student) -> Conversation:
        return Conversation(
            id=uuid.uuid4(),
            date_time=datetime.now(),
            topic="Новая беседа",
            content="",
            status=ConversationStatus.PLANNED
        )


@dataclass
class HeadTeacher(Teacher):
    role: UserRole = field(default=UserRole.HEAD_TEACHER, init=False)
    position: str = "Завуч"

    def complete_follow_up(self, follow_up: FollowUp) -> None:
        follow_up.mark_completed()


@dataclass
class Admin(HeadTeacher):
    role: UserRole = field(default=UserRole.ADMIN, init=False)
    position: str = "Администратор"

    def manage_users(self) -> None:
        print("Управление пользователями системы")


@dataclass
class Student:
    id: uuid.UUID
    full_name: str
    birth_date: date
    
    parents: list[Parent] = field(default_factory=list)

    def get_parents(self) -> list[Parent]:
        return self.parents

@dataclass
class Parent:
    id: uuid.UUID
    full_name: str
    phone: str

    children: list[Student] = field(default_factory=list)


@dataclass
class Participant:
    parent: Parent
    attended: bool = False


@dataclass
class FollowUp:
    id: uuid.UUID
    description: str
    due_date: date
    is_completed: bool = False

    def mark_completed(self) -> None:
        self.is_completed = True


@dataclass
class Conversation:
    id: uuid.UUID
    date_time: datetime
    topic: str
    content: str
    status: ConversationStatus = ConversationStatus.PLANNED
    
    participants: list[Participant] = field(default_factory=list)
    follow_ups: list[FollowUp] = field(default_factory=list)

    def complete(self) -> None:
        self.status = ConversationStatus.COMPLETED

    def add_participant(self, parent: Parent) -> None:
        self.participants.append(Participant(parent=parent))