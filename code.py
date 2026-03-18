import sys
import os

# Enable GPU acceleration with Vulkan and Skia
os.environ["QT_QUICK_BACKEND"] = "vulkan"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--enable-features=Vulkan,VulkanFromANGLE,SkiaGraphite "
    "--use-vulkan --enable-gpu-rasterization --ignore-gpu-blocklist "
    "--disable-software-rasterizer"
)
if sys.platform.startswith("linux"):
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, 
    QLineEdit, QPushButton, QComboBox, QLabel
)
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile

# SHAPESHIFER: User Agent Switcher
class Shapeshifer:
    def __init__(self, ua_map):
        self.ua_map = ua_map

    def apply(self, browser, ua_string):
        # Create a new profile just for this tab and set UA
        profile = QWebEngineProfile()
        profile.setHttpUserAgent(ua_string)
        page = browser.page()
        page.setWebEngineProfile(profile)
        browser.setPage(page)

class BotHunterUltimate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Hunter - Ultimate Workstation")
        self.resize(1366, 768)
        self.profile = QWebEngineProfile.defaultProfile()

        self.ua_map = {
            "Linux (Default)": self.profile.httpUserAgent(),
            "Windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "iPhone": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1"
        }

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(QLabel("URL: "))
        navtb.addWidget(self.urlbar)

        # User Agent Switcher dropdown
        self.ua_switcher = QComboBox()
        self.ua_switcher.addItems(self.ua_map.keys())
        navtb.addWidget(QLabel("User Agent: "))
        navtb.addWidget(self.ua_switcher)

        navtb.addWidget(QPushButton("New Tab", clicked=self.add_new_tab))

        self.shapeshifer = Shapeshifer(self.ua_map)
        self.add_new_tab()

    def add_new_tab(self, url="https://duckduckgo.com"):
        browser = QWebEngineView()
        ua_label = self.ua_switcher.currentText()
        ua_string = self.ua_map[ua_label]
        self.shapeshifer.apply(browser, ua_string)

        i = self.tabs.addTab(browser, f"{ua_label} Tab")
        self.tabs.setCurrentIndex(i)
        browser.setUrl(QUrl(url))
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
            # Switch user agent for this tab if changed
            ua_label = self.ua_switcher.currentText()
            ua_string = self.ua_map[ua_label]
            self.shapeshifer.apply(current_browser, ua_string)
            current_browser.setUrl(QUrl(url))

    def update_urlbar(self, q, browser=None):
        if browser == self.tabs.currentWidget():
            self.urlbar.setText(q.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotHunterUltimate()
    window.show()
    sys.exit(app.exec())
