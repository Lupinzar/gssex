from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtGui import QColor
from ..uibase.mainwindow import Ui_MainWindow
from ..static import APPLICATION_NAME, RELEASE
from ..state import FORMAT_NAMES, NAMES_FORMAT
from .app import App, Config

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_opened_file.setText("(No save state opened)")
        self.setWindowTitle(f"{APPLICATION_NAME} {RELEASE}")
        self.app = App()
        self.config = Config()
        self.setup_state_combo()
        self.refresh_config()

        self.action_open_folder.triggered.connect(self.open_folder)
        self.action_open_file.triggered.connect(self.open_file)
        self.action_previous_file.triggered.connect(self.previous_file)
        self.action_next_file.triggered.connect(self.next_file)
        
    #dynamically load the combo box based on the supported formats in state module
    def setup_state_combo(self):
        for name in NAMES_FORMAT.keys():
            self.state_format_combo.addItem(name)

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

    def refresh_config(self):
        self.bg_color_toggle.setChecked(self.config.override_background)
        self.state_format_combo.setCurrentText(FORMAT_NAMES[self.config.state_format])
        self.output_directory_line.setPlaceholderText(self.config.output_path)
        self.bg_color_button.setColor(QColor(self.config.override_color))

            