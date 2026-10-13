"""Regras relacionadas a verificar e pagar custos de mana.

Este módulo não usa input() nem print(). A interface é responsável por
perguntar ao jogador como ele quer pagar o mana genérico.
"""

from constants import GENERIC_MANA


def can_pay(player, card):
    """Retorna True se o jogador tiver mana suficiente para a carta."""
    available = player.mana_pool.copy()

    # Primeiro, reservamos o mana colorido exigido pela carta.
    for color, amount in card.cost.items():
        if color == GENERIC_MANA:
            continue

        if color not in available or available[color] < amount:
            return False

        available[color] -= amount

    # O custo genérico pode ser pago com qualquer mana que sobrou.
    generic_cost = card.cost.get(GENERIC_MANA, 0)
    return sum(available.values()) >= generic_cost


def pay_cost(player, card, generic_payment=None):
    """Paga o custo sem solicitar informações ao usuário.

    generic_payment deve ser uma lista com a cor gasta para cada unidade de
    mana genérico. Exemplo: ["green", "white"]. A função valida o pagamento
    inteiro antes de alterar o mana_pool, evitando pagamentos parciais.

    Retorna (sucesso, mensagem).
    """
    if not can_pay(player, card):
        return False, "Not enough mana!"

    generic_cost = card.cost.get(GENERIC_MANA, 0)
    generic_payment = list(generic_payment or [])

    if len(generic_payment) != generic_cost:
        if generic_cost == 0 and not generic_payment:
            pass
        else:
            return False, "The generic mana payment is incomplete."

    available = player.mana_pool.copy()

    # Reservar primeiro os custos coloridos obrigatórios.
    for color, amount in card.cost.items():
        if color == GENERIC_MANA:
            continue
        available[color] -= amount

    # Depois validar as cores escolhidas para o custo genérico.
    for color in generic_payment:
        if color not in available or available[color] <= 0:
            return False, f"Invalid generic mana payment: {color}."
        available[color] -= 1

    # Só altera a mana pool depois que todo o pagamento foi validado.
    player.mana_pool = available
    return True, ""
