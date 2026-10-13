"""Fábricas de cartas e criação dos decks.

Cada chamada cria uma instância nova. Isso evita que cópias da mesma carta
compartilhem estado, como summoning_sick ou damage_taken.
"""

from constants import BLACK, BLUE, GENERIC_MANA, GREEN, RED, WHITE
from models import Creature, Land, Sorcery


def create_plains():
    return Land("Plains", WHITE)


def create_island():
    return Land("Island", BLUE)


def create_swamp():
    return Land("Swamp", BLACK)


def create_mountain():
    return Land("Mountain", RED)


def create_forest():
    return Land("Forest", GREEN)


def create_goblin():
    return Creature("Goblin", cost={RED: 1}, power=1, toughness=1)


def create_beast():
    return Creature(
        "Beast",
        cost={GREEN: 1, GENERIC_MANA: 1},
        power=3,
        toughness=3,
    )


def create_shock():
    return Sorcery("Shock", cost={RED: 1}, damage=2)


def create_fireball():
    return Sorcery(
        "Fireball",
        cost={RED: 2, GENERIC_MANA: 3},
        damage=8,
    )


def create_healing_salve():
    return Sorcery("Healing Salve", cost={WHITE: 1}, heal=3)


def create_angels_mercy():
    return Sorcery(
        "Angel's Mercy",
        cost={WHITE: 2, GENERIC_MANA: 2},
        heal=7,
    )


def create_deck():
    """Cria um deck com a mesma composição da versão original do notebook."""
    deck = (
        [create_mountain() for _ in range(10)]
        + [create_plains() for _ in range(5)]
        + [create_forest() for _ in range(5)]
        + [create_shock() for _ in range(5)]
        + [create_fireball() for _ in range(5)]
        + [create_goblin() for _ in range(5)]
        + [create_healing_salve() for _ in range(3)]
        + [create_angels_mercy()]
        + [create_beast() for _ in range(5)]
    )
    return deck
