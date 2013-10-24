#! /usr/bin/env python

# Standard modules
import sys
from PokerBot import PokerBot

# Handle command line arguments
# [API Key]
if len(sys.argv) != 2:
    print "Usage: " + sys.argv[0] + " [API Key]"
    sys.exit(1)

api_key = sys.argv[1]
route = 'http://nolimitcodeem.com/api/players/' + api_key + "/"

sly = PokerBot(route)
sly.PlayTournament()
