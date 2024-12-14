from enum import Enum


class CloseStatus(Enum):
    SUCCESS = 1
    CLOSED = 0
    RECORDING = -1
