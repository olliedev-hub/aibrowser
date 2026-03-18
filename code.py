import sys
import os

# 1. THE GPU POWERHOUSE (VULKAN & SKIA)
# Setting these before QApplication starts to prevent crashes
os.environ["QT_QUICK_BACKEND"] = "vulkan"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--enable-features=Vulkan,VulkanFromANGLE,SkiaGraphite "
    "--use-vulkan --enable-gpu-rasterization --ignore-gpu-blocklist "
    "--disable-software-rasterizer"
)

# Linux Sandbox Fix for Chromebooks
if sys.platform.startswith("linux"):
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, 
    QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel
)
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile

class BotHunterUltimate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Hunter - Ultimate Workstation")
        self.resize(1366, 768)

        # CORE PROFILE SETUP
        self.profile = QWebEngineProfile.defaultProfile()
        
        # USER AGENT DATABASE (Every OS)
        self.ua_map = {
            "Linux (Default)": self.profile.httpUserAgent(),
            "Windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Basic toolbar for navigation
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(QLabel("URL: "))
        navtb.addWidget(self.urlbar)
        navtb.addWidget(QPushButton("New Tab", clicked=self.add_new_tab))

        self.add_new_tab()

    def add_new_tab(self, url="https://duckduckgo.com"):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda q, browser=browser: self.update_urlbar(q, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def navigate_to_url(self):
        url = self.urlbar.text()
        if not url.startswith("http"):
            url = "http://" + url
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.setUrl(QUrl(url))

    def update_urlbar(self, q, browser=None):
        if browser == self.tabs.currentWidget():
            self.urlbar.setText(q.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotHunterUltimate()
    window.show()
    sys.exit(app.exec())
