import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QListWidgetItem, QLineEdit,
    QPushButton, QSystemTrayIcon, QMenu, QAction, QLabel
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon

class ClipboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CopyTable")
        self.setMinimumSize(420, 500)
        self.history = []
        self.last_clip = ""

        # Load icon once, use everywhere
        import os
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "copytable.svg")
        self.app_icon = QIcon(icon_path)

        # Taskbar + Alt-Tab + window decorations
        self.setWindowIcon(self.app_icon)

        # Set on the QApplication itself (covers Alt-Tab & taskbar)
        QApplication.instance().setWindowIcon(self.app_icon)

        self._build_ui()
        self._build_tray()

        # Poll clipboard every 500ms
        self.timer = QTimer()
        self.timer.timeout.connect(self._check_clipboard)
        self.timer.start(500)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        # Title
        title = QLabel("📋 CopyTable — Clipboard History")
        title.setStyleSheet("font-size: 15px; font-weight: bold; padding-bottom: 4px;")
        layout.addWidget(title)

        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search clipboard history...")
        self.search_box.textChanged.connect(self._filter_list)
        self.search_box.setStyleSheet("padding: 6px; font-size: 13px;")
        layout.addWidget(self.search_box)

        # Clipboard list
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget::item { padding: 8px; border-bottom: 1px solid #ddd; }
            QListWidget::item:selected { background-color: #0078d7; color: white; }
        """)
        self.list_widget.itemDoubleClicked.connect(self._copy_item)
        layout.addWidget(self.list_widget)

        # Buttons row
        btn_layout = QHBoxLayout()

        self.copy_btn = QPushButton("⬆ Copy Selected")
        self.copy_btn.clicked.connect(self._copy_item)
        self.copy_btn.setStyleSheet("padding: 7px; font-size: 13px;")

        self.delete_btn = QPushButton("🗑 Delete Selected")
        self.delete_btn.clicked.connect(self._delete_item)
        self.delete_btn.setStyleSheet("padding: 7px; font-size: 13px;")

        self.clear_btn = QPushButton("✖ Clear All")
        self.clear_btn.clicked.connect(self._clear_all)
        self.clear_btn.setStyleSheet("padding: 7px; font-size: 13px; color: red;")

        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)

    def _build_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.app_icon)  # uses shared icon
        self.tray.setToolTip("CopyTable")

        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self._tray_clicked)
        self.tray.show()

    def _tray_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show() if self.isHidden() else self.hide()

    def _check_clipboard(self):
        clip = QApplication.clipboard().text()
        if clip and clip != self.last_clip:
            self.last_clip = clip
            if clip not in self.history:
                self.history.insert(0, clip)
                self._refresh_list()

    def _refresh_list(self):
        query = self.search_box.text().lower()
        self.list_widget.clear()
        for entry in self.history:
            if query in entry.lower():
                display = entry[:80] + "..." if len(entry) > 80 else entry
                item = QListWidgetItem(display)
                item.setData(Qt.UserRole, entry)  # store full text
                self.list_widget.addItem(item)

    def _filter_list(self):
        self._refresh_list()

    def _copy_item(self):
        item = self.list_widget.currentItem()
        if item:
            QApplication.clipboard().setText(item.data(Qt.UserRole))

    def _delete_item(self):
        item = self.list_widget.currentItem()
        if item:
            full_text = item.data(Qt.UserRole)
            self.history = [e for e in self.history if e != full_text]
            self._refresh_list()

    def _clear_all(self):
        self.history.clear()
        self.list_widget.clear()

    def closeEvent(self, event):
        # Minimize to tray instead of closing
        event.ignore()
        self.hide()
        self.tray.showMessage("CopyTable", "Still running in the system tray.", QSystemTrayIcon.Information, 2000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # keep alive in tray
    window = ClipboardApp()
    window.show()
    sys.exit(app.exec_())
