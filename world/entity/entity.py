"""
Module providing an entity class representing a 
body with mass, location, and velocity.
"""
from abc import ABC
import abc


class Entity(ABC):
    """
    Class representing body potentially in motion.
    """
    @abc.abstractmethod
    def __init__(self):
        """
        Initialize a new entity.
        """

    @abc.abstractmethod
    def intersect(self, other_entity):
        """
        Method to return whether or not this entity is intersecting
        another given entity.
        """


if __name__ == "__main__":
    pass
