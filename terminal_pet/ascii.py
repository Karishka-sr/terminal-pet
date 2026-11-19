"""ASCII-арт мордочки питомца в разных настроениях и состояниях.

Числа в описании модуля не содержат логики — вся логика живёт в `pet.py`.
Этот модуль отвечает только за "красивости" терминала.
"""

ART = {
    "happy": [
        r"  /\_/\  ",
        r" ( ^.^ ) ",
        r"  > ~ <  ",
    ],
    "hungry": [
        r"  /\_/\  ",
        r" ( o.o ) ",
        r"  > ~ <  ",
    ],
    "sleepy": [
        r"  /\_/\  ",
        r" ( -_- ) ",
        r"  > ~ <  ",
    ],
    "sad": [
        r"  /\_/\  ",
        r" ( ;_; ) ",
        r"  > ~ <  ",
    ],
    "asleep": [
        r"  /\_/\  ",
        r" ( u.u ) ",
        r"  > ~ <  ",
    ],
}

MOOD_EMOJI = {
    "happy": "(^_^)",
    "hungry": "(o.o)",
    "sleepy": "(-_-)",
    "sad": "(;_;)",
    "asleep": "(u.u)zZ",
}

FULL = "\u2588"  # █
EMPTY = "\u2591"  # ░


def _bar(value: int, max_value: int, width: int = 5) -> str:
    """Полоска прогресса из блоков, зелёная/жёлтая/красная в зависимости от уровня."""
    value = max(0, min(value, max_value))
    ratio = value / max_value if max_value else 0
    filled = round(ratio * width)
    if ratio < 0.34:
        color = 31  # red
    elif ratio < 0.67:
        color = 33  # yellow
    else:
        color = 32  # green
    return (
        f"\033[{color}m{FULL * filled}\033[0m"
        f"{EMPTY * (width - filled)}"
    )


def render(pet) -> str:
    """Собирает картинку питомца: имя, мордочку и статусы."""
    lines = [f"  {pet.name}  {MOOD_EMOJI[pet.mood]}"]
    lines.extend(ART[pet.mood])
    lines.append(f"  hunger {_bar(pet.hunger, pet.max_hunger)}")
    lines.append(f"  energy {_bar(pet.energy, pet.max_energy)}")
    return "\n".join(lines)