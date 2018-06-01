"""
Module providing world / map representing game terrain.
"""
import abc
from abc import ABC


class World(ABC):
    """
    Class representing a game world. Cannot be initialized
    directly; see children.
    """
    @abc.abstractmethod
    def __init__(self, title="default_title", files=None):
        """
        Initialize a new world object, optionally from a file.
        Files is a dictionary of form:
        Key[type] = Value[(filename, filetype)]
        where type =
        "characters" OR "features" OR "structures" OR "entities"
        filename is a string relative / absolute path
        filetype =
        "pickle" OR "json"
        """
        self.title = title
        self.files = files
        # see above
        self.characters = dict()
        # KEY[id] = VALUE[character]
        self.features = dict()
        # KEY[id] = VALUE[feature]
        self.structures = dict()
        # KEY[id] = VALUE[structure]
        self.entities = dict()
        # KEY[id] = VALUE[entity]
        self.locations = dict()
        # KEY[(x, y, <z>) = VALUE[entity_id]
        # x, y, z in cm
        self._dictionaries = [self.characters,
                              self.features,
                              self.structures,
                              self.entities,
                              self.locations]

    @abc.abstractmethod
    def __str__(self):
        """
        Return text information about the world.
        """

    def add(self, obj, update=True):
        """
        Adds an object to the world's data dictionaries.
        """
        for dictionary in self._dictionaries:




class Circle_World(World):
    """
    Class representing a flat, circular world.
    Dimensionality not defined.
    """
    def __init__(self, title="Default title", files=None):
        super().__init__(title, files)

    def __str__(self):
        """
        Display title, radius, other information.
        """
        ret = ["World: {}".format(self.title)]
        ret.append("Type: Circle")
        ret.append("Radius: {}".format(self.radius))

        return "\n".join(ret)


class Rect_World(World):
    """
    Class representing a flat, rectangular world.
    Dimensionality not defined.
    """
    def __init__(self, title="default_title", files=None):
        super().__init__(title, files)


if __name__ == "__main__":
    pass
