"""Логика жизни питомца: голод, энергия, настроение, старение.

Вся механика живёт здесь и покрыта тестами в tests/.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path

MAX_HUNGER = 100
MAX_ENERGY = 100

MOODS = ("happy", "hungry", "sleepy", "sad", "asleep")

GREETINGS = [
    "Привет! Это я, твой терминальный питомец.",
    "С возвращением! Я по тебе скучал.",
    "О, привет! Покорми меня скорее!",
    "Рад тебя видеть. Терминал без тебя был таким скучным.",
]

MOOD_DEFAULT_FILE = Path.home() / ".terminal_pet.json"


@dataclass
class Pet:
    name: str = "Yuki"
    age: int = 0
    hunger: int = 100
    energy: int = 100
    happiness: int = 100
    times_fed: int = 0
    is_alive: bool = True
    born_on: str = ""

    mood: str = field(default="happy", repr=False)

    def __post_init__(self) -> None:
        if not self.born_on:
            import datetime

            self.born_on = datetime.date.today().isoformat()
        self._update_mood()

    @property
    def max_hunger(self) -> int:
        return MAX_HUNGER

    @property
    def max_energy(self) -> int:
        return MAX_ENERGY

    def _update_mood(self) -> None:
        if not self.is_alive:
            self.mood = "sad"
        elif self.energy <= 15:
            self.mood = "asleep"
        elif self.hunger < 30:  # сытость закончилась — пора есть
            self.mood = "hungry"
        elif self.energy <= 40:
            self.mood = "sleepy"
        elif self.happiness < 30:
            self.mood = "sad"
        else:
            self.mood = "happy"

    def feed(self, amount: int = 30) -> str:
        """Покормить питомца. Возвращает сообщение-реакцию."""
        if not self.is_alive:
            return f"{self.name} уже не с нами..."
        before = self.hunger
        self.hunger = min(MAX_HUNGER, self.hunger + amount)
        if before < 20 and self.hunger >= 20:
            message = f"{self.name} наконец-то поел! Спасибо, я был ужасно голоден."
        elif self.hunger >= MAX_HUNGER:
            message = f"{self.name} сыт по горло и довольно урчит."
        else:
            message = f"{self.name} грызёт угощение. Умм, вкусно!"
        self.times_fed += 1
        self.happiness = min(MAX_ENERGY, self.happiness + 5)
        self._update_mood()
        return message

    def play(self) -> str:
        """Поиграть с питомцем (тратит энергию, но поднимает счастье)."""
        if not self.is_alive:
            return f"{self.name} уже не с нами..."
        if self.energy < 15:
            return f"{self.name} слишком устал(а) и просится спать."
        if self.hunger < 30:
            return f"{self.name} слишком голоден(на), чтобы играть. Сначала покорми."
        self.energy = max(0, self.energy - 15)
        self.happiness = min(MAX_ENERGY, self.happiness + 10)
        self.hunger = max(0, self.hunger - 5)
        self._update_mood()
        return f"{self.name} гоняется за курсором! Это было весело."

    def sleep(self) -> str:
        """Уложить питомца спать (восстанавливает энергию)."""
        if not self.is_alive:
            return f"{self.name} уже не с нами..."
        self.energy = min(MAX_ENERGY, self.energy + 50)
        self.happiness = min(MAX_ENERGY, self.happiness + 5)
        self._update_mood()
        return f"{self.name} сладко зевает и засыпает прямо на клавиатуре. zZz..."

    def tick(self) -> str | None:
        """Один 'тик' жизни: питомец понемногу голодает и устаёт."""
        if not self.is_alive:
            return None
        self.age += 1
        self.hunger = max(0, self.hunger - 3)  # сытость убывает со временем
        if self.happiness > 0 and self.hunger == 0:
            self.happiness = max(0, self.happiness - 10)
        if self.age % 3 == 0:
            self.energy = max(0, self.energy - 2)

        if self.hunger == 0 and self.happiness == 0:
            self.is_alive = False
            self.happiness = 0
            self.energy = 0
            self._update_mood()
            return f"...{self.name} тихо попрощался и ушёл в большой скроллбуфер."
        self._update_mood()
        return None

    def to_dict(self) -> dict:
        data = asdict(self)
        data.pop("mood", None)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        clean = {k: v for k, v in data.items() if k in allowed and k != "mood"}
        return cls(**clean)

    def save(self, path: Path = MOOD_DEFAULT_FILE) -> None:
        path.write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path = MOOD_DEFAULT_FILE) -> "Pet":
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return cls.from_dict(data)
        return cls()


def greeting_for(pet: Pet) -> str:
    if pet.hunger < 30:
        return f"{pet.name} проголодался(ась). Покорми?"
    if pet.energy <= 15:
        return f"{pet.name} совсем сонный(ая)..."
    if pet.happiness < 30:
        return f"{pet.name} выглядит грустным(ой). Поиграй с ним(ней)!"
    return GREETINGS[pet.age % len(GREETINGS)]