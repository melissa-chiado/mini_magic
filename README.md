# Mini Magic — Python

Um jogo de cartas simplificado inspirado em Magic: The Gathering, feito para praticar Python e programação orientada a objetos.

> Este projeto implementa apenas um subconjunto simplificado das regras de Magic. Ele não é uma implementação completa das regras oficiais.

## Como executar

1. Instale o Python 3.10 ou superior.
2. Baixe/clonе este repositório.
3. Abra o terminal na pasta `Mini_Magic_Modular`.
4. Execute:

   ```bash
   python main.py
   ```

O projeto usa apenas a biblioteca padrão do Python; não é necessário instalar dependências externas.

## Estrutura dos módulos

| Arquivo | Responsabilidade |
|---|---|
| `constants.py` | Nomes padronizados para cores de mana e tipos de carta. |
| `models.py` | Classes `Player`, `Card`, `Land`, `Creature` e `Sorcery`. |
| `cards.py` | Funções que criam cartas e montam um deck. Cada cópia é uma instância separada. |
| `mana.py` | Verifica e paga custos de mana, sem ler entradas ou imprimir mensagens. |
| `combat.py` | Regras de ataque e combate entre uma criatura atacante e uma bloqueadora. |
| `game.py` | Cria a partida e contém operações básicas do motor, como compra, início de turno e jogar carta. |
| `terminal_ui.py` | Menus, `input()` e `print()` da interface de terminal. |
| `main.py` | Ponto de entrada que inicia o jogo. |
| `tests/` | Testes automatizados básicos do sistema de mana. |

## Princípio de organização

O motor do jogo altera o estado e retorna resultados. A interface de terminal decide como apresentar esses resultados. Por exemplo, `play_card()` retorna `(success, message)`; a função de interface imprime a mensagem. No futuro, uma interface gráfica poderá chamar as mesmas funções do motor sem precisar redesenhar as regras.

## Funcionalidades atuais

- Cartas de criatura, terreno e feitiço (sorcery).
- Custos de mana colorido e genérico.
- Compra de cartas e limite simplificado de um terreno por turno.
- Criaturas com poder, resistência, dano marcado e enjoo de invocação.
- Combate simplificado com uma criatura atacante e no máximo um bloqueador.
- Fases principais pré-combate e pós-combate.

## Limitações conhecidas

- O jogo é uma versão simplificada e não reproduz todas as regras de MTG.
- O mana dos terrenos é disponibilizado automaticamente no início do turno; não há sistema de virar/desvirar terrenos.
- A fase de combate permite um ataque por turno, com no máximo um bloqueador.
- Ainda não há prioridade, pilha, mágicas instantâneas, habilidades ou palavras-chave avançadas.

## Executar os testes

Na pasta do projeto, rode:

```bash
python -m unittest discover -s tests -v
```
