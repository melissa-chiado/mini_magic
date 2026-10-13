"""Interface de terminal. Toda entrada e saída do jogador fica neste módulo."""

from combat import attack, creature_combat, creatures
from constants import GENERIC_MANA
from game import cleanup, create_game, draw, play_card, start_turn
from mana import can_pay
from models import Creature, Land, Sorcery


def get_number(message):
    while True:
        choice = input(message).strip()
        if choice.isdigit():
            return int(choice)
        print("Please type a number.")


def format_cost(card):
    if not card.cost:
        return "free"

    parts = []
    for color, amount in card.cost.items():
        label = "generic mana" if color == GENERIC_MANA else color
        parts.append(f"{label}: {amount}")
    return ", ".join(parts)


def show_mana(player):
    print("\nMana pool:")
    for color, amount in player.mana_pool.items():
        print(f"  {color}: {amount}")


def show_hand(player):
    print(f"\n{player.name}'s hand:")
    if not player.hand:
        print("  (empty)")
        return

    for index, card in enumerate(player.hand, start=1):
        if isinstance(card, Creature):
            details = f"Cost: {format_cost(card)} | {card.power}/{card.toughness}"
        elif isinstance(card, Land):
            details = f"Produces: {card.mana_color} mana"
        elif isinstance(card, Sorcery):
            details = f"Cost: {format_cost(card)}"
            if card.damage:
                details += f" | Damage: {card.damage}"
            if card.heal:
                details += f" | Heal: {card.heal}"
        else:
            details = ""
        print(f"  {index}. {card.name} ({details})")


def show_battlefield(player):
    print(f"\n{player.name}'s battlefield:")
    if not player.board:
        print("  (empty)")
        return

    for card in player.board:
        if isinstance(card, Creature):
            status = "summoning sick" if card.summoning_sick else "ready"
            print(f"  {card.name} ({card.power}/{card.toughness}, {status})")
        elif isinstance(card, Land):
            print(f"  {card.name}")
        else:
            print(f"  {card.name}")


def choose_generic_payment(player, card):
    """A interface pergunta como pagar o custo genérico; mana.py só valida."""
    generic_cost = card.cost.get(GENERIC_MANA, 0)
    if generic_cost == 0:
        return []

    available = player.mana_pool.copy()
    for color, amount in card.cost.items():
        if color != GENERIC_MANA:
            available[color] -= amount

    payment = []
    for unit in range(generic_cost):
        while True:
            print(f"\nChoose mana for generic cost ({unit + 1}/{generic_cost}):")
            for color, amount in available.items():
                if amount > 0:
                    print(f"  {color}: {amount}")

            chosen_color = input("Type a color: ").strip().lower()
            if chosen_color not in available:
                print("Invalid color.")
            elif available[chosen_color] <= 0:
                print(f"You have no available {chosen_color} mana for this cost.")
            else:
                available[chosen_color] -= 1
                payment.append(chosen_color)
                break

    return payment


def main_phase(player, opponent):
    while player.hand:
        show_mana(player)
        show_hand(player)
        choice = get_number("\nChoose a card number (0 to finish this phase): ")

        if choice == 0:
            return
        if choice < 1 or choice > len(player.hand):
            print("Invalid number!")
            continue

        card = player.hand[choice - 1]

        if not isinstance(card, Land) and not can_pay(player, card):
            print("Not enough mana!")
            continue

        generic_payment = []
        if not isinstance(card, Land) and card.cost.get(GENERIC_MANA, 0) > 0:
            generic_payment = choose_generic_payment(player, card)

        success, message = play_card(player, opponent, card, generic_payment)
        if message:
            print(f"\n{message}")
        # if success:
        #     show_mana(player)


def choose_blocker(opponent):
    blockers = creatures(opponent)
    if not blockers:
        print(f"\n{opponent.name} has no creatures available to block.")
        return None

    print(f"\n{opponent.name}, choose a blocker:")
    print("  0. Don't block")
    for index, creature in enumerate(blockers, start=1):
        print(f"  {index}. {creature.name} ({creature.power}/{creature.toughness})")

    while True:
        choice = get_number("Choose a blocker: ")
        if choice == 0:
            return None
        if 1 <= choice <= len(blockers):
            return blockers[choice - 1]
        print("Invalid number!")


def combat_phase(player, opponent):
    attackers = creatures(player)
    if not attackers:
        return

    print(f"\nCombat phase. {opponent.name} has {opponent.life} life left.")
    show_battlefield(player)

    while True:
        print("\nChoose an attacking creature:")
        for index, creature in enumerate(attackers, start=1):
            print(f"  {index}. {creature.name} ({creature.power}/{creature.toughness})")
        print("  0. Do not attack")

        choice = get_number("Choose a creature: ")
        if choice == 0:
            return
        if choice < 1 or choice > len(attackers):
            print("Invalid number!")
            continue

        attacker = attackers[choice - 1]
        if attacker.summoning_sick:
            print(f"{attacker.name} has summoning sickness and cannot attack yet.")
            continue

        blocker = choose_blocker(opponent)
        if blocker is None:
            print("\n" + attack(player, opponent, attacker))
        else:
            print("\n" + creature_combat(player, opponent, attacker, blocker))
        # Mantém o comportamento da versão do notebook: um ataque por fase.
        return


def player_turn(player, opponent, all_players):
    print("\n" + start_turn(player))
    print(draw(player))

    print("\nPre-combat main phase")
    main_phase(player, opponent)

    combat_phase(player, opponent)

    print("\nPost-combat main phase")
    main_phase(player, opponent)

    cleanup(all_players)


def run_game():
    player1, player2 = create_game()
    players = [player1, player2]
    print("Welcome to Mini Magic!")

    while True:
        player_turn(player1, player2, players)
        if player2.life <= 0:
            print(f"\n{player1.name} wins!")
            break

        player_turn(player2, player1, players)
        if player1.life <= 0:
            print(f"\n{player2.name} wins!")
            break
