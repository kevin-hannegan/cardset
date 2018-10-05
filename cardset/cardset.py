import random

class card:  
    
    def __init__(self, suit=None, rank=None, faceUp=None):
        self.suits = {
            0 : 'Diamonds',
            1 : 'Clubs',
            2 : 'Hearts',
            3 : 'Spades'
        }
        self.ranks = {
            1 : 'Ace',
            2 : 'Two',
            3 : 'Three',
            4 : 'Four',
            5 : 'Five',
            6 : 'Six',
            7 : 'Seven',
            8 : 'Eight',
            9 : 'Nine',
            10 : 'Ten',
            11 : 'Jack',
            12 : 'Queen',
            13 : 'King'
        }
        if suit is None:
            self.suit = self.suits[random.randint(0,3)]
        else:
            self.suit = suit
        if rank is None:
            self.rank = self.ranks[random.randint(1,13)]
        else:
            self.rank = rank
        if faceUp is None:
            self.faceUp = False
        else:
            self.faceUp = faceUp

    def flip(self):
        if self.faceUp == False:
            self.faceUp = True
        else:
            self.faceUp = False

    def shortHand(self, side=False):
        rankKey = ['A','2','3','4','5','6','7','8','9','T','J','Q','K']
        for key in range(1, len(self.ranks)+1):
            if self.ranks[key] == self.rank[1]:
                rankString = rankKey[key-1]
                break
        suitKey = ['♦','♣','♥','♠']
        for key in range(0,len(self.suits)):
            if self.suits[key] == self.suit[1]:
                suitString = suitKey[key]
        cardString = rankString + suitString
        if side is True:
            if self.faceUp is True:
                cardString += "_U"
            else:
                cardString += "_D"
        return cardString

    def pickACard(self):
        self.suit = self.suits[random.randint(0,3)]
        self.rank = self.ranks[random.randint(1,13)]
        print("Your card is a " + str(self.rank) + " of " + str(self.suit))
  

class cardset:
    def __init__(self):
        self.cardset = []
        dummycard = card()
        for suit in dummycard.suits.items():
            for rank in dummycard.ranks.items():
                self.cardset.append(card(suit=suit, rank=rank, faceUp=False))

def flip(card):
    if card.faceUp == False:
            card.faceUp = True
    else:
            card.faceUp = False
                 


if __name__ == '__main__':
    somecard = card()
    somecard.pickACard()
    somecard.flip()
    print ("--- Cards in a Set ---")
    singledeck = cardset().cardset
    for eachcard in singledeck:
        print (eachcard.rank[1] + " of " + eachcard.suit[1])
