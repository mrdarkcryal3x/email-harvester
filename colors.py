#!/usr/bin/python

class Colors:
    
    def red(self):
        return "\033[1;31m"
    def green(self):
        return "\033[0;32m"
    def blue(self):
        return "\033[1;34m"
    def reset(self):
        return "\033[0;0m"
