import random

class Card:
    suit = ''
    name = ''
    value = 0

    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = name
        self.value = value


class GameSession:
    last_start_message_id = {}

    def __init__(self, name, message_id):
        self.isGame = True
        self.all_cards = []
        self.__CreateCards()
        self.current_player_index = 0
        self.current_player = Player('', self)
        self.players = []
        self.players.append(Player(name, self))
        self.last_start_message_id = message_id

    def reset(self):
        self.isGame = False
        self.players = []
        self.all_cards = []
        self.__CreateCards()
        self.current_player_index = 0
        self.current_player = Player('', self)
        

    def __CreateCards(self):
        self.all_cards = []
        names = {'2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'}
        names_and_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10,
                            'King': 10, 'Ace': 11}
        suits = ['♦️', '♥️', '♣️', '♠️']
        for current_player_index in suits:
            for j in names:
                card = Card(current_player_index, j, names_and_values[j])
                self.all_cards.append(card)

        random.shuffle(self.all_cards)


class Player:
    def __init__(self, name, session):
        self.name = name
        self.win = False
        self.cards = []
        self.value_sum = 0
        self.session = session

        self.hit()
        self.hit()

    def represent_cards(self):
        result = ""
        for card in self.cards:
            result += card.name + '  ' + card.suit + '  •  '
        return result[:len(result)-3]

    def hit(self):
        self.cards.append(self.session.all_cards.pop())
        self.value_sum += self.cards[-1].value
        self.cards.sort(key=lambda card: card.value)
        if self.value_sum > 21:
            for c in self.cards:
                if c.name == 'Ace' and c.value != 1:
                    c.value = 1
                    self.value_sum -= 10
                    break
            if self.value_sum > 21:
                return True
        if self.value_sum == 21:
            self.win = True
            return True
        return False
