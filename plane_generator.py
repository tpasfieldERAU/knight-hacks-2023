import random as rnd
from math import sin, cos, pi

mods = ["B707",
        "B717",
        "B727",
        "B737",
        "B747",
        "B757",
        "B767",
        "B777",
        "B787",
        "A319"
        "A320",
        "A321",
        "A330",
        "A340",
        "A350",
        "A360",
        "PA40",
        "DA42",
        "C130",
        "C17",
        "C5",
        "B1",
        "B2",
        "B21",
        "A12",
        "A10",
        "F-4",
        "F-14",
        "F-15",
        "F-16",
        "F/A-18",
        "F-22",
        "F-35",
        "F-111",
        "E-4"]

class Plane:
    def __init__(self, reg, mod, lat, lon, alt, vspeed, hspeed, head, arv=None, dep=None):
        self.reg = reg
        self.mod = mod
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.vspeed = vspeed
        self.hspeed = hspeed
        self.head = head
        self.arv = arv
        self.dep = dep

    def timeStep(self):
        self.alt = self.alt + self.vspeed * 15.0  # Reduce altitude
        self.vspeed += rnd.gauss(0.0, 7.5) # Change vertical speed
        self.lat += ((self.hspeed * 1.68781) * sin(pi * self.head / 180.0) * 15.0) / 364000.0
        self.lon += ((self.hspeed * 1.68781) * cos(pi * self.head / 180.0) * 15) / 327360.0
        self.hspeed += rnd.gauss(0.0, 2.0)
        self.head += rnd.gauss(0.0, 1.0)