import os
import sys

# Forces the Qt UI layer to use Vulkan
os.environ["QT_QUICK_BACKEND"] = "vulkan"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--enable-features=Vulkan,VulkanFromANGLE,SkiaGraphite "
    "--use-vulkan --enable-gpu-rasterization --ignore-gpu-blocklist"
)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, 
    QLineEdit, QPushButton, QMessageBox, QComboBox, QCheckBox
)
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage

CHROMIUM_STYLE = """
QMainWindow { background-color: #202124; }
QToolBar { background: #292a2d; border-bottom: 1px solid #3c4043; padding: 6px; spacing: 8px; }
QCheckBox { color: #8ab4f8; font-size: 11px; font-weight: bold; }
/* ... (rest of your existing CSS) ... */
"""

class BotHunterBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Hunter - Secure Workstation")
        self.resize(1280, 850)

        # 1. Profile Setup
        self.profile = QWebEngineProfile.defaultProfile()
        self.default_ua = self.profile.httpUserAgent()

        # 2. UI Setup
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        # --- NEW: PERFORMANCE SAVER CONTROLS ---
        self.navbar.addSeparator()
        
        self.cpu_saver = QCheckBox("CPU SAVER")
        self.cpu_saver.setToolTip("Freezes background tabs to stop CPU usage")
        self.navbar.addWidget(self.cpu_saver)

        self.mem_saver = QCheckBox("MEM SAVER")
        self.mem_saver.setToolTip("Discards background tabs from RAM (will reload on click)")
        self.navbar.addWidget(self.mem_saver)

        # Tab Container
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # Connect the "Tab Switched" signal to our saver logic
        self.tabs.currentChanged.connect(self.manage_tab_lifecycle)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.add_new_tab(QUrl("https://www.google.com"), "Home")

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None: qurl = QUrl("https://www.google.com")
        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        # Set initial state to Active
        browser.page().setLifecycleState(QWebEnginePage.LifecycleState.Active)
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

    def manage_tab_lifecycle(self, index):
        """ This is the core 'Chrome-style' logic """
        if index < 0: return

        for i in range(self.tabs.count()):
            browser = self.tabs.widget(i)
            if i == index:
                # Always wake up the tab you just clicked on
                browser.page().setLifecycleState(QWebEnginePage.LifecycleState.Active)
            else:
                # Handle background tabs based on checkboxes
                if self.mem_saver.isChecked():
                    # Memory Saver: Kills the process (Unloads from RAM)
                    browser.page().setLifecycleState(QWebEnginePage.LifecycleState.Discarded)
                elif self.cpu_saver.isChecked():
                    # CPU Saver: Pauses JS/Timers (Keeps in RAM)
                    browser.page().setLifecycleState(QWebEnginePage.LifecycleState.Frozen)

    def navigate_to_url(self):
        u = self.url_bar.text()
        if not "://" in u: u = "https://" + u
        self.tabs.currentWidget().setUrl(QUrl(u))

    def close_tab(self, i):
        if self.tabs.count() > 1: self.tabs.removeTab(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(CHROMIUM_STYLE)
    window = BotHunterBrowser()
    window.show()
    sys.exit(app.exec())
