#!/usr/bin/env python
from entity import Entity
import os

def floot(arg1):
    """Wrapper for float() that handles "D" exponential notation"""
    try:
        f = float(arg1)
    except ValueError:
        f = float(arg1.replace("D","E").replace("d","e"))
    return f

class GeneralNote(Entity):
    """General Note
    IGES Spec v5.3 p. 229 Section 4.60
    """

    def add_parameters(self, parameters):
        self.NS = int(parameters[1])
        self.text_strings = []
        for start in xrange(2, self.NS * 12, 12):
            self.text_strings.append({'NC': int(parameters[start]),
                                      'WT': floot(parameters[start + 1]),
                                      'HT': floot(parameters[start + 2]),
                                      'FC': int(parameters[start + 3]),
                                      'SL': floot(parameters[start + 4]),
                                      'A': floot(parameters[start + 5]),
                                      'M': int(parameters[start + 6]),
                                      'H': int(parameters[start + 7]),
                                      'XS': floot(parameters[start + 8]),
                                      'YS': floot(parameters[start + 9]),
                                      'ZS': floot(parameters[start + 10]),
                                      'TEXT':'H'.join(parameters[start + 11].split('H')[1:])})
    def __str__(self):
        s = '--- General Note ---' + os.linesep
        s += Entity.__str__(self) + os.linesep
        s += '-- Parameter Data --' + os.linesep
        s += str(self.NS) + os.linesep
        for ts in self.text_strings:
            s += str(ts) + os.linesep
     #   s += str(self.T) + os.linesep
      #  s += str(self.W) + os.linesep
       # s += str(self.control_points) + os.linesep
       # s += "Parameter: v(0) = {0}    v(1) = {1}".format(self.V0, self.V1) + os.linesep
        #if self.planar_curve:
         #   s += "Unit normal: {0} {1} {2}".format(self.XNORM, self.YNORM, self.ZNORM)
        return s

