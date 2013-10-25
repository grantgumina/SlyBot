import urllib2
import json
import time
from Card import Card
import random

class PokerBot:
    def __init__(self, route):
        self.route = route
        self.time_since_last_call = time.time()
        self.game_state = {}
        
    def PlayTournament(self):
        print "And hereeeeee weeeeeee....."
        print "Go."
        print self.route
        self.GameLoop()
    
    def GameLoop(self):
        while(1):
            if (self.HasBeenOneSecond()):
                self.UpdateGameState()

                # Check if it is our turn
                if (self.game_state['your_turn'] == True):
                    self.MakeMove()
                else:
                    print "It is not our turn yet."

    def UpdateGameState(self):
        # Get game state from the server
        text_response = urllib2.urlopen(self.route)
        self.game_state = json.load(text_response)
        self.UpdateSecondCounter() # Since we made a server request


    def HasBeenOneSecond(self):
        time_now = time.time()
        return time_now - self.time_since_last_call >= 1

    def UpdateSecondCounter(self):
        self.time_since_last_call = time.time()

    def MakeMove(self):
        # Determine the move to make here
       #a = self.GetAction()
       # print 'Return action: ' + a
       # action = 'check'
       # if a == 'check':
       #     if int(self.game_state['call_amount']) == 0:
       #         action = 'check'
       #         print 'We checked'
       #     else:
       #         action = 'fold'
       #         print 'We folded'
       # elif a == 'call':
       #     action = 'call'
       #     print 'We called'
       # elif a == 'small_bet':
       #     action = 'bet&amount=20'
       #     print 'We bet small'
       # elif a == 'large_bet':
       #     action = 'bet&amount=50'
       #     print 'We bet big'
       # elif a == 'all_in':
       #     action = 'bet&amount=1000000'
       #     print 'Fuck it, lets go all in'

        # data = "action_name=call" 
        # data = "action_name=" + action
        r1 = random.randint(1, 10)
        if r1 < 4:
            r = random.randint(200,400)
            bet = str(r)
            if r == 52:
                bet = "100"
            print "Betting: " + bet
            data = "action_name=bet&amount=" + bet
            urllib2.urlopen(self.route + "action", data)
        elif r1 < 10:
            data = "action_name=call"
            urllib2.urlopen(self.route + "action", data)
        else:
            if self.game_state['current_bet'] > 30:
                data = 'action_name=call'
                print "calling"
                urllib2.urlopen(self.route + "action", data)
            else:
                bet = "0"
                print "Betting: " + bet
                data = "action_name=bet&amount=" + bet
                urllib2.urlopen(self.route + "action", data)

    def GetAction(self):
        hand = [Card(h) for h in self.game_state['hand']]
        #print str(hand[0].rank) + str(hand[0].suit)
        #print str(hand[1].rank) + str(hand[1].suit)

        cards_on_board = len(self.game_state['community_cards'])
        print 'There are:' + str(cards_on_board) + ' cards on the board'

        if cards_on_board == 0:
            print hand[0].rank
            print hand[1].rank
            if hand[0].rank == hand[1].rank:
                # We have a pair
                if hand[0].rank <= 8:
                    print 'We have a low pocket pair'
                    return 'call'
                else:
                    print 'We have a high pocket pair'
                    return 'small_bet'
            
            highRank = max([hand[0].rank, hand[1].rank])
            if  highRank == '14':
                # Bet the ace
                return 'small_bet'
            elif highRank == '13':
                # Call the King
                return 'call'
            else:
                return 'check'

        elif cards_on_board >= 3:
           t = self.GetHandTypes()
           print "We have a: " + t
           if t == 'high_card':
               return 'check'
           elif t == 'pair':
               if hand[0].rank == 14:
                   return 'small_bet'
               elif hand[0].rank >= 12:
                   return 'call'
               else:
                   return 'check'
           elif t == 'three_of_a_kind':
               return 'small_bet'
           elif t == 'four_of_a_kind':
               return 'all_in'
           elif t == 'full_house':
               return 'all_in'
    
    def GetHandTypes(self):
        hand = [Card(h) for h in self.game_state['hand']]
        community = [Card(c) for c in self.game_state['community_cards']]
        

        # Make a dictionary of all of our matches 
        matches = {}
        if hand[0].rank == hand[1].rank:
            matches[hand[0].rank] = 2
            hc = matches[0]
            for bc in community:
                if hc == bc.rank:
                    matches[hc] = matches[hc] + 1
        else:
            for hc in hand:
                for bc in community:
                    if hc.rank == bc.rank:
                        if hc.rank not in matches.keys():
                            matches[hc.rank] = 2
                        else:
                            matches[hc.rank] = matches[hc.rank] + 1
        
        if len(matches.keys()) == 2:
            for v in matches.values:
                if v == 3:
                    # Full House FUCK YEA!!!
                    return 'full_house'
                else:
                    # Two pair
                    return 'two_pair'
        if len(matches.keys()) == 1:
            rank = matches.keys()[0]
            num_matches = matches[rank]
            if num_matches == 4:
                return 'four_of_a_kind'
            elif num_matches == 3:
                return 'three_of_a_kind'
            elif num_matches == 2:
                return 'pair'

        # Check if we have a flush
           # Check if we have a straight flush 
        # Check if we have a straight

        return 'high_card'

        
