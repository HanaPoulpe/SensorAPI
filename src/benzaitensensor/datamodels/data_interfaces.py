"""Defines abstract data interfaces"""
import typing

from .data_types import DataObject, ItemMap


class DataCursor(typing.Protocol):
    """
    Defines a cursor used to read/write data.

    The cursor is an active connection point to the back-end.
    """

    def read(
        self,
        keys: dict[str, ItemMap],
        cls: typing.Type[DataObject],
    ) -> typing.Iterable[DataObject]:
        """Read a data objects from specified keys"""
        ...

    def write(self, data: DataObject, no_wait: bool = False):
        """
        Write a data object to the storage

        :param data: Data object to write
        :param no_wait: If set to true, the call will return before the write operation being
        completed
        """
        ...

    def write_many(self, datas: typing.Iterable[DataObject], no_wait: bool = False):
        """
        Write multiple objects to the storage

        :param datas: Iterable of homogeneous data object to write
        :param no_wait: If set to true, the call will return before the write operation being
        completed
        """
        ...

    def close(self):
        """Operation to cleanup after any data operations"""
        ...


class DataInterface(typing.Protocol):
    """
    Defines Data Interface protocol

    Defines an interface with the back-end, this is a inactive connection that can be opened
    using the open method. Once opened data can be manipulated using the cursor returned by the
    open method.
    """

    def setup(self, *args, **kwargs):
        """Defines the operation to setup the data interface"""
        ...

    def connect(self) -> DataCursor:
        """Operations to run prior any data operations"""
        ...

    def close(self):
        """Operation to cleanup after any data operations"""
        ...

    def __enter__(self) -> DataCursor:
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...


class MakeContextManager:
    """
    Adds __enter__ and __exit__ to classes that implements DataInterface

    This decorator adds
    * __enter__(self) -> DataCursor
    * __exit__(self, exc_type, exc_val, exc_tb)
    * __connection: DataCursor

    This implementation is not safe to use with asynchronous calls from the same DataInterface
    instance.

    >>>@MakeContextManager()  # Brackets are mandatory with this decorator
    >>>class MyDatainterface:
    >>>    def setup(self, *args, *kwargs):
    >>>      pass
    >>>
    >>>    def connect(self):
    >>>        return DataCursor()
    >>>
    >>>    def close(self):
    >>>        pass
    """

    def __call__(self, cls: typing.Type[DataInterface]) -> typing.Type[DataInterface]:
        """Add methods the to class passed in argument"""
        if not hasattr(cls, "connect") or not hasattr(cls, "close"):
            raise TypeError(
                f"{self.__class__.__name__} must be used with classes implementing"
                f"{__name__}.DataInterface",
            )

        def enter(slf: DataInterface) -> DataCursor:
            """Default __enter__"""
            # We overload slf to create a __connection attribute
            # Ignore type as we willingly mutate the object.
            connection = slf.connect()
            setattr(slf, "__connection", connection)  # noqa
            return connection  # type: ignore

        def ext(slf: DataInterface, *args, **kwargs):
            """Default __exit__"""
            # This expects to contain a __connection attribute created by enter
            try:
                getattr(slf, "__connection").close()  # noqa
            finally:
                delattr(slf, "__connection")
                slf.close()

        cls.__enter__ = enter
        cls.__exit__ = ext

        return cls
