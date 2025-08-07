from typing import ClassVar

from ._strs import GVASStrProperty, GVASStrPropertyArray


class GVASObjectProperty(GVASStrProperty):
    __slots__ = ()

    _ACCEPT: ClassVar[str] = "ObjectProperty"


class GVASObjectPropertyArray(GVASStrPropertyArray):
    __slots__ = ()

    _ACCEPT: ClassVar[str] = "ObjectProperty"
