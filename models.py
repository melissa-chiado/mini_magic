"""Classes principais do jogo: jogadores e tipos de carta."""

from constants import CREATURE, LAND, MANA_COLORS, SORCERY
from mana import pay_cost


class Player:
    def __init__(self, name):
        self.name = name
        self.life = 20
        self.hand = []
        self.deck = []
        self.board = []
        self.mana_pool = {color: 0 for color in MANA_COLORS}
        self.max_mana = 0
        self.lands_played_this_turn = 0


class Card:
    def __init__(self, name, cost=None):
        self.name = name
        self.cost = dict(cost or {})
        self.card_type = None

    def play(self, player, opponent, generic_payment=None):
        """Cada subclasse implementa seu próprio comportamento."""
        raise NotImplementedError("Each card type must implement play().")


class Land(Card):
    def __init__(self, name, mana_color):
        super().__init__(name=name, cost={})
        self.card_type = LAND
        self.mana_color = mana_color

    def play(self, player, opponent, generic_payment=None):
        if player.lands_played_this_turn >= 1:
            return False, "You already played a land this turn!"

        player.board.append(self)
        player.lands_played_this_turn += 1
        player.mana_pool[self.mana_color] += 1
        return True, f"{player.name} plays {self.name}!"


class Creature(Card):
    def __init__(self, name, cost, power, toughness):
        super().__init__(name=name, cost=cost)
        self.card_type = CREATURE
        self.power = power
        self.toughness = toughness
        self.damage_taken = 0
        self.summoning_sick = True

    def play(self, player, opponent, generic_payment=None):
        success, message = pay_cost(player, self, generic_payment)
        if not success:
            return False, message

        player.board.append(self)
        self.summoning_sick = True
        return True, f"{player.name} summons {self.name}!"


class Sorcery(Card):
    def __init__(self, name, cost, damage=0, heal=0):
        super().__init__(name=name, cost=cost)
        self.card_type = SORCERY
        self.damage = damage
        self.heal = heal

    def play(self, player, opponent, generic_payment=None):
        success, message = pay_cost(player, self, generic_payment)
        if not success:
            return False, message

        if self.damage > 0:
            opponent.life -= self.damage
            message = (
                f"{player.name} plays {self.name}!\n"
                f"{opponent.name} takes {self.damage} damage!\n"
                f"{opponent.name} has {opponent.life} life left."
            )
        else:
            player.life += self.heal
            message = (
                f"{player.name} plays {self.name}!\n"
                f"{player.name} heals {self.heal} points!\n"
                f"{player.name} has {player.life} life left."
            )

        return True, message
