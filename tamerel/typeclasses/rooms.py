"""
Room

Rooms are simple containers that has no location of their own.

"""

from commands.default_cmdsets import CharGenCmdSet
from evennia import DefaultRoom


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    pass

class CharGen(Room):
    def at_object_creation(self):
        self.cmdset.add(CharGenCmdSet, permanent=True)
