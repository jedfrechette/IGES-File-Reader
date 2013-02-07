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

class Line(Entity):
    """Straight line segment"""

    def add_parameters(self, parameters):
        self.x1 = floot(parameters[1])
        self.y1 = floot(parameters[2])
        self.z1 = floot(parameters[3])
        self.x2 = floot(parameters[4])
        self.y2 = floot(parameters[5])
        self.z2 = floot(parameters[6])

    def __str__(self):
        s = '--- Line ---' + os.linesep
        s += Entity.__str__(self) + os.linesep
        s += "From point {0}, {1}, {2} {3}".format(self.x1, self.y1, self.z1, os.linesep)
        s += "To point {0}, {1}, {2}".format(self.x2, self.y2, self.z2)
        return s

class RationalBSplineCurve(Entity):
    """Rational B-Spline Curve
    IGES Spec v5.3 p. 123 Section 4.23
    See also Appendix B, p. 545
    """

    def add_parameters(self, parameters):
        self.K = int(parameters[1])
        self.M = int(parameters[2])
        self.prop1 = int(parameters[3])
        self.prop2 = int(parameters[4])
        self.prop3 = int(parameters[5])
        self.prop4 = int(parameters[6])
        
        self.N = 1 + self.K - self.M
        self.A = self.N + 2 * self.M

        # Knot sequence
        self.T = []
        for i in range(7, 7 + self.A + 1):
            self.T.append(floot(parameters[i]))

        # Weights
        self.W = []
        for i in range(self.A + 8, self.A + self.K + 8):
            self.W.append(floot(parameters[i]))

        # Control points
        self.control_points = []
        for i in range(9 + self.A + self.K, 9 + self.A + 4*self.K + 1, 3):
            point = (floot(parameters[i]), floot(parameters[i+1]), floot(parameters[i+2]))
            self.control_points.append(point)

        # Parameter values
        self.V0 = floot(parameters[12 + self.A + 4 * self.K])
        self.V1 = floot(parameters[13 + self.A + 4 * self.K])

        # Unit normal (only for planar curves)
        if len(parameters) > 14 + self.A + 4 * self.K + 1:
            self.planar_curve = True
            self.XNORM = floot(parameters[14 + self.A + 4 * self.K])
            self.YNORM = floot(parameters[15 + self.A + 4 * self.K])
            self.ZNORM = floot(parameters[16 + self.A + 4 * self.K])
        else:
            self.planar_curve = False

    def __str__(self):
        s = '--- Rational B-Spline Curve ---' + os.linesep
        s += Entity.__str__(self) + os.linesep
        s += str(self.T) + os.linesep
        s += str(self.W) + os.linesep
        s += str(self.control_points) + os.linesep
        s += "Parameter: v(0) = {0}    v(1) = {1}".format(self.V0, self.V1) + os.linesep
        if self.planar_curve:
            s += "Unit normal: {0} {1} {2}".format(self.XNORM, self.YNORM, self.ZNORM)
        return s


    def __str__(self):
        s = '--- Rational B-Spline Curve ---' + os.linesep
        s += Entity.__str__(self) + os.linesep
        s += str(self.T) + os.linesep
        s += str(self.W) + os.linesep
        s += str(self.control_points) + os.linesep
        s += "Parameter: v(0) = {0}    v(1) = {1}".format(self.V0, self.V1) + os.linesep
        if self.planar_curve:
            s += "Unit normal: {0} {1} {2}".format(self.XNORM, self.YNORM, self.ZNORM)
        return s

