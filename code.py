import sys
import os

# STABILITY FIX: Disable the sandbox if on Linux to prevent Segfaults
if sys.platform.startswith("linux"):
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, 
    QLineEdit, QPushButton, QCheckBox, QVBoxLayout, QWidget
)
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage

class BotHunterBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Hunter - High Performance")
        self.resize(1280, 850)

        # --- TAB WIDGET SETUP ---
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True) # Drag and drop tabs
        self.setCentralWidget(self.tabs)

        # Signals
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.manage_tab_lifecycle)

        # --- TOOLBAR ---
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        self.navbar.addSeparator()

        # Performance Toggles
        self.cpu_saver = QCheckBox("CPU SAVER")
        self.mem_saver = QCheckBox("MEM SAVER")
        self.navbar.addWidget(self.cpu_saver)
        self.navbar.addWidget(self.mem_saver)

        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        self.navbar.addWidget(self.new_tab_btn)

        # Initial Tab
        self.add_new_tab(QUrl("https://www.google.com"), "Home")

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        # Create the browser view
        browser = QWebEngineView()
        
        # Add to tabs first (Stability Fix)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Load URL
        browser.setUrl(qurl)

        # Update URL bar and Tab Title when page changes
        browser.urlChanged.connect(lambda q, b=browser: self.renew_url_bar(q, b))
        browser.loadFinished.connect(lambda _, b=browser: self.tabs.setTabText(
            self.tabs.indexOf(b), b.page().title()[:20] # Truncate long titles
        ))

    def renew_url_bar(self, q, browser):
        # Only update the URL bar if the tab is currently visible
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(q.toString())

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            # Proper memory cleanup for the browser instance
            target_widget = self.tabs.widget(i)
            self.tabs.removeTab(i)
            target_widget.deleteLater() 
        else:
            self.close() # Close app if last tab is closed

    def manage_tab_lifecycle(self, index):
        """ Handles Memory and CPU saving logic """
        if index < 0: return

        for i in range(self.tabs.count()):
            browser = self.tabs.widget(i)
            if not browser: continue
            
            page = browser.page()
            
            if i == index:
                # Wake up the active tab
                page.setLifecycleState(QWebEnginePage.LifecycleState.Active)
            else:
                # Background tabs
                if self.mem_saver.isChecked():
                    # Unloads from RAM (Reloads on click)
                    page.setLifecycleState(QWebEnginePage.LifecycleState.Discarded)
                elif self.cpu_saver.isChecked():
                    # Pauses JS (Stays in RAM)
                    page.setLifecycleState(QWebEnginePage.LifecycleState.Frozen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotHunterBrowser()
    window.show()
    sys.exit(app.exec())
