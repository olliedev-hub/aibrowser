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
    QLineEdit, QPushButton, QCheckBox, QComboBox, QVBoxLayout, QWidget, QLabel
)
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineSettings

class BotHunterUltimate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot Hunter - Ultimate Workstation")
        self.resize(1366, 768)

        # CORE PROFILE SETUP
        self.profile = QWebEngineProfile.defaultProfile()
        
        # USER AGENT DATABASE (Every OS)
        self.ua_map = {}
            "Linux (Default)": self.profile.http
