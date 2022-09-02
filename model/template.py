from abc import ABC, abstractproperty


class DBModel(ABC): 
    """
        Abstract class that defines the structure of models
    """

    @abstractproperty
    def STRUCTURE(): ...

    @abstractproperty
    def TABLE(): ...

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {vars(self)}>"