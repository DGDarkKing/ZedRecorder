from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import QMainWindow

from infrastracture.recorders.recorder import RecorderStates
from infrastracture.recorders.schemas.settings import SetSettings
from infrastracture.recorders.zed_camera import ZedCamera
from interface_window.main.design import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, camera: ZedCamera, save_path: Path, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.__camera = camera
        self.__save_path = save_path

        self.__set_enable_all(False)
        self.ui.BTN_PauseRecord.setVisible(False)
        self.ui.BTN_PauseRecord.setEnabled(False)
        self.ui.Btn_OpenCamera.setEnabled(True)
        self.__update_combobox_resolution()
        self.__update_combobox_fps()

        self.ui.Label_VideoName.setText('')

        self.ui.Btn_OpenCamera.clicked.connect(self.__open_camera)
        self.ui.Btn_CloseCamera.clicked.connect(self.__close_camera)

        self.ui.comboBox_Resolution.currentIndexChanged.connect(self.__select_resolution)
        self.ui.comboBox_FPS.currentIndexChanged.connect(self.__select_fps)

        self.ui.BTN_StartRecord.clicked.connect(self.__start_record)
        self.ui.BTN_FinishRecord.clicked.connect(self.__finish_record)

    def __set_enable_all(self, flag: bool):
        self.ui.Btn_OpenCamera.setEnabled(flag)
        self.ui.Btn_CloseCamera.setEnabled(flag)

        self.ui.comboBox_Resolution.setEnabled(flag)
        self.ui.comboBox_FPS.setEnabled(flag)

        self.ui.BTN_StartRecord.setEnabled(flag)
        self.ui.BTN_FinishRecord.setEnabled(flag)

    def __update_combobox_resolution(self):
        resolutions = self.__camera.acceptable_resolutions
        self.ui.comboBox_Resolution.clear()
        if resolutions is None:
            resolution = self.__camera.settings.resolution
            self.ui.comboBox_Resolution.addItem(resolution.name, resolution)
            return
        for resolution in resolutions:
            self.ui.comboBox_Resolution.addItem(resolution.name, resolution)

    def __select_combobox_resolution(self):
        resolution = self.__camera.settings.resolution
        index = self.ui.comboBox_Resolution.findText(resolution.name)
        if index == -1:
            return
        self.ui.comboBox_Resolution.setCurrentIndex(index)

    def __update_combobox_fps(self):
        fps_list = self.__camera.acceptable_fps_for_resolution
        self.ui.comboBox_FPS.clear()
        if fps_list is None:
            fps = self.__camera.settings.fps
            self.ui.comboBox_FPS.addItem(str(fps), fps)
            return
        for fps in fps_list:
            self.ui.comboBox_FPS.addItem(str(fps), fps)

    def __select_combobox_fps(self):
        fps = self.__camera.settings.fps
        index = self.ui.comboBox_FPS.findText(str(fps))
        if index == -1:
            return
        self.ui.comboBox_Resolution.setCurrentIndex(index)

    def __open_camera(self, s):
        self.__set_enable_all(False)
        status = self.__camera.open()
        if status == status.ERROR:
            self.ui.Btn_OpenCamera.setEnabled(True)
        else:
            self.__update_combobox_resolution()
            self.__select_combobox_resolution()
            self.__update_combobox_fps()
            self.__select_combobox_fps()
            self.__set_enable_all(True)
            self.ui.Btn_OpenCamera.setEnabled(False)

    def __close_camera(self, s):
        self.__set_enable_all(False)
        status = self.__camera.close()
        match status:
            case status.CLOSED | status.SUCCESS:
                self.ui.Btn_OpenCamera.setEnabled(True)
            case status.RECORDING:
                self.__update_record_panel()

    def __update_record_panel(self):
        state = self.__camera.state
        if state == state.NOT_RECORD:
            self.ui.BTN_FinishRecord.setEnabled(False)
            self.ui.BTN_StartRecord.setEnabled(True)
        else:
            self.ui.BTN_FinishRecord.setEnabled(True)
            self.ui.BTN_StartRecord.setEnabled(False)

    def __select_resolution(self, index):
        if not self.ui.comboBox_Resolution.isEnabled():
            return
        elif self.__camera.state == RecorderStates.RECORD:
            return
        resolution = self.ui.comboBox_Resolution.itemData(index)
        self.__camera.change_settings(SetSettings(resolution=resolution))

    def __select_fps(self, index):
        if not self.ui.comboBox_FPS.isEnabled():
            return
        elif self.__camera.state == RecorderStates.RECORD:
            return
        fps = self.ui.comboBox_FPS.itemData(index)
        self.__camera.change_settings(SetSettings(fps=fps))

    def __start_record(self, s):
        self.__set_enable_all(False)
        if not self.__camera.is_open:
            return
        if self.__camera.state != RecorderStates.NOT_RECORD:
            return
        filename = self.__save_path / datetime.now().isoformat()
        filename = self.__camera.record(str(filename))
        if filename:
            self.ui.Label_VideoName.setText(filename)
        self.ui.BTN_FinishRecord.setEnabled(True)

    def __finish_record(self, s):
        self.__set_enable_all(False)
        if self.__camera.state == RecorderStates.NOT_RECORD:
            return
        self.__camera.stop()
        self.ui.BTN_StartRecord.setEnabled(True)
        self.ui.comboBox_Resolution.setEnabled(True)
        self.ui.comboBox_FPS.setEnabled(True)
        self.ui.Btn_CloseCamera.setEnabled(True)
        self.ui.Label_VideoName.setText('')


