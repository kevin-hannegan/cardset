import spidergame, os
from cardset import card

class spiderPlayer():
    def __init__(self):
        self.logFile = os.path.join("C:\\Users\\Kevin Hannegan\\Documents\\Visual Studio 2017\\Projects\\cardset\\cardset",'recursionlog.txt')
        if os._exists(self.logFile):
            os.remove(self.logFile)
        pass

    def availableMoves(self, board):
        # identify highest moveable card in each slot
        moveCards = []
        for slotNumber in range(0, len(board)):
            if len(board[slotNumber]) > 0:
                topSuit = board[slotNumber][len(board[slotNumber])-1].suit[0]
                topRank = board[slotNumber][len(board[slotNumber])-1].rank[0]
                matches = True
                numberCards = 1
                while matches == True:
                    if board[slotNumber][len(board[slotNumber]) - 1 - numberCards].faceUp == True:
                        if board[slotNumber][len(board[slotNumber]) - 1 - numberCards].suit[0] == topSuit:
                            if board[slotNumber][len(board[slotNumber]) - 1 - numberCards].rank[0] == topRank + numberCards:
                                numberCards += 1
                            else:
                                matches = False
                        else:
                            matches = False
                    else:
                        matches = False
                moveCards.append(numberCards)
            else:
                moveCards.append(0)
        
        # identify slots onto moveable cards could be played
        moveList = []
        for slot in range(0, len(board)):
            if len(board[slot]) > 0:
                cards = moveCards[slot]
                slotSize = len(board[slot])
                for cardNumber in range(0, cards):
                    playRank = board[slot][slotSize - 1 - cardNumber].rank[0]
                    for targetSlot in range(0, len(board)):
                        if len(board[targetSlot]) > 0:
                            slotRank = board[targetSlot][len(board[targetSlot]) - 1].rank[0]
                            if playRank == slotRank - 1:
                                 moveList.append([slot + 1, cardNumber + 1, targetSlot + 1])
                        else:
                            moveList.append([slot + 1, cardNumber + 1, targetSlot + 1])
        return moveList

    def sequenceSize(self, slotNumber, board):
        sequenceCount = 1
        if len(board[slotNumber-1]) > 2:
            lastRank = board[slotNumber -1][len(board[slotNumber -1])-1].rank[0]
            for i in range(len(board[slotNumber-1])-2, 0, -1):
                if board[slotNumber-1][i].faceUp is True:
                    nextRank = board[slotNumber-1][i].rank[0]
                    if nextRank == lastRank + 1:
                        sequenceCount += 1
                        lastRank = nextRank
                    else:
                        break
                else:
                    break
        return sequenceCount


    def bestMoves(self, moveList, board):
        if len(moveList) == 0:
            return []
        newMoveList = []
        moveScores = []
        for eachMove in moveList:
            [fromSlot, numberCards, toSlot] = eachMove
            fromSuit = board[fromSlot-1][len(board[fromSlot-1])-1].suit[0]
            topRank = board[fromSlot -1][len(board[fromSlot-1])-numberCards].rank[0] 

                # Better moves are matching suit or flip cards
            if len(board[toSlot -1]) == 0:
                moveScores.append(1)
            else:
                toSuit = board[toSlot -1][len(board[toSlot-1])-1].suit[0]
                underCardFaceUp =  board[fromSlot -1][len(board[fromSlot-1])-numberCards -1].faceUp
                if fromSuit == toSuit or underCardFaceUp is False:
                    moveScores.append(3)
                else:
                    fromSequence = self.sequenceSize(fromSlot, board)
                    toSequence = self.sequenceSize(toSlot, board)
                    if toSequence > fromSequence:
                        moveScores.append(2)
                    else:
                        moveScores.append(0)
        maxScore = max(moveScores)
        for i in range(0, len(moveScores)):
            if moveScores[i] == maxScore:
                newMoveList.append(moveList[i])
        return newMoveList
 

                # neutral moves add to sequence in non-matching suits

                # bad moves break matching suits





        return newMoveList

    def doBoardsMatch(self, board1, board2):
        for slotNumber in range(0, 10):
            b1SlotSize = len(board1[slotNumber])
            b2SlotSize = len(board2[slotNumber])
            if b1SlotSize != b2SlotSize:
                return False
            for cardNumber in range(0, b1SlotSize):
                card1 = board1[slotNumber][cardNumber]
                card2 = board2[slotNumber][cardNumber]
                if card1.suit != card2.suit or card1.rank != card2.rank or card1.faceUp != card2.faceUp:
                    return False
        return True

    def isBoardInLowerHistory(self, boardHistory, board, depth):
        for branchNumber in range(len(boardHistory)-2, 0, -1):
            branch = boardHistory[branchNumber]
            if len(branch) > depth:
                for counter in range(len(branch)-1, depth, -1):
                    if self.doBoardsMatch(branch[counter], board) is True:
                        return True
        return False

    def copyBoard(self, board, boardType=False):
        newBoard = []
        for eachSlot in board:
            newBoard.append([])
            for eachCard in eachSlot:
                suit = eachCard.suit
                rank = eachCard.rank
                faceUp = eachCard.faceUp
                newCard = card(suit, rank, faceUp)
                newBoard[len(newBoard)-1].append(newCard)
        if boardType is True:
            return newBoard
        immutableBoard = [tuple(slot) for slot in newBoard]
        return immutableBoard

    def boardString(self, board):
        newstring = ""
        for eachSlot in board:
            newstring += "[ "
            for eachCard in eachSlot:
                newstring += eachCard.shortHand(True) + " "
            newstring += "] "
        return newstring

    def deckString(self, deck):
        newString = ""
        for eachCard in deck:
            newString += eachCard.shortHand() + " "
        return newString


    def moveString(self, move):
        string = '-'.join([str(e) for e in move])
        return string

    def moveListString(self, moveList):
        string = ' '.join([self.moveString(move) for move in moveList])
        return string

    def log(self, branchNumber, depth, moveType, move, moves, board, deck):
        print()
        writeString = str(branchNumber) + ',' + str(depth) + ',' + moveType + ',' + self.moveString(move) + ',' + self.moveListString(moves) + '\n'
        with open(self.logFile, 'a') as log:
            log.write(writeString)

    def copyDeck(self, deck, deckType=False):
        tempDeck = []
        for eachCard in deck:
            tempDeck.append(card(eachCard.suit, eachCard.rank, eachCard.faceUp))
        if deckType is True:
            return tempDeck
        immutableDeck = tuple(tempDeck)
        return immutableDeck

    def bruteForceSolution(self, spider, board, deck, boardHistory=[[]], depth=0, branchNumber=0, topScore=0, deckHistory=[[]]):
        allMoves = self.availableMoves(board)
        # print (allMoves)
        moves = self.bestMoves(allMoves, board)
        print (moves)
        print ("                                                      depth: " + str(depth))
        spider.showBoard(board)
        boardHistory[branchNumber].append(self.copyBoard(board, False))
        deckHistory[branchNumber].append(self.copyDeck(deck))
        # need to filter move sequences that create infinite loops (e.g., search move log for loops and terminate)
        depth += 1

        terminateLoop = False
        winningBranch = False
        bestInstance = object()
        bestHistory = []
        winningSolutions = 0
        commandCode = 'Move'
   #     print("Score: " + str(spider.stats.score))
        if board == spider.winningBoard:
            terminateLoop = True
            winningBranch = True
            winningSolutions = 1
        if self.isBoardInLowerHistory(boardHistory, board, depth) is True:
            commandCode = 'Pass'
        else:
            for boardNumber in range(0, len(boardHistory[branchNumber])-1):
                if boardNumber > 0:
                    # print("Previous Board:", self.doBoardsMatch(boardHistory[branchNumber][boardNumber-1], board))
                    if self.doBoardsMatch(boardHistory[branchNumber][boardNumber], board) is True or len(moves) == 0:

                        if len(deck) == 0:
                            terminateLoop = True
                            winningBranch = False
                            commandCode = 'Pass'
                            break
                        else:
                            # add code for empty slots to generate move command - ok
                            slotSizes = [len(slot) for slot in board]
                            commandCode = 'Draw'
                            for size in slotSizes:
                                if size == 0:
                                    commandCode = 'Move'
                                    break
                            break
                    else:
                        commandCode = 'Move'    
        if commandCode == 'Draw':
            drawsRemaining = int(len(deck) / 10)
            if drawsRemaining > 0:
                board, deck = spidergame.spider.draw(spider, board, deck)
            
                print ("Draws Remaining: " + str(drawsRemaining))
                self.log(branchNumber, depth, commandCode, [], [], board, deck)
                winningBranch, blank, boardHistory, winningSolutions, branchNumber, topScore = self.bruteForceSolution(spider, board, deck, boardHistory, depth, branchNumber, topScore, deckHistory)
        if commandCode == 'Move':
            for moveNumber in range(0, len(moves)):
                if moveNumber > 0:
                    boardHistory.append(boardHistory[branchNumber][0:depth])
                    deckHistory.append(deckHistory[branchNumber][0:depth])
                    branchNumber += 1
                    board = self.copyBoard(boardHistory[branchNumber][depth-1], True)
                    deck = self.copyDeck(deckHistory[branchNumber][depth-1], True)
         
                [fromSlot, numberCards, toSlot] = moves[moveNumber]
                success, board = spidergame.spider.move(spider, board, fromSlot, numberCards, toSlot)
            # if win, then note elevate game information (e.g., data in game.stats)
            # ifboard returns to a previous state, then caught infinite loop, so draw or terminate branch
            # fix so len(boardHistory) and depth remain equal.  when adding a new branch, add boardHisotry from all higher depths
                if depth < 200:
                    self.log(branchNumber, depth, commandCode, moves[moveNumber], moves, board, deck)
                    winningBranch, blank, boardHistory, winningSolutions, branchNumber, topScore = self.bruteForceSolution(spider, board, deck, boardHistory, depth, branchNumber, topScore, deckHistory)

        if spider.stats.score > topScore and winningBranch == True:
            topScore = spider.stats.score
            bestInstance = spider
            bestHistory = boardHistory[branchNumber]
            winningSolutions += winningSolutions
        return winningBranch, bestInstance, boardHistory, winningSolutions, branchNumber, topScore



             


        # consolidate stats across games (e.g., min moves, highest score, number of possible solutions, initial board and deck state)

if __name__ == '__main__':
    game = spidergame.spider()
    player = spiderPlayer()
    game.showBoard(game.board)
    player.availableMoves(game.board)
    cont = False
    while cont == True:
        game.inputMove(game.board, game.deck)
        game.win(game.board)
        moves = player.availableMoves(game.board)
        print(moves)
    player.bruteForceSolution(game, game.board, game.deck)

