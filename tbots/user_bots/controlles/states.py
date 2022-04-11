from enum import Enum, auto


class ChangeAccountSts(Enum):
    WAITING_API_ID = auto()
    WAITING_API_HASH = auto()
