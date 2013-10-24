import urllib2
import json
import time

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
        # data = "action_name=call" 
        data = "action_name=bet&amount=222"
        urllib2.urlopen(self.route + "action", data)


        print "Took an action!"



        
