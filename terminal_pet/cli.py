"""Командная строка: `terminal-pet <команда>`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .ascii import render
from .pet import Pet, greeting_for

COMMANDS = {
    "feed": "покормить питомца",
    "play": "поиграть с питомцем",
    "sleep": "уложить спать",
    "status": "показать текущее состояние",
    "tick": "прожить один 'тик' времени (голод растёт, появляется приветствие)",
    "info": "общая информация о питомце",
    "reset": "стереть сохранение и начать заново",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="terminal-pet",
        description="Милый ASCII-зверёк, который живёт в терминале и помнит тебя между запусками.",
        epilog="Команды: " + ", ".join(f"{k} ({v})" for k, v in COMMANDS.items()),
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="greet",
        choices=["greet", *COMMANDS],
        help="что сделать с питомцем",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="имя питомца при первом запуске",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=None,
        help="файл сохранения (по умолчанию ~/.terminal_pet.json)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    path = args.file or Pet.MOOD_DEFAULT_FILE
    pet = Pet.load(path)

    if args.name:
        if pet.age == 0 and pet.times_fed == 0:
            pet.name = args.name
        else:
            print("Имя уже задано при рождении. Его нельзя менять — это же компаньон!")
            return 2

    command = args.command

    def show(message: str) -> None:
        print(render(pet))
        print()
        print(message)

    if command == "greet":
        message = greeting_for(pet)
        show(message)
    elif command == "feed":
        show(pet.feed())
    elif command == "play":
        show(pet.play())
    elif command == "sleep":
        show(pet.sleep())
    elif command == "status":
        show(f"{pet.name} в порядке. Посмотри, как он(а) выглядит!")
    elif command == "tick":
        result = pet.tick()
        show(result if result else f"Тик-так. {pet.name} чуть проголодался(ась).")
    elif command == "info":
        print(
            f"Имя: {pet.name}\n"
            f"День рождения: {pet.born_on}\n"
            f"Возраст (тиков): {pet.age}\n"
            f"Накормлен(а): {pet.times_fed} раз(а)\n"
            f"Настроение: {pet.mood}"
        )
        return 0
    elif command == "reset":
        if path.exists():
            path.unlink()
        pet = Pet(name=pet.name)
        pet.save(path)
        print("Всё стёрто. Новый питомец родился прямо в твоём терминале!")
        print(render(pet))
        return 0

    pet.save(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())