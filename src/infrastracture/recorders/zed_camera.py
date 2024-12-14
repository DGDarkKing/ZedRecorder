import time
from enum import Enum
from pathlib import Path

import numpy as np
from PySide6 import QtCore

import pyzed.sl as sl
from typing_extensions import Type

from infrastracture.recorders.recorder import Recorder, RecorderStates
from infrastracture.recorders.schemas.close_status import CloseStatus
from infrastracture.recorders.schemas.open_status import OpenStatus
from infrastracture.recorders.schemas.resolution import Resolution
from infrastracture.recorders.schemas.settings import Settings, SetSettings


class ZedCamera(Recorder):
    __DEFAULT_RESOLUTION = sl.RESOLUTION.HD1080
    __DEFAULT_FPS = 30

    __USB_MODELS = (sl.MODEL.ZED, sl.MODEL.ZED2, sl.MODEL.ZED2i, sl.MODEL.ZED_M)
    __GMSL_MODELS = (sl.MODEL.ZED_X, sl.MODEL.ZED_XM)

    class UsbCameraResolution(Enum):
        VGA = sl.RESOLUTION.VGA.value
        HD720 = sl.RESOLUTION.HD720.value
        HD1080 = sl.RESOLUTION.HD1080.value
        HD2K = sl.RESOLUTION.HD2K.value

    class GmslCameraResolution(Enum):
        SVGA = sl.RESOLUTION.SVGA.value
        HD1080 = sl.RESOLUTION.HD1080.value
        HD1200 = sl.RESOLUTION.HD1200.value

    class Fps(Enum):
        FPS15 = 15
        FPS30 = 30
        FPS60 = 60
        FPS100 = 100
        FPS120 = 120

    __USB_RULES = {
        UsbCameraResolution.VGA.value: tuple(fps.value for fps in (Fps.FPS15, Fps.FPS30, Fps.FPS60, Fps.FPS100)),
        UsbCameraResolution.HD720.value: tuple(fps.value for fps in (Fps.FPS15, Fps.FPS30, Fps.FPS60)),
        UsbCameraResolution.HD1080.value: tuple(fps.value for fps in (Fps.FPS15, Fps.FPS30)),
        UsbCameraResolution.HD2K.value: tuple(fps.value for fps in (Fps.FPS15,)),
    }

    __GMSL_RULES = {
        GmslCameraResolution.SVGA.value: tuple(fps.value for fps in (Fps.FPS15, Fps.FPS30, Fps.FPS60, Fps.FPS120)),
        GmslCameraResolution.HD1080.value: tuple(fps.value for fps in (Fps.FPS15, Fps.FPS30, Fps.FPS60)),
        GmslCameraResolution.HD1200.value: tuple(fps.value for fps in (Fps.FPS15, Fps.FPS30, Fps.FPS60)),
    }

    __ZED_RESOLUTION_TO_COMMON_RESOLUTION = {
        sl.RESOLUTION.VGA: Resolution.VGA,
        sl.RESOLUTION.SVGA: Resolution.SVGA,
        sl.RESOLUTION.HD720: Resolution.HD720,
        sl.RESOLUTION.HD1080: Resolution.HD1080,
        sl.RESOLUTION.HD1200: Resolution.HD1200,
        sl.RESOLUTION.HD2K: Resolution.HD2K,
    }

    __COMMON_RESOLUTION_TO_ZED_RESOLUTION = {
        common: zed
        for zed, common in __ZED_RESOLUTION_TO_COMMON_RESOLUTION.items()
    }

    def __init__(self):
        super().__init__()
        self.__camera = sl.Camera()
        self.__init = sl.InitParameters()
        self.__init.camera_fps = self.__DEFAULT_FPS
        self.__init.camera_resolution = self.__DEFAULT_RESOLUTION
        self.__init.depth_mode = sl.DEPTH_MODE.NONE
        self.__settings = self.__get_settings()
        self.__model: sl.MODEL | None = None
        self.__rules: dict[int, tuple[int, ...]] | None = None
        self.__acceptable_resolutions: Type[ZedCamera.UsbCameraResolution] | Type[ZedCamera] | None = None
        self.__mutex = QtCore.QMutex()
        self.__grab_mutex = QtCore.QMutex()

    def __get_settings(self) -> Settings:
        return Settings(
            fps=self.__init.camera_fps,
            resolution=self.__ZED_RESOLUTION_TO_COMMON_RESOLUTION[self.__init.camera_resolution],
        )

    def open(self) -> OpenStatus:
        if self.__camera.is_opened():
            return OpenStatus.OPENED
        status = self.__camera.open(self.__init)
        if status != sl.ERROR_CODE.SUCCESS:
            return OpenStatus.ERROR
        info: sl.CameraInformation = self.__camera.get_camera_information()
        self.__model = info.camera_model
        self.__rules = self.__get_rules()
        self.acceptable_resolutions = self.__get_acceptable_rules()

        return OpenStatus.SUCCESS

    def close(self) -> CloseStatus:
        if not self.__camera.is_opened():
            return CloseStatus.CLOSED
        status: sl.RecordingStatus = self.__camera.get_recording_status()
        if status.is_paused or status.is_recording:
            return CloseStatus.RECORDING
        self.__camera.close()
        return CloseStatus.SUCCESS

    def __get_rules(self) -> dict[int, tuple[int, ...]]:
        if self.__model in self.__USB_MODELS:
            return self.__USB_RULES
        return self.__GMSL_RULES

    def __get_acceptable_rules(self) -> Type[UsbCameraResolution] | Type[GmslCameraResolution]:
        if self.__model in self.__USB_MODELS:
            return ZedCamera.UsbCameraResolution
        return ZedCamera.GmslCameraResolution

    def change_settings(self, settings: SetSettings) -> Settings | None:
        if self.__model is None or settings.empty:
            return None

        resolution: sl.RESOLUTION = (
            self.__COMMON_RESOLUTION_TO_ZED_RESOLUTION[settings.resolution]
            if settings.resolution
            else self.__init.camera_resolution
        )
        try:
            self.acceptable_resolutions(resolution.value)
        except ValueError:
            raise ValueError('Resolution is not available')

        fps: int = settings.fps or self.__init.camera_fps
        rule = self.__rules.get(resolution.value)
        if fps not in rule:
            fps = min(abs(rule_fps - fps) for rule_fps in rule)
        self.__init.camera_fps = fps
        self.__init.camera_resolution = resolution
        status = self.reopen()
        if status == OpenStatus.ERROR:
            raise IOError('Reopen Failed')
        self.__settings = self.__get_settings()
        return self.__settings

    def reopen(self) -> OpenStatus:
        if self.__camera.is_opened():
            self.__camera.close()
        return self.open()

    @property
    def is_open(self) -> bool:
        return self.__camera.is_opened()

    @property
    def settings(self) -> Settings:
        return self.__settings

    @property
    def acceptable_resolutions(self) -> list[Resolution] | None:
        if self.__acceptable_resolutions is None:
            return None

        resolutions = [self.__ZED_RESOLUTION_TO_COMMON_RESOLUTION[resoltion.value] for resoltion in
                       self.__acceptable_resolutions]
        return resolutions

    @property
    def acceptable_fps_for_resolution(self) -> tuple[int, ...] | None:
        return self.__rules[self.__init.camera_resolution.value] if self.__rules else None

    @property
    def fps_rules_of_resolutions(self) -> dict[int, tuple[int, ...]]:
        return self.__rules

    def run(self) -> None:
        runtime = sl.RuntimeParameters()
        while self._do_work:
            self.__mutex.lock()
            if not self.__camera.is_opened():
                self.__mutex.unlock()
                time.sleep(0.5)
                continue

            self.__grab_code = self.__camera.grab(runtime)
            self.__mutex.unlock()
            if self.__grab_code != sl.ERROR_CODE.SUCCESS:  # Check that a new image is successfully acquired
                self._exception_signal.emit(Exception('При работе камеры что-то пошло не так\n'
                                                      f'Код: {self.__grab_code.value} Название: "{self.__grab_code.name}"'))
                break
        self._stop_work()

    def retrieve_frame(self) -> np.ndarray | None:
        if not self.__camera.is_opened():
            return None
        self.__mutex.lock()
        if self.__grab_code != sl.ERROR_CODE.SUCCESS:
            self.__mutex.unlock()
            return
        mat = sl.Mat()
        self.__camera.retrieve_image(mat, sl.VIEW.LEFT)
        self.__mutex.unlock()
        return mat.get_data()

    def _stop_work(self):
        if self._state != RecorderStates.NOT_RECORD:
            self.__mutex.lock()
            self.__camera.disable_recording()
            self._state = RecorderStates.NOT_RECORD
            self.__mutex.unlock()
        if self.__camera.is_opened():
            self.__camera.close()

    def _start_record(self, file_name: str) -> str:
        file_name = f'{file_name}.svo'
        path = Path(file_name)
        if not path.parent.exists():
            raise Exception(f'Каталога "{path.parent}" не существует')
        self._file_name = file_name
        self.__mutex.lock()
        rec_param = sl.RecordingParameters(file_name,
                                           sl.SVO_COMPRESSION_MODE.H264)  # Enable recording with the filename specified in argument
        err_code = self.__camera.enable_recording(rec_param)
        self.__mutex.unlock()
        if err_code != sl.ERROR_CODE.SUCCESS:
            raise Exception('При попытке начать запись что-то пошло не так\n'
                            f'Код: {err_code.value} Название: "{err_code.name}"')
        return rec_param.video_filename

    def _pause_record(self):
        self.__mutex.lock()
        self.__camera.pause_recording(True)
        self.__mutex.unlock()

    def _continue_record(self):
        self.__mutex.lock()
        self.__camera.pause_recording(False)
        self.__mutex.unlock()

    def _stop_record(self):
        self.__mutex.lock()
        self.__camera.disable_recording()
        self.__mutex.unlock()
        file_name = self._file_name
        self._file_name = None
        return file_name
