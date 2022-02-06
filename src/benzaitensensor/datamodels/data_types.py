"""Defines a data manipulation protocol"""
import datetime
import decimal
import typing

DataType: typing.TypeAlias = typing.Union[
    str,
    int,
    float,
    bool,
    decimal.Decimal,
    bytes,
    datetime.datetime,
    datetime.date,
]


class DataObject(typing.Protocol):
    """Defines a type that can be casted to a storable datatype"""

    def to_item_map(self) -> dict[str, DataType]:
        """Converts to a list of key, value pairs that can be used in the any data interface"""
        ...

    @classmethod
    def attributes(
            cls) -> typing.Tuple[dict[str, typing.Type[DataType]],
                                 dict[str, typing.Type[DataType]]]:
        """Returns a tuple (attributes, keys) for map (attribute name -> attribute type)"""
        ...

    @classmethod
    def get_data_interface_params(cls) -> dict[str, typing.Any] | None:
        """Provide parameters that might be required by the data interface"""
        ...


ItemMap: typing.TypeAlias = dict[str, DataType] | DataObject
