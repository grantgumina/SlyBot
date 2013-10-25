class Card:
    def __init__(self, cardstr):
        self.name = cardstr[0].upper()
        self.name = str(self.name)
        self.rank = 0
        if self.name == 'T':
            self.rank = 10
        elif self.name == 'J':
            self.rank = 11
        elif self.name == 'Q':
            self.rank == 12
        elif self.name == 'K':
            self.rank == 13
        elif self.name == 'A':
            self.rank == 14
        else:
            self.rank = int(self.name)

        print self.name + "--> " + str(self.rank)

        self.suit = cardstr[1]
        
