from cardset import card, cardset
import random, re


class spider:
    def __init__(self):
        self.deck = self.createDecks()
        print ("Deck Created...")
        self.board = self.createBoard()
        print ("Board Built...")
        self.deck = self.shuffle(self.deck)
        print ("Deck Shuffled...")
        self.board, self.deck = self.deal(self.board, self.deck)
        self.stats = self.stats()
        print("Board dealt - ready to play!")
        self.cont = True
        self.winningBoard = [[] for x in range(0, 10)]

    def createDecks(self):
        numberdecks = 2
        deck = []
        packages = []
        for pack in range(0, numberdecks):
            packages.append(cardset().cardset)
        for eachPack in packages:
            for eachCard in eachPack:
                deck.append(eachCard)
        return deck

    def createBoard(self):
        numberSlots = 10
        slots = [[] for x in range(numberSlots)]
        return slots

    def shuffle(self, deck):
        numberCards = len(deck)
        shuffledDeck = []
        for a in range(0, numberCards):
            pulledCard = random.randint(0,numberCards-1)
            shuffledDeck.append(deck[pulledCard])
            del deck[pulledCard]
            numberCards -= 1        
        return shuffledDeck

    def deal(self, board, deck):
        faceDownCards = len(deck) - 6 * len(board)
        cardsDelt = 0
        while cardsDelt < faceDownCards:
            for eachSlot in board:
                eachSlot.append(deck[0])
                cardsDelt += 1
                del deck[0]
                if cardsDelt == faceDownCards:
                    break
     
        for eachSlot in board:
            deck[0].flip()
            eachSlot.append(deck[0])
            cardsDelt += 1
            del deck[0]

        return board, deck



    def showBoard(self, board):
        print("")
        print("--------- CURRENT STATE OF BOARD ---------")
        print("")
        print("    1   2   3   4   5   6   7   8   9   10")
        maxStack = 0
        for eachSlot in board:
            if len(eachSlot) > maxStack:
                maxStack = len(eachSlot)
        rowString = ""
        for row in range(0, maxStack):
            rowString = str(row + 1) + " "
            if row < 9:
                rowString += " "
            for eachSlot in board:
                if len(eachSlot) > row:
                    if eachSlot[row].faceUp is True:
                        rowString += " " + eachSlot[row].shortHand() + " "
                    else:
                        rowString += " -- "
                else:
                    rowString += "    "
            print(rowString)
        print("")
        print("")

    def move(self, board, fromSlot, numberCards, toSlot, validationOverride=False):
        if validationOverride is False:
            if self.moveValidate(board, fromSlot, numberCards, toSlot) is False:
                print("Invalid Move!")
                return False, board
        for eachCard in board[fromSlot-1][len(board[fromSlot-1])-numberCards:len(board[fromSlot-1])]:
            board[toSlot-1].append(eachCard)
        if board[fromSlot-1][len(board[fromSlot-1])-numberCards-1].faceUp == False:
            board[fromSlot-1][len(board[fromSlot-1])-numberCards-1].faceUp = True
            underCardFlip = True
        else:
            underCardFlip = False
        del board[fromSlot-1][len(board[fromSlot-1])-numberCards:len(board[fromSlot-1])]
        self.stats.normalMove([fromSlot, numberCards, toSlot, underCardFlip])
        board = self.clearSet(board)
        return True, board


    def moveValidate(self, board, fromSlot, numberCards, toSlot):
         # check for valid slot entries
        if fromSlot > 10 or toSlot > 10 or fromSlot <= 0 or toSlot <= 0:
            return False
        # check there is enough cards in the stack to make the move
        if len(board[fromSlot - 1]) < numberCards:
            return False
        # check all moved cards are face up
        for eachCard in board[fromSlot-1][len(board[fromSlot-1])-numberCards:len(board[fromSlot-1])]:
            if eachCard.faceUp is False:
                return False
        # check last moved card is one rank below facing card in target slot
        if board[toSlot-1] != []:
            moveRank = board[fromSlot-1][len(board[fromSlot-1])-numberCards].rank[0]
            toRank = board[toSlot-1][len(board[toSlot-1])-1].rank[0]
            if moveRank != toRank - 1:
                return False
        # check all cards being moved are of same suit
        topSuit = True
        for eachCard in board[fromSlot-1][len(board[fromSlot-1])-numberCards:len(board[fromSlot-1])]:
            if topSuit == True:
                checkSuit = eachCard.suit
                topSuit = False
            if eachCard.suit != checkSuit:
                return False
        return True

    def inputMove(self, board, deck):
        drawsRemaining = int(len(deck) / 10)
        print("Score = " + str(self.stats.score) + "   Move Count = " + str(self.stats.moveCount))
        print(str(drawsRemaining) + " draws remaining.  Type D in input to draw, U to undo")
        print("Move format: From Slot, Number of Cards, To Slot")
        moveString = input("Input move: ")
        try:
            if moveString == 'd' or moveString == 'D' or moveString == 'Draw' or moveString == 'draw':
                self.draw(board, deck)
                self.showBoard(board)
                success = True
                return success, board
            if moveString == 'undo' or moveString == 'Undo' or moveString == 'u' or moveString == 'U':
                success, board = self.undo(board)
                self.showBoard(board)
                return success, board

            if moveString == 'exit':
                self.end()
            [a, b, c] = re.split(',', moveString)
            fromSlot = int(a)
            numberCards = int(b)
            toSlot = int(c)
        except:
            print("Input Error. Try Again")
            self.inputMove(board, deck)
            success = True
            return success, board
        success, board = self.move(board, fromSlot, numberCards, toSlot)
        self.showBoard(board)
        return success, board
    
    def clearSet(self, board):
        slotNumber = 0
        for eachSlot in board:
            clearSet = False
            if len(eachSlot) > 12:
                tempsuit = eachSlot[len(eachSlot)-1].suit[1]
                for suitedSet in range(0,13):
                    if eachSlot[len(eachSlot) - suitedSet - 1].suit[1] != tempsuit:
                        if eachSlot[len(eachSlot) - suitedSet - 1].rank[0] != suitedSet:
                            break
                    else:
                        if suitedSet == 12 and eachSlot[len(eachSlot) -1].rank[0] == suitedSet:
                            del board[slotNumber][len(eachSlot):len(eachSlot) - 12]
                            self.stats.clearSetMove()
        slotNumber += 1
        return board

    def win(self, board):
        numberSlots = 10
        if board == [[] for x in range(numberSlots)]:
            print("You win!")
            response = input("New Game? (y/n):")
            if response == 'y' or response == 'Y':
                deck = self.createDecks()
                shuffledDeck = self.shuffle(deck)
                self.deal(board, shuffledDeck)
                self.showBoard(board)
            else:
                self.end()

    def draw(self, board, deck):
        for eachSlot in board:
            if eachSlot == []:
                print("Invalid Move.  All slots have at least one card.")
                return
        self.stats.moveLog.append(['Draw'])
        for eachSlot in board:
            deck[0].flip()
            eachSlot.append(deck[0])
            del deck[0]
        return board, deck

    def run(self):
        while self.cont == True:
            instruction, move = moveQueue
            if len(moveQueue) != 0:
                if instruction == 'Draw':
                    self.draw(self.board, self.deck)
                if instruction == 'Move':
                    self.move(move)
                if instruction == 'Exit':
                    self.end()
                if instruction == 'Undo':
                    self.undo(self.board)
            self.win(self.board)

    def undo(self, board):
        if self.stats.moveLog[len(self.stats.moveLog)-1][0] == 'Draw':
            position = 10
            for eachSlot in board:
                position -= 1
                self.deck.insert(0, board[position][len(board[position])-1])
                self.deck[0].flip()
                del board[position][len(board[position])-1]
 
        else:
            lastMove = self.stats.moveLog[len(self.stats.moveLog)-1]
            [fromSlot, numberCards, toSlot, underCardFlip] = [lastMove[2], lastMove[1], lastMove[0], lastMove[3]] 
            for eachCard in board[fromSlot-1][len(board[fromSlot-1])-numberCards:len(board[fromSlot-1])]:
                board[toSlot-1].append(eachCard)
            if underCardFlip == True:
                board[toSlot-1][len(board[toSlot-1])-numberCards-1].flip()
            del board[fromSlot-1][len(board[fromSlot-1])-numberCards:len(board[fromSlot-1])]
        self.stats.undoMove()
        return True, board
        
            

    #for debugging
    def findcards(self, board, shortCard):
        location = ""
        maxStack = 0
        for eachSlot in board:
            if len(eachSlot) > maxStack:
                maxStack = len(eachSlot)
        for x in range(0, len(board)):
            for y in range(0, len(board[x])):
                if board[x][y].shortHand() == shortCard:
                    location += " (" + str(x+1) + "," + str(maxStack - y) + ") "
        return location

    def end(self):
        self.cont = False
    
    class stats:
        def __init__(self):
            self.moveCount = 0
            self.score = 500
            self.moveLog = []

        def normalMove(self, move):
            self.moveCount += 1
            self.score -= 1
            self.moveLog.append(move)

        def clearSetMove(self):
            self.score += 101

        def undoMove(self):
            self.moveCount -= 1
            self.score -= 1
            del self.moveLog[len(self.moveLog)-1]

if __name__ == '__main__':
    game = spider()
    game.showBoard(game.board)
    while game.cont == True:
        game.inputMove(game.board, game.deck)
        game.win(game.board)
    else:
        print("Game over")