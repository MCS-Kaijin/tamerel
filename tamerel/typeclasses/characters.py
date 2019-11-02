"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
import random

from evennia import DefaultCharacter
from evennia.utils.create import create_object

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
        self.db.attributes = {'strength': 0, 'charisma': 0, 'intelligence': 0, 'supernatural': 0, 'calm': 0, 'health': 10}
        self.db.values = [-1, 0, 1, 2, 3]
        self.db.description = 'This player has yet to set their description.'
        self.db.humanity = 100
        self.db.is_lord = False

    def return_appearance(self, looker):
        string = 'They appear to be Immortal Man like yourself.'
        if self.db.attributes['health'] > 7:
            string += ' They are in good health!'
        elif self.db.attributes['health'] > 5:
            string += ' They are looking a little rough.'
        elif self.db.attributs['health'] > 1:
            string += ' They don\'t look too good.'
        else:
            string += ' They should be down!'
        if self.db.is_lord:
            string += ' They have a hollow look in their eyes....'
        return string

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
    
    def set_attribute_ADMIN(self, attr, value):
        self.db.attributes[attr] = value

    def annhilate_ADMIN(self):
        self.reset()
        self.move_to(self.search('Limbo'))

    def get_attributes(self):
        for key in self.db.attributes.keys():
            self.msg('{}: {}'.format(key.upper(), self.db.attributes[key]))
    
    def reset(self):
        for key in self.db.attributes.keys():
            self.db.attributes[key] = 0
        self.db.values = [-1, 0, 1, 2, 3]

    def roll_plus_attr(self, attr):
        base = random.randint(2, 12)
        return base + self.db.attributes[attr]

    def str_miss(self, doer):
        doer.db.humanity -= 1
        doer.location.msg_contents('{} tried to attack {} but missed!'.format(doer.key, self.key))
        doer.check_humanity()

    def str_mixed_success(self, doer):
        doer.db.humanity -= 5
        doer.location.msg_contents('{} attacked {}!'.format(doer.key, self.key))
        doer.check_humanity()

    def str_success(self, doer):
        doer.db.humanity -= 10
        doer.location.msg_contents('{} brutally mauled {}!'.format(doer.key, self.key))
        doer.check_humanity()

    def check_humanity(self):
        if self.db.humanity <= 0:
            self.db.humanity = 0
            self.msg('You are no longer human!')
            ft = create_object('objects.Object',
                    key='Fate Token',
                    location=self.location)


class Horror(Character):
    def at_object_creation(self):
        Character.at_object_creation(self)
        self.db.humanity = 0
    
    def str_miss(self, doer):
        doer.msg('You missed {}.'.format(self.key))

    def str_mixed_success(self, doer):
        self.db.attributes['health'] -= 3
        doer.db.humanity += 1
        doer.msg('You hit {}.'.format(self.key))
        self.check_health()

    def str_success(self, doer):
        self.db.attributes['health'] -= 5
        doer.db.humanity += 1
        doer.msg('You hit {} hard!'.format(self.key))
        self.check_health()

    def check_health(self):
        if self.db.attributes['health'] <= 0:
            self.location.msg_contents('{} cries out in pain as it collapses back into dark magical energy!'.format(self.key.capitalize()))
            self.delete()
