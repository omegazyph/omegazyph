"""
"alt" + "3" = ♥
"alt" + "4" = ♦
"alt" + "5" = ♣
"alt" + "6" = ♠
"""


"""
 _____
|A    |
|  ♠  |
|____A|
"""


def display_cards(rank1, suit1, rank2, suit2):
    card1 = [
        f"┌───────┐",
        f"| {rank1:<2}    |",
        f"|       |",
        f"|   {suit1}   |",
        f"|       |",
        f"|    {rank1:>2} |",
        f"└───────┘"
    ]
    card2 = [
        f"┌───────┐",
        f"| {rank2:<2}    |",
        f"|       |",
        f"|   {suit2}   |",
        f"|       |",
        f"|    {rank2:>2} |",
        f"└───────┘"
    ]
    combined_cards = [""] * 7
    for i in range(7):
        combined_cards[i] = card1[i] + "   " + card2[i]
    return "\n".join(combined_cards)

# Example usage:
print(display_cards('A', '♠', 'K', '♥'))

