from typing import ClassVar

from ._strs import GVASStrProperty


class GVASNameProperty(GVASStrProperty):
    __slots__ = ()

    _TYPE: ClassVar[str] = "Name"
