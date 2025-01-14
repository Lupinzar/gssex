from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal
from ..uibase.mainwindow import Ui_MainWindow
from ..static import APPLICATION_NAME, RELEASE
from ..state import FORMAT_NAMES, NAMES_FORMAT
from .app import App, Config
from .rendertab import RenderTab

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_opened_file.setText("(No save state opened)")
        self.setWindowTitle(f"{APPLICATION_NAME} {RELEASE}")
        self.app = App()
        self.app.config.load()
        self.setup_state_combo()
        self.refresh_config()

        #do some setup for our tabs that inherit RenderTab
        rtab: RenderTab
        for rtab in self.main_tabs.findChildren(RenderTab):
            rtab.bind_states(self.app)
            rtab.statusMessage.connect(self.show_timed_status_message)

        self.main_tabs.currentChanged.connect(self.handle_tab_changed)
        #needed for "Find in RAW" feature
        self.tab_vram.link_raw_tab(self.tab_raw)

        #config changes
        self.bg_color_toggle.toggled.connect(self.update_config)
        self.bg_color_button.colorChanged.connect(self.update_config)
        self.state_format_combo.currentTextChanged.connect(self.update_config)
        self.output_select_button.pressed.connect(self.select_output_dir)
        self.default_config_button.pressed.connect(self.restore_config_defaults)

        self.action_open_folder.triggered.connect(self.open_folder)
        self.action_open_file.triggered.connect(self.open_file)
        self.action_previous_file.triggered.connect(self.previous_file)
        self.action_next_file.triggered.connect(self.next_file)
        self.action_lock_palette.triggered.connect(self.update_pal_lock)

        #after everything is loaded/setup, handle any tab updates
        self.handle_tab_changed()
        
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
        self.load_state()

    def open_file(self):
        file = QFileDialog.getOpenFileName(self, "Select save state...", self.app.directory, "Save states (*.gs?)")
        if not file[0]:
            return
        if not self.app.open_file(file[0]):
            self.show_timed_status_message(f"Could not open {file}")
            return
        self.update_file_ui()
        self.load_state()

    def next_file(self):
        if not self.app.adjust_file_index(1):
            self.show_timed_status_message("Already at last save state")
            return
        self.update_file_ui()
        self.load_state()

    def previous_file(self):
        if not self.app.adjust_file_index(-1):
            self.show_timed_status_message("Already at first save state")
            return
        self.update_file_ui()
        self.load_state()

    def load_state(self):
        if not self.app.load_state(self.app.config.state_format):
            self.show_timed_status_message(f"Could not load {self.app.make_path()}")
        if isinstance(self.main_tabs.currentWidget(), RenderTab):
            self.main_tabs.currentWidget().saveStateChanged.emit()

    def update_file_ui(self):
        self.label_opened_file.setText(self.app.make_path())

    def refresh_config(self):
        self.bg_color_toggle.setChecked(self.app.config.override_background)
        self.state_format_combo.setCurrentText(FORMAT_NAMES[self.app.config.state_format])
        self.output_directory_line.setPlaceholderText(self.app.config.output_path)
        self.bg_color_button.setColor(QColor(self.app.config.override_color))

    def update_config(self):
        self.app.config.override_background = self.bg_color_toggle.isChecked()
        self.app.config.override_color = self.bg_color_button.color().rgb()
        self.app.config.output_path = self.output_directory_line.placeholderText()
        self.app.config.state_format = NAMES_FORMAT[self.state_format_combo.currentText()]
        self.save_config()

    def save_config(self):
        if self.app.config.save():
            self.show_timed_status_message('Configuration saved')
        else:
            self.show_timed_status_message(f'Warning: Could not save configuration to {Config.CONFIG_PATH}')
    
    def select_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select images output directory...", self.app.config.output_path)
        if not directory:
            return
        self.app.config.output_path = directory
        self.refresh_config()
        self.update_config()

    def update_pal_lock(self):
        self.app.use_global_pal = self.action_lock_palette.isChecked()
        if isinstance(self.main_tabs.currentWidget(), RenderTab):
            self.main_tabs.currentWidget().paletteSwapped.emit()


    def restore_config_defaults(self):
        answer = QMessageBox.question(
            self, 
            "Confirmation", 
            "Are you sure you want to restore defaults?\nYour current configuration will be lost.", 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return
        self.app.config = Config()
        self.refresh_config()
        self.save_config()

    def handle_tab_changed(self):
        if isinstance(self.main_tabs.currentWidget(), RenderTab):
            self.main_tabs.currentWidget().fullRefresh.emit()
