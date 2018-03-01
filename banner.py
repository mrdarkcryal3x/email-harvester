#!/usr/bin/python

import sys

try:
    from colors import Colors
except ImportError:
    print 'Make sure you have all required packages'
    sys.exit(1)

class Banner:
    
    def __init__(self):
        colors = Colors()
        green = colors.green()
        reset = colors.reset()
    
        print green +  """
            Simple Email Harvester
            This tools allows to scrape websites for emails
            Usage: ./email_harvester.py --url http://www.example.com --file example_emails.txt
                
                """ +  reset
