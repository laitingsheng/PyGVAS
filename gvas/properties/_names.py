from typing import ClassVar

from ._strs import GVASStrProperty, GVASStrPropertyArray


class GVASNameProperty(GVASStrProperty):
    __slots__ = ()

    _ACCEPT: ClassVar[str] = "NameProperty"


class GVASNamePropertyArray(GVASStrPropertyArray):
    __slots__ = ()

    _ACCEPT: ClassVar[str] = "NameProperty"
