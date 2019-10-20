"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    def at_object_creation(self):
        # create and initialize character's attributes
        self.db.attributes = {'strength': 0, 'charisma': 0, 'intelligence': 0, 'supernatural': 0, 'calm': 0}
        self.db.values = [-1, 0, 1, 2, 3]
        self.db.description = 'This player has yet to set their description.'

    def return_appearance(self, looker):
        return self.db.desc

    def set_description(self, desc):
        self.db.description = desc

    def set_attribute(self, attr, value):
        if not value in self.db.values:
            self.msg('Please supply a valid value.\n{}'.format(' '.join([str(value) for value in self.db.values])))
            return False
        attr = attr.lower()
        if not attr in self.db.attributes.keys():
            self.msg('Please supply a valid attribute.\n{}'.format(' '.join(self.db.attributes.keys())))
            return False
        self.db.attributes[attr] = value
        self.db.values.remove(value)
        self.msg('{} set to {}'.format(attr.capitalize(), value))

    def get_attributes(self):
        for key in self.db.attributes.keys():
            self.msg('{}: {}'.format(key.upper(), self.db.attributes[key]))
    
    def reset(self):
        for key in self.db.attributes.keys():
            self.db.attributes[key] = 0
        self.db.values = [-1, 0, 1, 2, 3]
