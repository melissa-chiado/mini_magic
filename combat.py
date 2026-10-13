"""Regras básicas de combate. Não contém input() nem print()."""

from models import Creature


def creatures(player):
    """Retorna as criaturas no campo do jogador."""
    return [card for card in player.board if isinstance(card, Creature)]


def attack(player, opponent, attacker):
    """Aplica dano ao oponente quando a criatura não é bloqueada."""
    opponent.life -= attacker.power
    return (
        f"{attacker.name} attacks {opponent.name}!\n"
        f"{opponent.name} takes {attacker.power} damage!\n"
        f"{opponent.name} has {opponent.life} life left."
    )


def creature_combat(player, opponent, attacker, blocker):
    """Resolve dano simultâneo entre uma criatura atacante e uma bloqueadora."""
    attacker.damage_taken += blocker.power
    blocker.damage_taken += attacker.power

    messages = [f"{blocker.name} blocks {attacker.name}!"]

    if attacker.damage_taken >= attacker.toughness:
        player.board.remove(attacker)
        messages.append(f"{attacker.name} dies!")

    if blocker.damage_taken >= blocker.toughness:
        opponent.board.remove(blocker)
        messages.append(f"{blocker.name} dies!")

    if len(messages) == 1:
        messages.append("Both creatures survive combat.")

    return "\n".join(messages)
