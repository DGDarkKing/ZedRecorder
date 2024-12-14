import abc
from enum import Enum
from typing import Union, Optional

from PySide6 import QtCore
from PySide6.QtGui import QImage


class RecorderStates(Enum):
    RECORD = 1,
    PAUSE = 2
    NOT_RECORD = 3


class Recorder(QtCore.QThread):
    _image_signal = QtCore.Signal(QImage)
    _exception_signal = QtCore.Signal(Exception)

    def __init__(self):
        super().__init__()
        self._file_name = ''
        self._state = RecorderStates.NOT_RECORD
        self._do_work = True

    @property
    def state(self):
        return self._state

    @abc.abstractmethod
    def finish_work(self):
        self._do_work = False

    @abc.abstractmethod
    def _stop_work(self):
        ...

    def __del__(self):
        self._stop_work()

    @abc.abstractmethod
    def run(self) -> None:
        ...

    @property
    def image_signal(self):
        return self._image_signal

    @property
    def exception_signal(self):
        return self._exception_signal

    def record(self, file_name: str = '') -> Optional[str]:
        if self._state == RecorderStates.RECORD:
            return

        result_file_name = None
        if self._state == RecorderStates.NOT_RECORD:
            result_file_name = self._start_record(file_name)
        else:
            self._continue_record()
        self._state = RecorderStates.RECORD
        return result_file_name

    def pause(self) -> None:
        if self._state in (RecorderStates.NOT_RECORD, RecorderStates.PAUSE):
            return None

        self._pause_record()
        self._state = RecorderStates.PAUSE

    def stop(self) -> Union[None, str]:
        if self._state == RecorderStates.NOT_RECORD:
            return

        file_name = self._stop_record()
        self._state = RecorderStates.NOT_RECORD
        return file_name

    @abc.abstractmethod
    def _start_record(self, file_name: str) -> str:
        ...

    @abc.abstractmethod
    def _pause_record(self) -> None:
        ...

    @abc.abstractmethod
    def _continue_record(self) -> None:
        ...

    @abc.abstractmethod
    def _stop_record(self) -> str:
        ...
