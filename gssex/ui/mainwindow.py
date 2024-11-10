from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtCore import QCoreApplication
from ..uibase.mainwindow import Ui_MainWindow
from ..static import APPLICATION_NAME, RELEASE
from .app import App, Config

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_opened_file.setText("(No save state opened)")
        self.setWindowTitle(f"{APPLICATION_NAME} {RELEASE}")
        self.app = App()
        self.config = Config()

        self.action_open_folder.triggered.connect(self.open_folder)
        self.action_open_file.triggered.connect(self.open_file)
        self.action_previous_file.triggered.connect(self.previous_file)
        self.action_next_file.triggered.connect(self.next_file)

    def show_timed_status_message(self, message: str):
        self.statusbar.showMessage(message, App.DEFAULT_STATUS_TIMEOUT)

    def open_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select save state directory...", self.app.directory)
        if not directory:
            return
        if not self.app.open_directory(directory):
            self.show_timed_status_message(f"Could not open {directory}")
            return
        if not self.app.select_first_file():
            self.label_opened_file.setText(f"{self.app.directory} (no save states)")
            return
        self.update_file_ui()
        #TODO: handle savestate opening and refresh

    def open_file(self):
        file = QFileDialog.getOpenFileName(self, "Select save state...", self.app.directory, "Save states (*.gs?)")
        if not file[0]:
            return
        if not self.app.open_file(file[0]):
            self.show_timed_status_message(f"Could not open {file}")
            return
        self.update_file_ui()
        #TODO: handle savestate opening and refresh

    def next_file(self):
        if not self.app.adjust_file_index(1):
            self.show_timed_status_message("Already at last save state")
            return
        self.update_file_ui()
        #TODO: handle savestate opening and refresh

    def previous_file(self):
        if not self.app.adjust_file_index(-1):
            self.show_timed_status_message("Already at first save state")
            return
        self.update_file_ui()

    def update_file_ui(self):
        self.label_opened_file.setText(f"{self.app.directory}/{self.app.current_file}")

            