from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterRequest(_message.Message):
    __slots__ = ["y1", "y2", "p"]
    Y1_FIELD_NUMBER: _ClassVar[int]
    Y2_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    y1: str
    y2: str
    p: str
    def __init__(self, y1: _Optional[str] = ..., y2: _Optional[str] = ..., p: _Optional[str] = ...) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ["id", "error"]
    ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    id: str
    error: str
    def __init__(self, id: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class LoginRequestRoundOne(_message.Message):
    __slots__ = ["id", "r1", "r2"]
    ID_FIELD_NUMBER: _ClassVar[int]
    R1_FIELD_NUMBER: _ClassVar[int]
    R2_FIELD_NUMBER: _ClassVar[int]
    id: str
    r1: str
    r2: str
    def __init__(self, id: _Optional[str] = ..., r1: _Optional[str] = ..., r2: _Optional[str] = ...) -> None: ...

class LoginResponseRoundOne(_message.Message):
    __slots__ = ["c", "error"]
    C_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    c: str
    error: str
    def __init__(self, c: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class LoginRequestRoundTwo(_message.Message):
    __slots__ = ["id", "s"]
    ID_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    id: str
    s: str
    def __init__(self, id: _Optional[str] = ..., s: _Optional[str] = ...) -> None: ...

class LoginResponseRoundTwo(_message.Message):
    __slots__ = ["b", "error"]
    B_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    b: bool
    error: str
    def __init__(self, b: bool = ..., error: _Optional[str] = ...) -> None: ...
