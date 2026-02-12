from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, Signal, QFileSystemWatcher
from gssex.uibase.mainwindow import Ui_MainWindow
from gssex.static import APPLICATION_NAME, AUTHOR_STRING, GIT_HUB_URL, SAVESTATE_DIALOG_TYPES
from gssex.release import RELEASE
from gssex.state import FORMAT_NAMES, NAMES_FORMAT
from gssex.ui.app import App, Config
from gssex.ui.rendertab import RenderTab
from gssex.ui.keydefine import KeyDefine
from os.path import isfile, basename, join
from shutil import copyfile

class MainWindow(QMainWindow, Ui_MainWindow):
    shortcut_change: Signal = Signal()

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.label_opened_file.setText("(No save state opened)")
        self.setWindowTitle(f"{APPLICATION_NAME} {RELEASE}")
        self.app = App()
        self.app.config.load()
        self.app.shortcuts.load()
        self.setup_state_combo()
        self.refresh_config()
        self.watcher_path: str
        self.watcher: QFileSystemWatcher
        self.watcher_counter: int = 0

        #do some setup for our tabs that inherit RenderTab
        rtab: RenderTab
        for rtab in self.main_tabs.findChildren(RenderTab):
            rtab.bind_states(self.app)
            rtab.statusMessage.connect(self.show_timed_status_message)

        self.main_tabs.currentChanged.connect(self.handle_tab_changed)
        #needed for "Find in RAW" feature
        self.tab_vram.link_raw_tab(self.tab_raw)
        self.tab_hw_sprites.link_raw_tab(self.tab_raw)

        #about tab
        self.about_label.setText(
            f'{APPLICATION_NAME} {RELEASE}\n\nBy: {AUTHOR_STRING}\nGitHub: {GIT_HUB_URL}'
        )
        self.about_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        #config changes
        self.bg_color_toggle.toggled.connect(self.update_config)
        self.bg_color_button.colorChanged.connect(self.update_config)
        self.state_format_combo.currentTextChanged.connect(self.update_config)
        self.output_select_button.pressed.connect(self.select_output_dir)
        self.default_config_button.pressed.connect(self.restore_config_defaults)
        self.config_shortcuts_button.pressed.connect(self.open_shortcuts)
        self.shortcut_change.connect(self.update_shortcuts)

        self.action_open_folder.triggered.connect(self.open_folder)
        self.action_open_file.triggered.connect(self.open_file)
        self.action_previous_file.triggered.connect(self.previous_file)
        self.action_next_file.triggered.connect(self.next_file)
        self.action_refresh.triggered.connect(self.refresh_file)
        self.action_lock_palette.triggered.connect(self.update_pal_lock)

        self.watch_file_button.pressed.connect(self.open_watcher_file)
        self.watch_start_button.pressed.connect(self.start_watching)
        self.watch_stop_button.pressed.connect(self.stop_watching)

        #after everything is loaded/setup, handle any tab updates
        self.handle_tab_changed()
        
        #keyboard shortcuts
        self.register_shortcuts()
        
    #dynamically load the combo box based on the supported formats in state module
    def setup_state_combo(self):
        for name in NAMES_FORMAT.keys():
            self.state_format_combo.addItem(name)

    def show_timed_status_message(self, message: str):
        self.statusbar.showMessage(message, App.DEFAULT_STATUS_TIMEOUT)

    def open_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select save state directory...", self.app.directory) #type: ignore
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
        file = QFileDialog.getOpenFileName(self, "Select save state...", self.app.directory, SAVESTATE_DIALOG_TYPES) #type: ignore
        if not file[0]:
            return
        self.core_open_file(file[0])

    def core_open_file(self, path: str):
        if not self.app.open_file(path):
            self.show_timed_status_message(f"Could not open {path}")
            return
        self.update_file_ui()
        self.load_state()

    def refresh_file(self):
        if not self.app.current_file:
            return
        path = self.app.make_path()
        if not self.app.open_file(path):
            self.show_timed_status_message(f"Could not reload {path}")
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
        self.emit_state_changed()

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
        self.refresh_file()

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
            self.main_tabs.currentWidget().paletteSwapped.emit()    #type: ignore

    def restore_config_defaults(self):
        answer = QMessageBox.question(
            self, 
            "Confirmation", 
            "Are you sure you want to restore defaults?\nYour current configuration will be lost.", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )

        if answer != QMessageBox.StandardButton.Yes:
            return
        self.app.config = Config()
        self.refresh_config()
        self.save_config()

    def open_shortcuts(self):
        sc = KeyDefine(self, self.app.shortcuts)
        sc.setWindowModality(Qt.WindowModality.WindowModal)
        sc.show()

    def register_shortcuts(self):
        self.action_lock_palette.setShortcut(self.app.shortcuts.get_sequence('shortcut_palette_swap'))
        for tab in self.main_tabs.findChildren(RenderTab):
            tab.register_shortcuts()

    def update_shortcuts(self):
        self.action_lock_palette.setShortcut(self.app.shortcuts.get_sequence('shortcut_palette_swap'))
        for tab in self.main_tabs.findChildren(RenderTab):
            tab.update_shortcuts()

    def open_watcher_file(self):
        file = QFileDialog.getOpenFileName(self, "Select save state...", self.app.directory, SAVESTATE_DIALOG_TYPES) #type: ignore
        if not file[0]:
            return
        self.watcher_path = file[0]
        self.watch_file_path_box.setPlaceholderText(self.watcher_path)

    def start_watching(self):
        if not hasattr(self, 'watcher_path'):
            QMessageBox.critical(None, 'Error', 'Please select a save state to watch')
            return
        if not isfile(self.watcher_path):
            QMessageBox.critical(None, 'Error', 'Selected save state is not a file or does not exist')
            return
        if not self.watch_load_toggle.isChecked() and not self.watch_save_toggle.isChecked():
            QMessageBox.critical(None, 'Error', 'Please select at least one of the check box options')
            return
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.watcher_path)
        self.watcher.fileChanged.connect(self.watcher_change)
        self.watch_start_button.setEnabled(False)
        self.watch_stop_button.setEnabled(True)

    def stop_watching(self):
        self.watcher.removePath(self.watcher_path)
        del self.watcher
        self.watch_start_button.setEnabled(True)
        self.watch_stop_button.setEnabled(False)
    
    def watcher_change(self):
        if self.watch_load_toggle.isChecked():
            self.core_open_file(self.watcher_path)
        if self.watch_save_toggle.isChecked():
            self.watcher_save_copy()

    def watcher_save_copy(self):
        path = join(self.app.config.output_path, self.build_watcher_name())
        while isfile(path):
            self.watcher_counter += 1
            path = join(self.app.config.output_path, self.build_watcher_name())
        try:
            copyfile(self.watcher_path, path)
        except:
            self.show_timed_status_message(f'Could not save state copy to: {path}')
            return
        self.show_timed_status_message(f'Saved save state copy to: {path}')

    def build_watcher_name(self) -> str:
        parts = basename(self.watcher_path).split('.')
        parts[0] = f'{parts[0]}_{self.watcher_counter:05}'
        return '.'.join(parts)

    def handle_tab_changed(self):
        if isinstance(self.main_tabs.currentWidget(), RenderTab):
            self.main_tabs.currentWidget().fullRefresh.emit()   #type: ignore

    def emit_state_changed(self):
        if isinstance(self.main_tabs.currentWidget(), RenderTab):
            self.main_tabs.currentWidget().saveStateChanged.emit()  #type: ignore
