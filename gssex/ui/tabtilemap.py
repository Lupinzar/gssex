from .rendertab import RenderTab
from .app import pil_to_qimage, pil_to_clipboard
from ..uibase.tabtilemap import Ui_TabTileMap
from ..static import Plane, Priority
from ..render import MapRender
from PySide6.QtWidgets import QButtonGroup, QLabel
from PySide6.QtGui import QPixmap, QShortcut, QKeySequence
from PIL import Image
from os.path import basename

class TabTileMap(RenderTab, Ui_TabTileMap):
    SCROLL_MARK_THICKNESS = 16
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setupUi(self)
        self.setup_plane_combo()
        self.mode_group = QButtonGroup()
        self.priority_group = QButtonGroup()
        self.renderer: MapRender|None = None
        self.info_labels: list[QLabel] = [
            self.info_hscroll_label,
            self.info_vscroll_label,
            self.info_scroll_size_label,
            self.info_window_size_label
        ]

        self.clear_valids()
        
        self.mode_group.addButton(self.mode_map_radio)
        self.mode_group.addButton(self.mode_screen_button)
        self.mode_group.addButton(self.mode_marks_button)
        self.mode_map_radio.setChecked(True)

        self.priority_group.addButton(self.priority_both_radio)
        self.priority_group.addButton(self.priority_high_radio)
        self.priority_group.addButton(self.priority_low_radio)
        self.priority_both_radio.setChecked(True)

        self.fullRefresh.connect(self.do_full_refresh)
        self.saveStateChanged.connect(self.do_full_refresh)
        self.paletteSwapped.connect(self.draw_main)

        self.plane_combo.currentIndexChanged.connect(self.draw_main)
        self.mode_group.buttonClicked.connect(self.draw_main)
        self.priority_group.buttonClicked.connect(self.draw_main)
        self.save_button.clicked.connect(self.save_image)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        self.register_shortcuts()
    
    def setup_plane_combo(self):
        for k in range(0, len(Plane)):
            enum = Plane(k)
            self.plane_combo.addItem(enum.name.replace("_", " ").title())

    def register_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+S"), self, lambda: self.save_image())
        QShortcut(QKeySequence("Ctrl+C"), self, lambda: self.copy_to_clipboard())

    def update_info(self):
        vdp = self.app.savestate.vdp_registers
        win_size = vdp.get_window_cell_size()
        self.info_hscroll_label.setText(vdp.scroll_mode_h.name.title())
        self.info_vscroll_label.setText(vdp.scroll_mode_v.name.title())
        self.info_scroll_size_label.setText(f'{vdp.scroll_width * 8} x {vdp.scroll_height * vdp.tile_height}')
        self.info_window_size_label.setText(f'{win_size[0] * 8} x {win_size[1] * vdp.tile_height}')
        
    def clear_valids(self):
        self.main_label.clear()
        for lbl in self.info_labels:
            lbl.setText('-')

    def do_full_refresh(self):
        if not self.app.valid_file:
            self.renderer = None
            self.clear_valids()
            return
        self.renderer = MapRender(self.app.savestate)
        self.update_info()
        self.draw_main()

    def draw_main(self):
        if not self.app.valid_file:
            return
        pilimg = self.get_pil_image()
        qimg = pil_to_qimage(pilimg)
        self.main_label.setFixedSize(pilimg.width, pilimg.height)
        self.scrollAreaWidgetContents.setFixedSize(pilimg.width, pilimg.height)
        self.main_label.setPixmap(QPixmap.fromImage(qimg))
        
        pilimg.close()

    def get_pil_image(self) -> Image.Image:
        match(self.mode_group.checkedButton()):
            case self.mode_screen_button:
                return self.get_pil_screen()
            case self.mode_marks_button:
                return self.get_pil_marks()
            case _:
                return self.get_pil_map()
            
    def get_pil_screen(self) -> Image.Image:
        pal_data = self.app.get_palette_and_background()
        img = self.renderer.render_screen(
            Plane(self.plane_combo.currentIndex()),
            self.priority_ui_to_enum(),
            pal_data[0]
        )
        img.putpalette(pal_data[1].flattened_colors())
        return img
    
    def get_pil_marks(self) -> Image.Image:
        plane = Plane(self.plane_combo.currentIndex())
        img = self.renderer.render_scoll_marks(plane, self.SCROLL_MARK_THICKNESS)
        screen = self.get_pil_screen()

        img.paste(screen, (self.SCROLL_MARK_THICKNESS, self.SCROLL_MARK_THICKNESS))
        screen.close()
        return img
    
    def get_pil_map(self) -> Image.Image:
        pal_data = self.app.get_palette_and_background()
        img = self.renderer.render_map(
            Plane(self.plane_combo.currentIndex()),
            self.priority_ui_to_enum(),
            pal_data[0]
        )
        img.putpalette(pal_data[1].flattened_colors())
        return img
    
    def save_image(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        img = self.get_pil_image()
        path = self.build_image_path()
        if self.app.save_image(img, path):
            self.statusMessage.emit(f"Output {path}")
        else:
            self.statusMessage.emit(f"Error outputting {path}")
        img.close()

    def copy_to_clipboard(self):
        if not self.app.valid_file:
            self.statusMessage.emit(self.STATE_NOT_VALID_MSG)
            return
        img = self.get_pil_image()
        pil_to_clipboard(img)
        img.close()

    def build_image_path(self) -> str:
        parts = [
            self.plane_combo.currentText().lower().replace(" ", "-"),
            self.mode_to_save_string(),
            self.priority_ui_to_enum().name.lower(),
            'global' if self.app.use_global_pal else 'state'
        ]
        key = "_".join(parts)
        return self.app.build_image_output_path(key)

    def priority_ui_to_enum(self) -> Priority:
        match(self.priority_group.checkedButton()):
            case self.priority_both_radio:
                return Priority.BOTH
            case self.priority_high_radio:
                return Priority.HIGH
        return Priority.LOW
    
    def mode_to_save_string(self) -> str:
        match self.mode_group.checkedButton():
            case self.mode_screen_button:
                return 'screen'
            case self.mode_marks_button:
                return 'screen-marks'
        return 'tilemap'
