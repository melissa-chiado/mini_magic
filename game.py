"""Operações do motor do jogo, sem interação com o terminal."""

import random

from cards import create_deck
from constants import MANA_COLORS
from models import Creature, Land, Player


def create_game():
    """Cria dois jogadores, embaralha os decks e compra sete cartas iniciais."""
    player1 = Player("Alice")
    player2 = Player("Bob")
    player1.deck = create_deck()
    player2.deck = create_deck()

    random.shuffle(player1.deck)
    random.shuffle(player2.deck)

    for _ in range(7):
        player1.hand.append(player1.deck.pop())
        player2.hand.append(player2.deck.pop())

    return player1, player2


def refill_mana(player):
    """Recalcula o mana produzido pelas lands no campo (regra simplificada)."""
    player.mana_pool = {color: 0 for color in MANA_COLORS}
    for card in player.board:
        if isinstance(card, Land):
            player.mana_pool[card.mana_color] += 1


def start_turn(player):
    player.lands_played_this_turn = 0
    refill_mana(player)

    # Na versão atual, a summoning sickness termina no próximo turno do dono.
    for card in player.board:
        if isinstance(card, Creature):
            card.summoning_sick = False

    return f"{player.name}'s turn begins."


def draw(player):
    if not player.deck:
        return f"{player.name} has no cards left to draw."

    card = player.deck.pop()
    player.hand.append(card)
    return f"{player.name} draws {card.name}."


def play_card(player, opponent, card, generic_payment=None):
    """Pede à carta que se jogue e a remove da mão apenas se houver sucesso."""
    if card not in player.hand:
        return False, "That card is not in your hand."

    success, message = card.play(player, opponent, generic_payment)
    if success:
        player.hand.remove(card)

    return success, message


def cleanup(players):
    """Remove o dano marcado de todas as criaturas no fim do turno."""
    for player in players:
        for card in player.board:
            if isinstance(card, Creature):
                card.damage_taken = 0
